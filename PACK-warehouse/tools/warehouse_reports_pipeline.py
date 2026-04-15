#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Складской pipeline:
1. Находит свежие warehouse CSV после sync Google Sheets.
2. Создает карточку по каждому отчету.
3. Обновляет сводный markdown-отчет.
4. Опционально отправляет сводку в Telegram.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def repo_root() -> Path:
    # .../VK-offee/PACK-warehouse/tools/warehouse_reports_pipeline.py
    return Path(__file__).resolve().parents[2]


ROOT = repo_root()
KB_DIR = ROOT / "knowledge-base"
WAREHOUSE_DIR = ROOT / "PACK-warehouse"
CARDS_DIR = WAREHOUSE_DIR / "02-domain-entities" / "report-cards"
WP_DIR = WAREHOUSE_DIR / "04-work-products"
LATEST_REPORT = WP_DIR / "WH.REPORT.002-warehouse-sync-summary-latest.md"
REGISTRY_FILE = WP_DIR / "WH.REGISTRY.001-documents.csv"
BOT_REPORTS_DIR = KB_DIR / "Отчёты для бота" / "Склад"

KEYWORDS = (
    "Остатки по складам",
    "Отчет по инвентаризации",
    "Список зерна Самокиша - Тургенева - Луговая - Склад",
    "Список зерна Самокиша - Тургенева - Луговая - Комментарий",
)

def sanitize_slug(text: str) -> str:
    out = text.lower()
    out = re.sub(r"[^a-zа-я0-9]+", "-", out)
    out = out.strip("-")
    return out[:120] or "report"


def detect_report_type(name: str) -> str:
    low = name.lower()
    if ("комментарий" in low) or ("комментари" in low):
        return "comment"
    if "инвентаризац" in low:
        return "inventory"
    if "зерна" in low:
        return "beans"
    if "остатки" in low:
        return "stock"
    return "other"


def file_sha1(path: Path) -> str:
    sha = hashlib.sha1()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            sha.update(chunk)
    return sha.hexdigest()


def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_registry() -> dict[str, dict[str, str]]:
    if not REGISTRY_FILE.exists():
        return {}
    rows: dict[str, dict[str, str]] = {}
    with REGISTRY_FILE.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row.get("record_key") or "").strip()
            if key:
                rows[key] = row
    return rows


def save_registry(rows: dict[str, dict[str, str]]) -> None:
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "record_key",
        "source_file",
        "source_mtime",
        "source_size_bytes",
        "source_hash",
        "report_type",
        "status",
        "first_seen_at",
        "last_seen_at",
        "last_processed_at",
        "card_path",
        "bot_card_path",
        "error",
    ]
    with REGISTRY_FILE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for key in sorted(rows.keys()):
            writer.writerow(rows[key])


def find_recent_reports(hours: int) -> list[Path]:
    cutoff = datetime.now() - timedelta(hours=hours)
    items: list[Path] = []
    for p in KB_DIR.rglob("*.csv"):
        try:
            mtime = datetime.fromtimestamp(p.stat().st_mtime)
        except FileNotFoundError:
            continue
        if mtime < cutoff:
            continue
        name = p.name
        if any(k in name for k in KEYWORDS):
            items.append(p)
    return sorted(items)


def parse_csv_rows(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.reader(f))


def parse_stock_metrics(rows: list[list[str]]) -> dict:
    # Ожидаем формат: Наименование,Общее кол-во,Тургенева,Луговая,Самокиша
    metrics = {
        "rows": 0,
        "low_stock_count": 0,
        "low_stock_items": [],
        "totals_by_location": {"Тургенева": 0, "Луговая": 0, "Самокиша": 0},
    }
    if not rows:
        return metrics

    for r in rows[1:]:
        if not r or not r[0].strip():
            continue
        row = r + [""] * (5 - len(r))
        name = row[0].strip()
        total_raw = row[1].strip()
        if not total_raw or not re.fullmatch(r"\d+(\.\d+)?", total_raw):
            continue
        total = int(float(total_raw))
        metrics["rows"] += 1

        for idx, loc in ((2, "Тургенева"), (3, "Луговая"), (4, "Самокиша")):
            cell = row[idx].strip()
            if cell.isdigit():
                metrics["totals_by_location"][loc] += int(cell)

        if total <= 3:
            metrics["low_stock_count"] += 1
            metrics["low_stock_items"].append((name, total))

    return metrics


