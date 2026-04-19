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
import json
import os
import re
import shutil
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable
from urllib.parse import quote, urlencode
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
DECISION_QUEUE = WP_DIR / "WH.SESSION.001-decision-queue-latest.md"
REGISTRY_FILE = WP_DIR / "WH.REGISTRY.001-documents.csv"
DLQ_DIR = WAREHOUSE_DIR / "03-quarantine" / "dlq-files"
DLQ_REPORT = WP_DIR / "WH.DLQ.001-quarantine-report.md"
BOT_REPORTS_DIR = KB_DIR / "Отчёты для бота" / "Склад"

KEYWORDS = (
    "Остатки по складам",
    "Отчет по инвентаризации",
    "Продажи_",
    "Выручка_",
    "Каталог_",
    "Накладные_",
    "Продажи ",
    "Выручка ",
    "Каталог ",
    "Накладные ",
    "Список зерна Самокиша - Тургенева - Луговая - Склад",
    "Список зерна Самокиша - Тургенева - Луговая - Комментарий",
    "АБС анализ",
    "АБС-анализ",
    "ABC анализ",
    "ABC-анализ",
    "Abc",
    "АБС",
)

def sanitize_slug(text: str) -> str:
    out = text.lower()
    out = re.sub(r"[^a-zа-я0-9]+", "-", out)
    out = out.strip("-")
    return out[:120] or "report"


def detect_report_type(name: str) -> str:
    low = name.lower()
    if "продаж" in low:
        return "sales"
    if "выруч" in low:
        return "revenue"
    if "каталог" in low:
        return "catalog"
    if "накладн" in low:
        return "invoice"
    if ("комментарий" in low) or ("комментари" in low):
        return "comment"
    if "инвентаризац" in low:
        return "inventory"
    if "зерна" in low:
        return "beans"
    if "остатки" in low:
        return "stock"
    if ("абс" in low) or ("abc" in low):
        return "abc"
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


def escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def detect_github_repo_web_url() -> str:
    try:
        remote = (
            subprocess.check_output(
                ["git", "-C", str(ROOT), "remote", "get-url", "origin"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            .strip()
            .rstrip("/")
        )
    except Exception:
        return ""

    if remote.startswith("git@github.com:"):
        path = remote.split("git@github.com:", 1)[1]
        if path.endswith(".git"):
            path = path[:-4]
        return f"https://github.com/{path}"
    if remote.startswith("https://github.com/"):
        if remote.endswith(".git"):
            remote = remote[:-4]
        return remote
    return ""


def detect_git_branch() -> str:
    try:
        branch = (
            subprocess.check_output(
                ["git", "-C", str(ROOT), "rev-parse", "--abbrev-ref", "HEAD"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            .strip()
        )
        if branch and branch != "HEAD":
            return branch
    except Exception:
        pass

    # Detached HEAD fallback: пробуем origin/HEAD -> origin/main
    try:
        ref = (
            subprocess.check_output(
                ["git", "-C", str(ROOT), "symbolic-ref", "refs/remotes/origin/HEAD"],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            .strip()
        )
        if ref.startswith("refs/remotes/origin/"):
            cand = ref.split("refs/remotes/origin/", 1)[1].strip()
            if cand:
                return cand
    except Exception:
        pass

    return "main"


def path_exists_in_head(rel_path: str) -> bool:
    if not rel_path:
        return False
    try:
        subprocess.check_call(
            ["git", "-C", str(ROOT), "cat-file", "-e", f"HEAD:{rel_path}"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception:
        return False


def build_github_link(rel_path: str) -> str:
    base = (
        os.getenv("WAREHOUSE_REPORT_BASE_URL", "").strip()
        or detect_github_repo_web_url()
    )
    branch = os.getenv("WAREHOUSE_REPORT_BRANCH", "").strip() or detect_git_branch()
    if not base:
        return ""
    if not path_exists_in_head(rel_path):
        return ""
    return f"{base}/blob/{branch}/{quote(rel_path, safe='/')}"


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
        "dlq_path",
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
    for ext in ("*.csv", "*.pdf"):
        for p in KB_DIR.rglob(ext):
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
        rows = list(csv.reader(f))
    if not rows:
        raise ValueError("empty csv")
    return rows


def extract_pdf_payload(path: Path) -> dict[str, object]:
    payload: dict[str, object] = {
        "text": "",
        "pages": 0,
        "method": "",
        "error": "",
    }

    # 1) Pure-Python parser (предпочтительно для portability).
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        texts: list[str] = []
        for page in reader.pages:
            try:
                texts.append((page.extract_text() or "").strip())
            except Exception:
                texts.append("")
        text = "\n".join(t for t in texts if t)
        if text.strip():
            payload["text"] = text
            payload["pages"] = len(reader.pages)
            payload["method"] = "pypdf"
            return payload
    except Exception as exc:
        payload["error"] = str(exc)

    # 2) Fallback to pdftotext CLI (если доступен в окружении).
    try:
        proc = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
        text = (proc.stdout or "").strip()
        if text:
            payload["text"] = text
            payload["method"] = "pdftotext"
            return payload
    except Exception as exc:
        payload["error"] = f"{payload.get('error', '')}; {exc}".strip("; ")

    return payload


def parse_invoice_pdf_metrics(text: str) -> dict[str, object]:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    money_raw = re.findall(r"\b\d{1,3}(?:[ \u00a0]\d{3})*(?:[.,]\d{2})\b", text)
    money_vals: list[float] = []
    for m in money_raw:
        val = m.replace("\u00a0", "").replace(" ", "").replace(",", ".")
        try:
            money_vals.append(float(val))
        except ValueError:
            continue

    invoice_numbers = re.findall(r"(?:накладн\w*\s*№?\s*|№\s*)(\d{4,})", text, flags=re.IGNORECASE)
    dates = re.findall(r"\b\d{2}[./]\d{2}[./]\d{4}\b", text)
    vendors: list[str] = []
    for ln in lines[:250]:
        low = ln.lower()
        if any(k in low for k in ("ип ", "ооо ", "зао ", "поставщик", "продавец")):
            vendors.append(ln)
    vendors = list(dict.fromkeys(vendors))[:5]

    return {
        "line_count": len(lines),
        "char_count": len(text),
        "money_count": len(money_vals),
        "money_top": sorted(money_vals, reverse=True)[:8],
        "invoice_numbers": sorted(set(invoice_numbers))[:20],
        "dates": sorted(set(dates))[:10],
        "vendors": vendors,
        "preview_lines": lines[:12],
    }


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


def parse_abc_categories(rows: list[list[str]]) -> dict[str, str]:
    """Извлечь маппинг {название_позиции: категория A/B/C} из ABC-анализа."""
    result: dict[str, str] = {}
    if not rows:
        return result
    # Ищем заголовок: столбец с названием и столбец с категорией
    header = [c.strip().lower() for c in rows[0]]
    name_col = -1
    cat_col = -1
    for i, h in enumerate(header):
        if any(kw in h for kw in ("наимен", "товар", "позиц", "продукт", "name")):
            if name_col == -1:
                name_col = i
        if any(kw in h for kw in ("категор", "класс", "abc", "абс", "group")):
            if cat_col == -1:
                cat_col = i
    if name_col == -1:
        name_col = 0
    if cat_col == -1:
        # Ищем столбец где есть значения A/B/C
        for i in range(len(rows[0])):
            vals = {r[i].strip().upper() for r in rows[1:] if len(r) > i and r[i].strip()}
            if vals and vals.issubset({"A", "B", "C", "А", "В", "С"}):
                cat_col = i
                break
    if cat_col == -1:
        return result
    for r in rows[1:]:
        if len(r) <= max(name_col, cat_col):
            continue
        name = r[name_col].strip()
        cat = r[cat_col].strip().upper()
        # Нормализуем кириллические буквы к латинице
        cat = cat.replace("А", "A").replace("В", "B").replace("С", "C")
        if name and cat in ("A", "B", "C"):
            result[name.lower()] = cat
    return result


def parse_number(value: str) -> float | None:
    raw = value.strip().replace("\u00a0", "").replace(" ", "")
    if not raw:
        return None
    raw = raw.replace(",", ".")
    if not re.fullmatch(r"-?\d+(\.\d+)?", raw):
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def extract_period_from_text(text: str) -> str:
    dates = re.findall(r"\d{2}\.\d{2}\.\d{4}", text)
    if len(dates) >= 2:
        return f"{dates[0]} — {dates[1]}"
    dates_iso = re.findall(r"\d{4}-\d{2}-\d{2}", text)
    if len(dates_iso) >= 2:
        return f"{dates_iso[0]} — {dates_iso[1]}"
    return "n/a"


def parse_table_profile(rows: list[list[str]]) -> dict[str, object]:
    max_cols = max((len(r) for r in rows), default=0)
    data_rows = rows[1:] if len(rows) > 1 else []
    non_empty_rows = sum(1 for r in data_rows if any(c.strip() for c in r))
    headers = [c.strip() for c in (rows[0] if rows else []) if c.strip()]

    numeric_col_stats: list[tuple[int, str, float]] = []
    if rows:
        width = len(rows[0])
        for i in range(width):
            vals = []
            for r in data_rows:
                if len(r) <= i:
                    continue
                num = parse_number(r[i])
                if num is not None:
                    vals.append(num)
            if vals:
                label = rows[0][i].strip() if i < len(rows[0]) else f"col_{i+1}"
                numeric_col_stats.append((i, label or f"col_{i+1}", sum(vals)))
    numeric_col_stats.sort(key=lambda x: abs(x[2]), reverse=True)

    return {
        "rows_total": len(rows),
        "rows_data": non_empty_rows,
        "cols": max_cols,
        "headers": headers[:8],
        "top_numeric": numeric_col_stats[:3],
    }


def parse_non_stock_inventory_metrics(rows: list[list[str]]) -> dict[str, object]:
    names: list[str] = []
    debt_notes: list[str] = []
    money_vals: list[float] = []

    money_re = re.compile(r"\d{1,3}(?:[ \u00a0]\d{3})*(?:[.,]\d{2})\s*₽?")
    for r in rows:
        if len(r) > 1:
            candidate = (r[1] or "").strip()
            if candidate and not re.search(r"\d", candidate) and len(candidate) >= 3:
                names.append(candidate)
        for c in r:
            cell = (c or "").strip()
            if not cell:
                continue
            if "долг" in cell.lower():
                debt_notes.append(cell)
            for m in money_re.findall(cell):
                raw = m.replace("₽", "").replace("\u00a0", "").replace(" ", "").replace(",", ".").strip()
                try:
                    money_vals.append(float(raw))
                except ValueError:
                    continue
    names = list(dict.fromkeys(names))
    debt_notes = list(dict.fromkeys(debt_notes))
    return {
        "people_count": len(names),
        "people_top": names[:10],
        "money_cells_count": len(money_vals),
        "money_cells_sum": round(sum(money_vals), 2) if money_vals else 0.0,
        "debt_notes": debt_notes[:6],
    }


def build_smart_analytics(insights: list[dict]) -> dict:
    """Кросс-анализ остатков + ABC категорий."""
    # Собираем все остатки (позиция -> остаток)
    stock_map: dict[str, int] = {}
    for item in insights:
        if item.get("report_type") in ("stock", "inventory", "beans"):
            for name, qty in (item.get("top_low_items") or []):
                key = name.lower().strip()
                if key not in stock_map or stock_map[key] > qty:
                    stock_map[key] = qty

    # Собираем ABC категории
    abc_map: dict[str, str] = {}
    for item in insights:
        if item.get("report_type") == "abc":
            abc_map.update(item.get("abc_categories") or {})

    if not stock_map:
        return {}

    urgent: list[str] = []    # A + мало
    attention: list[str] = [] # B + мало
    excess: list[str] = []    # C + много
    no_abc: list[str] = []    # мало, но ABC нет

    for name_low, qty in sorted(stock_map.items(), key=lambda x: x[1]):
        cat = abc_map.get(name_low)
        display = f"{name_low.title()}: {qty} шт"
        if cat == "A":
            urgent.append(display)
        elif cat == "B":
            attention.append(display)
        elif cat == "C":
            excess.append(display)
        else:
            no_abc.append(display)

    # Позиции C категории с нормальными остатками
    for name_low, cat in abc_map.items():
        if cat == "C" and name_low not in stock_map:
            excess.append(f"{name_low.title()} (C-категория, в реестре)")

    return {
        "urgent": urgent[:8],
        "attention": attention[:6],
        "excess": excess[:5],
        "no_abc": no_abc[:5],
        "has_abc": bool(abc_map),
    }


def detect_data_gaps(insights: list[dict]) -> list[str]:
    """Каких данных не хватает для управленческого отчёта руководителя."""
    types = {str(item.get("report_type", "")) for item in insights}
    gaps: list[str] = []

    if "invoice" not in types:
        gaps.append("Нет накладных в структурированном виде: не считаем точную закупочную себестоимость по SKU.")
    else:
        gaps.append("Накладные PDF требуют OCR-разбора до SKU-уровня (цена, поставщик, дата).")

    if "sales" not in types:
        gaps.append("Нет отчёта продаж по SKU за период: нельзя считать спрос и оборачиваемость по позициям.")

    if "revenue" not in types:
        gaps.append("Нет детальной выручки по точкам/дням: ограничен контроль динамики точек.")

    gaps.append("Нет отчёта списаний/брака: не видно потери и причины перерасхода.")
    gaps.append("Нет факта поставок (lead time, недопоставки): нельзя оценить надёжность поставщиков.")
    return gaps[:5]


def make_card(source: Path) -> tuple[Path, Path, dict]:
    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    BOT_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    rel = source.relative_to(ROOT)
    stamp = datetime.fromtimestamp(source.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    source_sig = hashlib.sha1(rel.as_posix().encode("utf-8")).hexdigest()[:8]
    slug = f"{sanitize_slug(source.stem)}-{source_sig}"
    card_path = CARDS_DIR / f"WH.CARD.{slug}.md"
    bot_path = BOT_REPORTS_DIR / f"WH.BOT.{slug}.md"

    suffix = source.suffix.lower()
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

    insight: dict[str, object] = {
        "title": source.name,
        "report_type": detect_report_type(source.name),
        "source_rel": rel.as_posix(),
        "card_rel": "",
        "bot_card_rel": "",
    }

    report_type = detect_report_type(source.name)
    if (suffix == ".pdf") and (report_type == "invoice"):
        payload = extract_pdf_payload(source)
        text = str(payload.get("text", "") or "")
        metrics = parse_invoice_pdf_metrics(text) if text else {}
        period = extract_period_from_text(source.name)

        insight["report_type"] = "invoice"
        insight["rows"] = int(metrics.get("line_count", 0) or 0)
        insight["period"] = period
        insight["invoice_numbers"] = metrics.get("invoice_numbers", [])
        insight["invoice_money_top"] = metrics.get("money_top", [])

        body_lines.extend(
            [
                "## Накладные (PDF): авторазбор",
                f"- Период: **{period}**",
                f"- Метод извлечения: **{payload.get('method') or 'n/a'}**",
                f"- Страниц: **{payload.get('pages') or 0}**",
                f"- Извлечено строк: **{metrics.get('line_count', 0) if metrics else 0}**",
                f"- Извлечено символов: **{metrics.get('char_count', 0) if metrics else 0}**",
            ]
        )
        if metrics:
            nums = metrics.get("invoice_numbers") or []
            if nums:
                body_lines.append(f"- Номера накладных: **{', '.join(str(x) for x in nums[:10])}**")
            dts = metrics.get("dates") or []
            if dts:
                body_lines.append(f"- Обнаруженные даты: **{', '.join(str(x) for x in dts[:8])}**")
            vendors = metrics.get("vendors") or []
            if vendors:
                body_lines.append("- Поставщики (по тексту):")
                for v in vendors:
                    body_lines.append(f"  - {v}")
            mtop = metrics.get("money_top") or []
            if mtop:
                body_lines.append("- Крупные суммы (по тексту, авто):")
                for m in mtop[:6]:
                    body_lines.append(f"  - {m:,.2f}".replace(",", " "))
            preview = metrics.get("preview_lines") or []
            if preview:
                body_lines.append("")
                body_lines.append("## Превью извлечённого текста")
                for ln in preview[:10]:
                    body_lines.append(f"- {ln}")
        if not text:
            body_lines.append("- Не удалось извлечь текст из PDF автоматически.")
            if payload.get("error"):
                body_lines.append(f"- Ошибка: `{payload.get('error')}`")
    else:
        rows = parse_csv_rows(source)
        if ("Комментарий" in source.name) or ("Комментари" in source.name):
            bullets = parse_comment_bullets(rows)
            insight["comment_count"] = len(bullets)
            insight["comment_preview"] = bullets[:3]
            body_lines.append("## Выжимка комментариев")
            if bullets:
                for b in bullets:
                    body_lines.append(f"- {b}")
            else:
                body_lines.append("- Нет содержимого для выжимки.")
        else:
            if report_type == "abc":
                categories = parse_abc_categories(rows)
                insight["abc_categories"] = categories
                counts = {"A": 0, "B": 0, "C": 0}
                for cat in categories.values():
                    if cat in counts:
                        counts[cat] += 1
                body_lines.extend([
                    "## ABC Анализ",
                    f"- Позиций A (приоритет): **{counts['A']}**",
                    f"- Позиций B (средние): **{counts['B']}**",
                    f"- Позиций C (низкий приоритет): **{counts['C']}**",
                    "",
                    "## Топ категории A",
                ])
                a_items = [name for name, cat in categories.items() if cat == "A"][:10]
                for name in a_items:
                    body_lines.append(f"- {name.title()}")
                if not a_items:
                    body_lines.append("- Не найдено.")
            elif report_type in {"stock", "inventory", "beans"}:
                metrics = parse_stock_metrics(rows)
                if metrics["rows"] > 0:
                    insight["rows"] = metrics["rows"]
                    insight["low_stock_count"] = metrics["low_stock_count"]
                    insight["top_low_items"] = metrics["low_stock_items"][:3]
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
                else:
                    # Файл помечен как инвентаризация, но не является SKU-остатками.
                    # Делаем понятную бизнес-выжимку вместо пустых нулей.
                    profile = parse_table_profile(rows)
                    extra = parse_non_stock_inventory_metrics(rows)
                    insight["report_type"] = "inventory_non_stock"
                    insight["rows"] = int(profile["rows_data"])
                    insight["low_stock_count"] = 0
                    insight["top_low_items"] = []
                    insight["inventory_people_count"] = int(extra.get("people_count", 0) or 0)
                    insight["inventory_money_cells_count"] = int(extra.get("money_cells_count", 0) or 0)
                    insight["inventory_debt_notes"] = extra.get("debt_notes", [])

                    body_lines.extend(
                        [
                            "## Тип файла",
                            "- Это не карточка товарных остатков по SKU.",
                            "- Это сводная инвентаризационно-финансовая таблица (по сотрудникам/периодам).",
                            "",
                            "## Выжимка по данным",
                            f"- Строк данных: **{profile['rows_data']}**",
                            f"- Столбцов: **{profile['cols']}**",
                            f"- Сотрудников в таблице (по автоопределению): **{extra['people_count']}**",
                            f"- Денежных значений: **{extra['money_cells_count']}**",
                            f"- Сумма денежных значений (справочно): **{float(extra['money_cells_sum']):,.2f} ₽**".replace(",", " "),
                        ]
                    )
                    people = extra.get("people_top") or []
                    if people:
                        body_lines.append(f"- Имена (пример): **{', '.join(str(x) for x in people[:8])}**")
                    debts = extra.get("debt_notes") or []
                    if debts:
                        body_lines.append("")
                        body_lines.append("## Пометки по долгам/корректировкам")
                        for d in debts:
                            body_lines.append(f"- {d}")
            else:
                profile = parse_table_profile(rows)
                period = extract_period_from_text(source.name)
                insight["rows"] = int(profile["rows_data"])
                insight["low_stock_count"] = 0
                insight["top_low_items"] = []
                insight["period"] = period
                insight["table_headers"] = profile["headers"]
                insight["top_numeric"] = profile["top_numeric"]

                type_human = {
                    "sales": "Продажи",
                    "revenue": "Выручка",
                    "catalog": "Каталог",
                    "invoice": "Накладные",
                    "other": "Табличный отчёт",
                }.get(report_type, "Табличный отчёт")

                body_lines.extend(
                    [
                        f"## {type_human}: структурная выжимка",
                        f"- Период: **{period}**",
                        f"- Строк данных: **{profile['rows_data']}**",
                        f"- Столбцов: **{profile['cols']}**",
                    ]
                )
                headers = profile.get("headers") or []
                if headers:
                    body_lines.append(f"- Ключевые колонки: **{', '.join(str(h) for h in headers)}**")
                top_numeric = profile.get("top_numeric") or []
                if top_numeric:
                    body_lines.append("")
                    body_lines.append("## Числовые итоги (автооценка)")
                    for _, label, total in top_numeric:
                        body_lines.append(f"- {label}: **{total:,.2f}**".replace(",", " "))
                if report_type == "invoice":
                    body_lines.append("")
                    body_lines.append("## Важно")
                    body_lines.append("- Для PDF-накладных нужна OCR-нормализация для SKU-level аналитики (в этом цикле только базовая выжимка).")

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
    insight["card_rel"] = card_path.relative_to(ROOT).as_posix()
    insight["bot_card_rel"] = bot_path.relative_to(ROOT).as_posix()
    return card_path, bot_path, insight


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
        f"- DLQ: **{run_stats['dlq']}**",
        f"- Карточек сформировано: **{len(cards)}**",
        f"- Карточек для бота: **{len(bot_cards)}**",
        f"- Реестр: `{REGISTRY_FILE.relative_to(ROOT).as_posix()}`",
        f"- Quarantine report: `{DLQ_REPORT.relative_to(ROOT).as_posix()}`",
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


def build_decision_queue(insights: list[dict], run_stats: dict[str, int], manual_run: bool) -> str:
    """Очередь управленческих сессий по свежим складским артефактам."""
    ts = now_stamp()
    mode = "manual" if manual_run else "auto"
    lines = [
        "---",
        "type: warehouse-decision-queue",
        f"updated: {ts}",
        f"mode: {mode}",
        "---",
        "",
        "# Warehouse Decision Queue",
        "",
        "## Сводка цикла",
        f"- Входящих: **{run_stats['received']}**",
        f"- Обработано: **{run_stats['processed']}**",
        f"- Дубликатов: **{run_stats['duplicate']}**",
        f"- Ошибок: **{run_stats['error']}**",
        "",
        "## Сессии к разбору",
    ]

    if not insights:
        lines.append("- Новых сессий нет: в текущем окне не сформированы новые карточки.")
    else:
        for idx, item in enumerate(insights, start=1):
            title = str(item.get("title", "warehouse-report"))
            card_rel = str(item.get("card_rel", ""))
            source_rel = str(item.get("source_rel", ""))
            report_type = str(item.get("report_type", "other"))

            if report_type in {"stock", "inventory", "beans"}:
                action = "Проверить дефицитные SKU и сформировать заказ-лист."
            elif report_type == "abc":
                action = "Обновить приоритеты A/B/C и reorder-план."
            elif report_type == "comment":
                action = "Разобрать комментарии и зафиксировать операционные задачи."
            else:
                action = "Сверить данные и вынести решение по закупке/остаткам."

            lines.extend(
                [
                    f"### WH.SESSION.{idx:03d} — {title}",
                    f"- Тип: `{report_type}`",
                    f"- Статус: `pending_owner_review`",
                    f"- Карточка: `{card_rel}`" if card_rel else "- Карточка: `n/a`",
                    f"- Источник: `{source_rel}`" if source_rel else "- Источник: `n/a`",
                    f"- Следующее действие: {action}",
                    "",
                ]
            )

    text = "\n".join(lines) + "\n"
    DECISION_QUEUE.write_text(text, encoding="utf-8")
    return text


def replay_insights_from_registry(registry: dict[str, dict[str, str]], limit: int = 10) -> list[dict]:
    """Собрать demo-выжимку из уже обработанных карточек, если новых входящих нет."""
    rows = []
    for row in registry.values():
        if (row.get("status") or "").strip() not in {"processed", "duplicate"}:
            continue
        card_rel = (row.get("card_path") or "").strip()
        if not card_rel:
            continue
        try:
            ts = datetime.strptime((row.get("last_processed_at") or "").strip(), "%Y-%m-%d %H:%M:%S")
        except Exception:
            ts = datetime.min
        rows.append((ts, row))
    rows.sort(key=lambda x: x[0], reverse=True)

    insights: list[dict] = []
    for _, row in rows[: max(1, limit)]:
        source_file = (row.get("source_file") or "").strip()
        title = Path(source_file).name if source_file else Path(row.get("card_path") or "report").name
        insights.append(
            {
                "title": title,
                "report_type": (row.get("report_type") or "other").strip(),
                "source_rel": source_file,
                "card_rel": (row.get("card_path") or "").strip(),
                "bot_card_rel": (row.get("bot_card_path") or "").strip(),
            }
        )
    return insights


def append_dlq_entry(source: Path, record_key: str, reason: str) -> str:
    DLQ_DIR.mkdir(parents=True, exist_ok=True)
    DLQ_REPORT.parent.mkdir(parents=True, exist_ok=True)

    stamp = now_stamp()
    rel = source.relative_to(ROOT).as_posix()
    slug = hashlib.sha1(record_key.encode("utf-8")).hexdigest()[:10]
    copy_name = f"{source.stem}-{slug}{source.suffix}"
    dlq_copy = DLQ_DIR / copy_name
    shutil.copy2(source, dlq_copy)

    if not DLQ_REPORT.exists():
        DLQ_REPORT.write_text(
            "\n".join(
                [
                    "---",
                    "type: warehouse-dlq-report",
                    f"updated: {stamp}",
                    "---",
                    "",
                    "# Warehouse DLQ Report",
                    "",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

    existing = DLQ_REPORT.read_text(encoding="utf-8")
    updated = re.sub(
        r"^updated: .*$",
        f"updated: {stamp}",
        existing,
        count=1,
        flags=re.MULTILINE,
    )
    entry = "\n".join(
        [
            f"## {stamp} — {source.name}",
            f"- Source: `{rel}`",
            f"- DLQ copy: `{dlq_copy.relative_to(ROOT).as_posix()}`",
            f"- Reason: `{reason}`",
            "",
        ]
    )
    DLQ_REPORT.write_text(updated + entry, encoding="utf-8")
    return dlq_copy.relative_to(ROOT).as_posix()


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


def telegram_text(
    cards: list[Path],
    hours: int,
    run_stats: dict[str, int],
    insights: list[dict],
    manual_run: bool,
) -> str:
    ts = datetime.now().strftime("%d.%m.%Y %H:%M")
    report_rel = LATEST_REPORT.relative_to(ROOT).as_posix()
    report_url = build_github_link(report_rel)
    queue_rel = DECISION_QUEUE.relative_to(ROOT).as_posix()
    queue_url = build_github_link(queue_rel)

    mode = "manual" if manual_run else "auto"
    lines = [
        "📦 <b>Manager Digest · Склад</b>",
        f"Время: <code>{ts}</code> · Режим: <b>{mode}</b> · Окно: <b>{hours}ч</b>",
    ]

    analytics = build_smart_analytics(insights)
    if run_stats["error"] > 0:
        verdict = "🔴 Требует внимания"
    elif analytics.get("urgent"):
        verdict = "🟡 Есть риск дефицита"
    else:
        verdict = "🟢 Стабильно"
    lines.extend(
        [
            f"Вердикт: <b>{verdict}</b>",
            (
                "Поток: "
                f"входящих <b>{run_stats['received']}</b> · "
                f"обработано <b>{run_stats['processed']}</b> · "
                f"ошибок <b>{run_stats['error']}</b>"
            ),
        ]
    )

    # Раздел 1: Срочно (до 24ч)
    urgent_items: list[str] = []
    for item in analytics.get("urgent", [])[:5]:
        urgent_items.append(f"Заказать: {item}")
    if run_stats["error"] > 0:
        urgent_items.append(f"Разобрать ошибки обработки: {run_stats['error']}")
    if not urgent_items:
        urgent_items.append("Критичных дефицитов на 24ч не выявлено.")
    urgent_items = urgent_items[:5]

    # Раздел 2: Планово (2-7 дней)
    planned_items: list[str] = []
    for item in analytics.get("attention", [])[:5]:
        planned_items.append(f"Проверить спрос/остаток: {item}")
    has_invoices = any(str(it.get("report_type", "")) == "invoice" for it in insights)
    if has_invoices and len(planned_items) < 5:
        planned_items.append("Сверить закупочные цены из накладных с каталогом (2-7 дней).")
    if not planned_items:
        planned_items.append("Плановых действий на 2-7 дней не выявлено.")
    planned_items = planned_items[:5]

    # Раздел 3: Что не заказывать/сократить
    reduce_items: list[str] = []
    for item in analytics.get("excess", [])[:5]:
        reduce_items.append(f"Сократить дозакупку: {item}")
    if not reduce_items:
        reduce_items.append("Явных позиций для сокращения закупки не выявлено.")
    reduce_items = reduce_items[:5]

    # Раздел 4: Риски данных (чего не хватает)
    data_risks: list[str] = []
    gaps = detect_data_gaps(insights)
    for g in gaps[:5]:
        data_risks.append(g)
    if not analytics.get("has_abc"):
        data_risks.append("Приоритизация A/B/C недоступна, решения приняты по остаткам/движению.")
    if not data_risks:
        data_risks.append("Критичных пробелов данных не обнаружено.")
    data_risks = data_risks[:5]

    lines.append("")
    lines.append("<b>Срочно (до 24ч)</b>")
    for item in urgent_items:
        lines.append(f"• {escape_html(item)}")

    lines.append("")
    lines.append("<b>Планово (2-7 дней)</b>")
    for item in planned_items:
        lines.append(f"• {escape_html(item)}")

    lines.append("")
    lines.append("<b>Что не заказывать/сократить</b>")
    for item in reduce_items:
        lines.append(f"• {escape_html(item)}")

    lines.append("")
    lines.append("<b>Риски данных (чего не хватает)</b>")
    for item in data_risks:
        lines.append(f"• {escape_html(item)}")

    lines.append("")
    if report_url:
        lines.append(f"Полный отчёт: <a href=\"{report_url}\">WH.REPORT.002</a>")
    else:
        lines.append(f"Полный отчёт: <code>{escape_html(report_rel)}</code>")
    if queue_url:
        lines.append(f"Очередь решений: <a href=\"{queue_url}\">WH.SESSION.001</a>")
    else:
        lines.append(f"Очередь решений: <code>{escape_html(queue_rel)}</code>")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hours", type=int, default=6)
    parser.add_argument("--send-telegram", action="store_true")
    parser.add_argument("--telegram-on-empty", action="store_true")
    parser.add_argument("--manual-run", action="store_true")
    parser.add_argument("--refresh-duplicates", action="store_true")
    parser.add_argument("--replay-latest-cards", type=int, default=0)
    args = parser.parse_args()

    WP_DIR.mkdir(parents=True, exist_ok=True)
    CARDS_DIR.mkdir(parents=True, exist_ok=True)
    DLQ_DIR.mkdir(parents=True, exist_ok=True)

    sources = find_recent_reports(hours=args.hours)
    registry = load_registry()
    stamp = now_stamp()
    run_stats = {"received": len(sources), "processed": 0, "duplicate": 0, "error": 0, "dlq": 0}
    cards: list[Path] = []
    bot_cards: list[Path] = []
    insights: list[dict] = []
    for src in sources:
        rel = src.relative_to(ROOT).as_posix()
        src_stat = src.stat()
        src_mtime = datetime.fromtimestamp(src_stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        src_hash = file_sha1(src)
        record_key = f"{rel}|{src_stat.st_size}|{int(src_stat.st_mtime)}|{src_hash[:12]}"

        existing = registry.get(record_key)
        if existing:
            if args.refresh_duplicates:
                try:
                    card, bot_card, insight = make_card(src)
                    cards.append(card)
                    bot_cards.append(bot_card)
                    insights.append(insight)
                    existing["status"] = "refreshed"
                    existing["last_seen_at"] = stamp
                    existing["last_processed_at"] = stamp
                    existing["card_path"] = card.relative_to(ROOT).as_posix()
                    existing["bot_card_path"] = bot_card.relative_to(ROOT).as_posix()
                    existing["error"] = ""
                    run_stats["processed"] += 1
                except Exception as exc:  # pragma: no cover
                    existing["status"] = "error"
                    existing["last_seen_at"] = stamp
                    existing["error"] = str(exc)
                    run_stats["error"] += 1
            else:
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
            "dlq_path": "",
            "error": "",
        }

        try:
            card, bot_card, insight = make_card(src)
            cards.append(card)
            bot_cards.append(bot_card)
            insights.append(insight)
            row["status"] = "processed"
            row["last_processed_at"] = stamp
            row["card_path"] = card.relative_to(ROOT).as_posix()
            row["bot_card_path"] = bot_card.relative_to(ROOT).as_posix()
            run_stats["processed"] += 1
        except Exception as exc:  # pragma: no cover
            row["status"] = "error"
            row["error"] = str(exc)[:500]
            row["dlq_path"] = append_dlq_entry(src, record_key, row["error"])
            run_stats["error"] += 1
            run_stats["dlq"] += 1

        registry[record_key] = row

    save_registry(registry)
    if not insights and args.replay_latest_cards > 0:
        insights = replay_insights_from_registry(registry, limit=args.replay_latest_cards)

    build_latest_summary(cards, bot_cards, args.hours, run_stats)
    build_decision_queue(insights, run_stats, args.manual_run)
    print(
        f"[warehouse] sources={len(sources)} cards={len(set(cards))} "
        f"bot_cards={len(set(bot_cards))} duplicates={run_stats['duplicate']} "
        f"errors={run_stats['error']} summary={LATEST_REPORT} registry={REGISTRY_FILE}"
    )

    if args.send_telegram:
        if (not cards) and (not args.telegram_on_empty):
            print("[warehouse] telegram=skip:no-new-cards")
            return 0
        text = telegram_text(cards, args.hours, run_stats, insights, args.manual_run)
        ok, info = send_telegram_message(text)
        print(f"[warehouse] telegram={info}")
        if not ok:
            # Не валим пайплайн из-за Telegram; фиксируем как warning.
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