def parse_comment_bullets(rows: list[list[str]], max_lines: int = 12) -> list[str]:
    text_chunks: list[str] = []
    for r in rows:
        for c in r:
            cell = c.strip()
            if cell:
                text_chunks.append(cell)
    merged = "\n".join(text_chunks)
    lines = [ln.strip() for ln in merged.splitlines() if ln.strip()]
    # убираем слишком шумные строки
    lines = [ln for ln in lines if len(ln) >= 3]
    return lines[:max_lines]


def make_card(source: Path) -> tuple[Path, Path]:
    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    BOT_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    rel = source.relative_to(ROOT)
    stamp = datetime.fromtimestamp(source.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    source_sig = hashlib.sha1(rel.as_posix().encode("utf-8")).hexdigest()[:8]
    slug = f"{sanitize_slug(source.stem)}-{source_sig}"
    card_path = CARDS_DIR / f"WH.CARD.{slug}.md"
    bot_path = BOT_REPORTS_DIR / f"WH.BOT.{slug}.md"

    rows = parse_csv_rows(source)
    body_lines = [
        "---",
        "type: warehouse-report-card",
        f"source: {rel.as_posix()}",
        f"updated: {stamp}",
        "status: active",
        "---",
        "",
        f"# Карточка отчета: {source.name}",
        "",
        f"- Источник: `{rel.as_posix()}`",
        f"- Обновлен: `{stamp}`",
        "",
    ]

    if ("Комментарий" in source.name) or ("Комментари" in source.name):
        bullets = parse_comment_bullets(rows)
        body_lines.append("## Выжимка комментариев")
        if bullets:
            for b in bullets:
                body_lines.append(f"- {b}")
        else:
            body_lines.append("- Нет содержимого для выжимки.")
    else:
        metrics = parse_stock_metrics(rows)
        body_lines.extend(
            [
                "## Метрики",
                f"- Учетных позиций: **{metrics['rows']}**",
                f"- Низкие остатки (<=3): **{metrics['low_stock_count']}**",
                (
                    "- Сумма по точкам: "
                    f"Тургенева={metrics['totals_by_location']['Тургенева']}, "
                    f"Луговая={metrics['totals_by_location']['Луговая']}, "
                    f"Самокиша={metrics['totals_by_location']['Самокиша']}"
                ),
                "",
                "## Низкий остаток (top 12)",
            ]
        )
        low_items = metrics["low_stock_items"][:12]
        if low_items:
            for name, total in low_items:
                body_lines.append(f"- {name}: {total}")
        else:
            body_lines.append("- Низких остатков не найдено.")

    body_lines.extend(
        [
            "",
            "## Следующий шаг",
            "- Проверить потребности точки по заявке и сверить с минимальными остатками.",
            "- При необходимости добавить SKU в ближайшую закупку.",
            "",
        ]
    )

    text = "\n".join(body_lines)
    card_path.write_text(text, encoding="utf-8")
    bot_path.write_text(text, encoding="utf-8")
    return card_path, bot_path


def build_latest_summary(
    cards: Iterable[Path],
    bot_cards: Iterable[Path],
    hours: int,
    run_stats: dict[str, int],
) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    cards = sorted(set(cards))
    bot_cards = sorted(set(bot_cards))
    lines = [
        "---",
        "type: warehouse-sync-report",
        f"updated: {now}",
        "---",
        "",
        "# Warehouse Sync Summary",
        "",
        f"- Окно анализа: последние `{hours}` ч",
        f"- Входящих документов: **{run_stats['received']}**",
        f"- Обработано: **{run_stats['processed']}**",
        f"- Дубликатов: **{run_stats['duplicate']}**",
        f"- Ошибок: **{run_stats['error']}**",
        f"- Карточек сформировано: **{len(cards)}**",
        f"- Карточек для бота: **{len(bot_cards)}**",
        f"- Реестр: `{REGISTRY_FILE.relative_to(ROOT).as_posix()}`",
        "",
        "## Карточки",
    ]
    if cards:
        for c in cards:
            rel = c.relative_to(ROOT).as_posix()
            lines.append(f"- `{rel}`")
    else:
        lines.append("- Новых складских отчетов в окне не найдено.")
    lines.extend(["", "## Карточки для бота"])
    if bot_cards:
        for c in bot_cards:
            rel = c.relative_to(ROOT).as_posix()
            lines.append(f"- `{rel}`")
    else:
        lines.append("- Нет.")
    lines.append("")
    text = "\n".join(lines)
    LATEST_REPORT.write_text(text, encoding="utf-8")
    return text


def read_env_from_telegram_bot() -> dict[str, str]:
    env: dict[str, str] = {}
    env_path = ROOT / "telegram-bot" / ".env"
    if not env_path.exists():
        return env
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def read_key_value_env(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip()
    return env


def read_first_line(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore").strip()


def resolve_telegram_credentials() -> tuple[str, str]:
    env_file = read_env_from_telegram_bot()
    aist_env = read_key_value_env(Path.home() / ".config" / "aist" / "env")
    exocortex_chat = read_first_line(Path.home() / ".config" / "exocortex" / "telegram-chat-id")
    exocortex_token = read_first_line(Path.home() / ".config" / "exocortex" / "telegram-token")
    # 1) Явные env (без смешивания со сторонними источниками).
    env_token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    env_chat = (
        os.getenv("WAREHOUSE_REPORT_CHAT_ID", "").strip()
        or os.getenv("TELEGRAM_CHAT_ID", "").strip()
    )
    if env_token and env_chat:
        return env_token, env_chat

    # 2) telegram-bot/.env (локальный продуктовый контур).
    bot_token = env_file.get("TELEGRAM_BOT_TOKEN", "").strip()
    bot_chat = (
        env_file.get("WAREHOUSE_REPORT_CHAT_ID", "").strip()
        or env_file.get("TELEGRAM_CHAT_ID", "").strip()
    )
    if bot_token and bot_chat:
        return bot_token, bot_chat

    # 3) ~/.config/aist/env (каноничный инженерный env).
    aist_token = aist_env.get("TELEGRAM_BOT_TOKEN", "").strip()
    aist_chat = (
        aist_env.get("WAREHOUSE_REPORT_CHAT_ID", "").strip()
        or aist_env.get("TELEGRAM_CHAT_ID", "").strip()
    )
    if aist_token and aist_chat:
        return aist_token, aist_chat

    # 4) ~/.config/exocortex/* (legacy fallback, но пара сохраняется из одного слоя).
    if exocortex_token and exocortex_chat:
        return exocortex_token, exocortex_chat

    # 5) Последний fallback на случай частично заполненного окружения.
    token = env_token or bot_token or aist_token or exocortex_token
    chat_id = env_chat or bot_chat or aist_chat or exocortex_chat
    return token, chat_id


def send_telegram_message(text: str) -> tuple[bool, str]:
    token, chat_id = resolve_telegram_credentials()
    if not token:
        return False, "skip: TELEGRAM_BOT_TOKEN missing"
    if not chat_id:
        return False, "skip: WAREHOUSE_REPORT_CHAT_ID/TELEGRAM_CHAT_ID missing"

    payload = urlencode(
        {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": "true",
        }
    ).encode("utf-8")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    req = Request(url, data=payload, method="POST")
    try:
        with urlopen(req, timeout=20) as resp:
            ok = 200 <= resp.status < 300
        return ok, f"sent:{ok}"
    except Exception as exc:  # pragma: no cover
        detail = str(exc)
        try:
            detail = f"{detail}; body={exc.read().decode('utf-8', errors='ignore')}"
        except Exception:
            pass
        return False, f"send_failed:{detail}"


def telegram_text(cards: list[Path], hours: int) -> str:
    ts = datetime.now().strftime("%d.%m.%Y %H:%M")
    header = [
        "📦 <b>Склад: автоотчёт</b>",
        f"Время: <code>{ts}</code>",
        f"Окно: последние <b>{hours}ч</b>",
        f"Карточек: <b>{len(cards)}</b>",
        "",
    ]
    if not cards:
        header.append("Новых складских отчётов не найдено.")
        return "\n".join(header)

    header.append("Карточки:")
    for c in cards[:12]:
        rel = c.relative_to(ROOT).as_posix()
        header.append(f"• <code>{rel}</code>")
    if len(cards) > 12:
        header.append(f"• … и ещё {len(cards)-12}")
    return "\n".join(header)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", type=int, default=6)
    parser.add_argument("--send-telegram", action="store_true")
    args = parser.parse_args()

    WP_DIR.mkdir(parents=True, exist_ok=True)
    CARDS_DIR.mkdir(parents=True, exist_ok=True)

    sources = find_recent_reports(hours=args.hours)
    registry = load_registry()
    stamp = now_stamp()
    run_stats = {"received": len(sources), "processed": 0, "duplicate": 0, "error": 0}
    cards: list[Path] = []
    bot_cards: list[Path] = []
    for src in sources:
        rel = src.relative_to(ROOT).as_posix()
        src_stat = src.stat()
        src_mtime = datetime.fromtimestamp(src_stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        src_hash = file_sha1(src)
        record_key = f"{rel}|{src_stat.st_size}|{int(src_stat.st_mtime)}|{src_hash[:12]}"

        existing = registry.get(record_key)
        if existing:
            run_stats["duplicate"] += 1
            existing["status"] = "duplicate"
            existing["last_seen_at"] = stamp
            continue

        row = {
            "record_key": record_key,
            "source_file": rel,
            "source_mtime": src_mtime,
            "source_size_bytes": str(src_stat.st_size),
            "source_hash": src_hash,
            "report_type": detect_report_type(src.name),
            "status": "new",
            "first_seen_at": stamp,
            "last_seen_at": stamp,
            "last_processed_at": "",
            "card_path": "",
            "bot_card_path": "",
            "error": "",
        }

        try:
            card, bot_card = make_card(src)
            cards.append(card)
            bot_cards.append(bot_card)
            row["status"] = "processed"
            row["last_processed_at"] = stamp
            row["card_path"] = card.relative_to(ROOT).as_posix()
            row["bot_card_path"] = bot_card.relative_to(ROOT).as_posix()
            run_stats["processed"] += 1
        except Exception as exc:  # pragma: no cover
            row["status"] = "error"
            row["error"] = str(exc)[:500]
            run_stats["error"] += 1

        registry[record_key] = row

    save_registry(registry)
    build_latest_summary(cards, bot_cards, args.hours, run_stats)
    print(
        f"[warehouse] sources={len(sources)} cards={len(set(cards))} "
        f"bot_cards={len(set(bot_cards))} duplicates={run_stats['duplicate']} "
        f"errors={run_stats['error']} summary={LATEST_REPORT} registry={REGISTRY_FILE}"
    )

    if args.send_telegram:
        text = telegram_text(cards, args.hours)
        ok, info = send_telegram_message(text)
        print(f"[warehouse] telegram={info}")
        if not ok:
            # Не валим пайплайн из-за Telegram; фиксируем как warning.
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
