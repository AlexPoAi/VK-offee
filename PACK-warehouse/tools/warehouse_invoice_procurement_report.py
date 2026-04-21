#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


ROOT = repo_root()
KB_DIR = ROOT / "knowledge-base"
WP_DIR = ROOT / "PACK-warehouse" / "04-work-products"
SUPPLIER_DIR = ROOT / "PACK-warehouse" / "02-domain-entities" / "WH.SUPPLIER.001-directory.md"
SUPPLIER_CARDS_DIR = ROOT / "PACK-warehouse" / "02-domain-entities" / "suppliers"
OUT_FILE = WP_DIR / "WH.WP.007-invoice-procurement-supplier-map-2026-04-19 (Карта поставщиков и закупочный контур по PDF-накладным).md"
SUPPLIER_INDEX_FILE = ROOT / "PACK-warehouse" / "02-domain-entities" / "WH.SUPPLIER.CARDS.INDEX.md"


@dataclass
class InvoiceItem:
    code: str
    name: str
    qty: float
    price: float
    amount: float
    product_type: str


@dataclass
class InvoiceRecord:
    source_file: str
    invoice_no: str
    invoice_date: str
    seller: str
    seller_inn: str
    buyer_address: str
    total: float
    items: list[InvoiceItem]


PRODUCT_RULES: list[tuple[str, str]] = [
    ("drip", "кофе_drip"),
    ("дрип", "кофе_drip"),
    ("зерно", "кофе_зерно"),
    ("кофе", "кофе_зерно"),
    ("чай", "чай"),
    ("шоколад", "шоколад"),
    ("какао", "шоколад"),
    ("сироп", "сиропы"),
    ("сок", "напитки"),
    ("нектар", "напитки"),
    ("вода", "напитки"),
    ("лимонад", "напитки"),
    ("десерт", "десерты"),
    ("чиабат", "кухня"),
    ("сырник", "кухня"),
    ("блин", "кухня"),
    ("боул", "кухня"),
    ("ролл", "кухня"),
    ("онигурадзу", "кухня"),
    ("рис", "кухня"),
    ("крышка", "расходники"),
    ("стакан", "расходники"),
    ("салфет", "расходники"),
    ("перчат", "расходники"),
    ("пакет", "расходники"),
    ("трубоч", "расходники"),
    ("антисептик", "хозтовары"),
    ("белизна", "хозтовары"),
]


SUPPLIER_HINTS: list[tuple[str, str]] = [
    ("тейсти кофе", "кофе_зерно"),
    ("tasty coffee", "кофе_зерно"),
    ("unicava", "шоколад"),
    ("барсервис", "сиропы"),
    ("шипилов", "расходники"),
    ("камелот", "напитки"),
    ("премиум-сегмент", "напитки"),
    ("ритейл проперти", "напитки"),
    ("новая жизнь", "другое"),
    ("мфуд", "кухня"),
    ("умами", "кухня"),
    ("кухня вкусный кофе", "кухня"),
    ("дмитрий", "десерты"),
    ("смакотерия", "десерты"),
    ("пряники", "десерты"),
]


CONTACT_HINTS: list[tuple[str, dict[str, str]]] = [
    (
        "дмитрий",
        {
            "contact_person": "Дмитрий",
            "phone": "+7 978 745 61-05",
            "telegram": "TBD",
            "whatsapp": "TBD",
            "email": "TBD",
            "supplier_contact": "+7 978 745 61-05",
            "order_channel": "Viber (лс)",
            "source_of_contact": "Баристский справочник поставщиков: Поставщики информация 2.0.xlsx -> Десерты и моти (Дмитрий)",
        },
    ),
    (
        "мфуд",
        {
            "contact_person": "TBD",
            "phone": "7 978 742 99-16",
            "telegram": "TBD",
            "whatsapp": "7 978 742 99-16",
            "email": "TBD",
            "supplier_contact": "7 978 742 99-16",
            "order_channel": "WhatsApp (лс)",
            "source_of_contact": "Баристский справочник поставщиков: Поставщики информация 2.0.xlsx -> Мфуд",
        },
    ),
    (
        "барсервис",
        {
            "contact_person": "Наталья",
            "phone": "+7 978 023 04-05",
            "telegram": "TBD",
            "whatsapp": "+7 978 023 04-05",
            "email": "TBD",
            "supplier_contact": "+7 978 023 04-05",
            "order_channel": "WhatsApp (лс)",
            "source_of_contact": "Баристский справочник поставщиков: Поставщики информация 2.0.xlsx -> Сиропы (Наталья); матч по категории сиропов",
        },
    ),
    (
        "камелот",
        {
            "contact_person": "Эмиль",
            "phone": "+7 978 818 04-06",
            "telegram": "TBD",
            "whatsapp": "+7 978 818 04-06",
            "email": "TBD",
            "supplier_contact": "+7 978 818 04-06",
            "order_channel": "WhatsApp (чат «Заказ сок Вико»)",
            "source_of_contact": "Баристский справочник поставщиков: Поставщики информация 2.0.xlsx -> Сок Вико (Эмиль); матч по напиткам/сокам",
        },
    ),
    (
        "кухня вкусный кофе",
        {
            "contact_person": "Александр",
            "phone": "TBD",
            "telegram": "чат в telegram \"кухня ВКУСНЫЙ КОФЕ\"",
            "whatsapp": "TBD",
            "email": "TBD",
            "supplier_contact": "чат в telegram \"кухня ВКУСНЫЙ КОФЕ\"",
            "order_channel": "Telegram chat",
            "source_of_contact": "Баристский справочник поставщиков: Поставщики информация 2.0.xlsx -> Кухня ВКУСНЫЙ КОФЕ",
        },
    ),
]


def money_to_float(raw: str) -> float:
    return float(raw.replace("\u00a0", "").replace(" ", "").replace(",", "."))


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def clean_item_label(text: str) -> str:
    value = normalize_ws(text)
    value = re.sub(r"^(?:1а\s+1б\s+2\s+2а\s+3\s+4\s+5\s+6\s+7\s+8\s+9\s+10\s+10а\s+11\s+)?", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^[A-ZА-Я0-9\"«»._/-]+\s+\d+\s+", "", value)
    value = re.sub(r"\s+-\s+\d+.*$", "", value)
    return value[:90].strip(" ,.-") or value[:90]


def normalize_invoice_item_name(text: str) -> str:
    value = normalize_ws(text)
    # В распознанном тексте УПД часто прилипает шапка колонок "1а 1б 2 2а ... 11"
    # перед кодом и названием товара. Для price-ledger и supplier cards этот шум вреден.
    value = re.sub(
        r"^(?:1а\s+1б\s+2\s+2а\s+3\s+4\s+5\s+6\s+7\s+8\s+9\s+10\s+10а\s+11\s+)+",
        "",
        value,
        flags=re.IGNORECASE,
    )
    value = re.sub(r"^[A-ZА-Я0-9._/-]{2,}\s+1\s+", "", value)
    value = re.sub(r"^[A-ZА-Я0-9._/-]{2,}\s+", "", value)
    value = re.sub(r"\s{2,}", " ", value).strip(" ,.-")
    return value or normalize_ws(text)


def slugify(text: str) -> str:
    value = text.lower()
    value = re.sub(r"[^a-zа-я0-9]+", "-", value, flags=re.IGNORECASE)
    return value.strip("-") or "supplier"


def parse_ru_date(raw: str) -> datetime | None:
    raw = normalize_ws(raw)
    months = {
        "января": "01",
        "февраля": "02",
        "марта": "03",
        "апреля": "04",
        "мая": "05",
        "июня": "06",
        "июля": "07",
        "августа": "08",
        "сентября": "09",
        "октября": "10",
        "ноября": "11",
        "декабря": "12",
    }
    word_date = re.search(r"(\d{1,2})\s+([а-я]+)\s+(\d{4})", raw.lower())
    if word_date and word_date.group(2) in months:
        raw = f"{int(word_date.group(1)):02d}.{months[word_date.group(2)]}.{word_date.group(3)}"
    for fmt in ("%d.%m.%Y", "%d.%m.%y"):
        try:
            return datetime.strptime(raw, fmt)
        except ValueError:
            continue
    return None


def canonical_supplier_name(seller: str) -> str:
    seller_low = normalize_ws(seller).lower()
    if "барсервис" in seller_low:
        return "Барсервис"
    if "мфуд" in seller_low:
        return "МФУД"
    if "тейсти кофе" in seller_low or "тэйсти кофе" in seller_low or "tasty coffee" in seller_low:
        return "Тэйсти Кофе"
    if "unicava" in seller_low:
        return "UNICAVA"
    if "шипилов" in seller_low:
        return "ИП Шипилов Сергей Николаевич"
    if "камелот" in seller_low:
        return "КАМЕЛОТ"
    if "ритейл проперти 6" in seller_low:
        return "Ритейл Проперти 6"
    if "премиум-сегмент" in seller_low:
        return "Премиум-Сегмент"
    if "новая жизнь" in seller_low:
        return "Новая Жизнь"
    return normalize_ws(seller)


def contact_details_for_supplier(seller: str) -> dict[str, str]:
    seller_low = seller.lower()
    defaults = {
        "contact_person": "TBD",
        "phone": "TBD",
        "telegram": "TBD",
        "whatsapp": "TBD",
        "email": "TBD",
        "supplier_contact": "TBD",
        "order_channel": "TBD",
        "source_of_contact": "TBD (нужно подтвердить у Жанны / в Google Drive)",
    }
    for needle, payload in CONTACT_HINTS:
        if needle in seller_low:
            defaults.update(payload)
            break
    return defaults


def extract_text(pdf: Path) -> str:
    return subprocess.check_output(["pdftotext", "-layout", str(pdf), "-"], text=True)


def canonical_pdf_key(pdf: Path) -> str:
    name = pdf.name.lower()
    while name.endswith(".pdf"):
        name = name[:-4]
    return name.strip()


def split_invoices(text: str) -> list[str]:
    parts = re.split(r"(?=передаточный\s+Счет-фактура №)", text, flags=re.IGNORECASE)
    return [p for p in parts if "Счет-фактура №" in p]


def classify_product_type(name: str, seller: str) -> str:
    seller_low = seller.lower()
    for needle, product_type in SUPPLIER_HINTS:
        if needle in seller_low:
            return product_type
    hay = f"{seller} {name}".lower()
    for needle, product_type in PRODUCT_RULES:
        if needle in hay:
            return product_type
    return "другое"


def parse_items(block: str, seller: str) -> list[InvoiceItem]:
    section_match = re.search(r"Наименование товара.*?Всего к оплате", block, flags=re.S)
    if not section_match:
        return []
    section = section_match.group(0)
    pattern = re.compile(
        r"^\s*(?P<code>\S+)\s+(?P<idx>\d+)\s+(?P<name>.+?)\s+-\s+\d+\s+\S+\s+"
        r"(?P<qty>\d+(?:[.,]\d+)?)\s+(?P<price>\d[\d \u00a0]*[.,]\d{2})\s+"
        r"(?P<amount>\d[\d \u00a0]*[.,]\d{2})",
        flags=re.M | re.S,
    )
    items: list[InvoiceItem] = []
    for match in pattern.finditer(section):
        name = normalize_invoice_item_name(match.group("name"))
        qty = money_to_float(match.group("qty"))
        price = money_to_float(match.group("price"))
        amount = money_to_float(match.group("amount"))
        if len(name) < 3:
            continue
        items.append(
            InvoiceItem(
                code=match.group("code"),
                name=name,
                qty=qty,
                price=price,
                amount=amount,
                product_type=classify_product_type(name, seller),
            )
        )
    return items


def parse_invoice(block: str, source_file: str) -> InvoiceRecord | None:
    no_date = re.search(r"Счет-фактура №\s*([^\s]+)\s+от\s+([^\n]+)", block)
    seller = re.search(r"Продавец\s+(.+)", block)
    inn = re.search(r"ИНН/КПП продавца\s+([^\n]+)", block)
    buyer = re.search(r"Грузополучатель и его адрес:\s+(.+)", block)
    total = re.search(r"Всего к оплате\s+([\d \u00a0]+[.,]\d{2})", block)
    if not (no_date and seller and total):
        return None

    seller_name = canonical_supplier_name(re.sub(r"\(\d+\)\s*$", "", seller.group(1)))
    invoice_date = normalize_ws(re.sub(r"\s+\(.*$", "", no_date.group(2)))
    items = parse_items(block, seller_name)
    return InvoiceRecord(
        source_file=source_file,
        invoice_no=no_date.group(1).strip(),
        invoice_date=invoice_date,
        seller=seller_name,
        seller_inn=normalize_ws(inn.group(1)) if inn else "n/a",
        buyer_address=normalize_ws(buyer.group(1)) if buyer else "n/a",
        total=money_to_float(total.group(1)),
        items=items,
    )


def collect_invoice_records() -> list[InvoiceRecord]:
    pdfs = sorted(KB_DIR.rglob("*Накладные*.pdf"))
    unique_pdfs: list[Path] = []
    seen_keys: set[str] = set()
    for pdf in pdfs:
        key = canonical_pdf_key(pdf)
        if key in seen_keys:
            continue
        seen_keys.add(key)
        unique_pdfs.append(pdf)
    records: list[InvoiceRecord] = []
    for pdf in unique_pdfs:
        text = extract_text(pdf)
        for block in split_invoices(text):
            record = parse_invoice(block, pdf.relative_to(ROOT).as_posix())
            if record:
                records.append(record)
    return records


def build_report(records: list[InvoiceRecord]) -> str:
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    by_supplier: dict[str, list[InvoiceRecord]] = defaultdict(list)
    by_type: dict[str, list[tuple[str, InvoiceItem]]] = defaultdict(list)
    for rec in records:
        by_supplier[rec.seller].append(rec)
        for item in rec.items:
            by_type[item.product_type].append((rec.seller, item))

    supplier_rows: list[str] = []
    for seller, recs in sorted(by_supplier.items()):
        item_count = sum(len(r.items) for r in recs)
        total_amount = sum(r.total for r in recs)
        avg_invoice = total_amount / len(recs) if recs else 0.0
        parsed_dates = [dt for dt in (parse_ru_date(r.invoice_date) for r in recs) if dt is not None]
        last_invoice_dt = max(parsed_dates) if parsed_dates else None
        last_invoice = last_invoice_dt.strftime("%d.%m.%Y") if last_invoice_dt else "n/a"
        sample_types = sorted({item.product_type for r in recs for item in r.items})
        supplier_rows.append(
            f"| {seller} | {len(recs)} | {item_count} | {total_amount:,.2f} | {avg_invoice:,.2f} | {last_invoice} | {', '.join(sample_types[:4]) or 'n/a'} |".replace(",", " ")
        )

    procurement_rows: list[str] = []
    preferred_types = ["кофе_зерно", "кофе_drip", "чай", "шоколад", "сиропы", "напитки", "десерты", "кухня", "расходники", "хозтовары"]
    for product_type in preferred_types:
        rows = by_type.get(product_type, [])
        if not rows:
            continue
        qty_total = sum(item.qty for _, item in rows)
        amount_total = sum(item.amount for _, item in rows)
        top_suppliers = sorted({seller for seller, _ in rows})
        sample_items = ", ".join(item.name for _, item in rows[:3])
        procurement_rows.append(
            f"| {product_type} | {', '.join(top_suppliers[:3])} | {qty_total:,.2f} | {amount_total:,.2f} | {sample_items[:140]} |".replace(",", " ")
        )

    missing_links = []
    for must_have in ("кофе_зерно", "кофе_drip", "чай"):
        if must_have not in by_type:
            missing_links.append(f"- В текущих PDF-накладных не найден устойчивый поставщик для категории `{must_have}`. Нужно либо догрузить накладные этого поставщика, либо руками завести supplier mapping.")

    lines = [
        "---",
        "type: work-product",
        "id: WH.WP.007",
        f"generated: {generated_at}",
        "---",
        "",
        "# WH.WP.007 — Карта поставщиков и закупочный контур по PDF-накладным",
        "",
        "## Что сделано",
        "- Разобраны PDF-накладные из папки `knowledge-base/Отчёты для бота/Накладные`.",
        "- Выделены реальные поставщики, счета-фактуры, суммы и товарные группы.",
        "- Построен первый supplier map для закупочного отчёта.",
        "",
        "## Executive Summary",
        f"- Всего накладных документов: **{len(records)}**",
        f"- Уникальных поставщиков: **{len(by_supplier)}**",
        f"- Товарных групп в факте: **{len(by_type)}**",
        "- Главный результат: по PDF уже можно строить закупочный контур `тип товара -> поставщик -> ассортимент -> сумма закупки`.",
        "",
        "## Поставщики из факта",
        "| Поставщик | Документов | Позиций | Оборот, руб | Средний чек, руб | Последняя закупка | Типы продукции |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    lines.extend(supplier_rows or ["| n/a | 0 | 0 | 0.00 | n/a |"])
    lines.extend(
        [
            "",
            "## Закупочный контур по типам продукции",
            "| Тип продукции | Поставщики | Объем, факт | Сумма, руб | Примеры позиций |",
            "|---|---|---:|---:|---|",
        ]
    )
    lines.extend(procurement_rows or ["| n/a | n/a | 0.00 | 0.00 | n/a |"])
    lines.extend(
        [
            "",
            "## Улучшение твоей модели за счет реального факта",
            "- `Шоколад UNICAVA` уже подтвержден как отдельный поставщик категории `шоколад`.",
            "- `Барсервис` подтвержден как поставщик категории `сиропы`.",
            "- `ИП Шипилов Сергей Николаевич` подтвержден как поставщик `расходников/упаковки`.",
            "- `ООО КАМЕЛОТ` и `ООО Премиум-сегмент / Ритейл Проперти 6` идут как `напитки/retail`.",
            "- `МФУД`, `Умами`, `Кухня ВКУСНЫЙ КОФЕ`, `Дмитрий (Десерты)`, `Смакотерия` формируют кухонно-десертный контур.",
            "",
            "## Что ещё не хватает до идеального procurement-report",
        ]
    )
    lines.extend(missing_links or ["- Не хватает автоматического связывания low-stock SKU из остатков с конкретной строкой накладной поставщика."])
    lines.extend(
        [
            "- В накладных обычно нет прямого `контакта для заказа`, поэтому нужен отдельный supplier directory с телефоном/Telegram/WhatsApp.",
            "- Нужен `lead time` по поставщику: сегодня из PDF видно дату документа, но не норму срока поставки.",
            "- Нужен `par level / reorder point` по SKU, чтобы отчёт говорил не просто `что мало`, а `сколько заказать`.",
            "",
            "## Что делать дальше в реализации",
            "1. Автоматически обновлять `WH.SUPPLIER.001-directory.md` из факта накладных.",
            "2. Связать позиции low-stock из остатков с типами продукции и supplier map.",
            "3. Ввести поля `order_deadline`, `delivery_eta`, `why_now`, `risk_if_no_action` в финальный закупочный отчёт.",
            "4. Дозагрузить накладные/справочник по кофе и чаю, если их нет в текущем пакете PDF.",
            "",
            "## Источники",
        ]
    )
    for rec in records[:20]:
        lines.append(f"- `{rec.source_file}` -> `{rec.seller}` / № `{rec.invoice_no}` / `{rec.invoice_date}` / `{rec.total:,.2f} руб`".replace(",", " "))
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    records = collect_invoice_records()
    WP_DIR.mkdir(parents=True, exist_ok=True)
    SUPPLIER_CARDS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(build_report(records), encoding="utf-8")
    write_supplier_cards(records)
    print(OUT_FILE)
    print(f"records={len(records)} suppliers={len({r.seller for r in records})}")
    return 0


def write_supplier_cards(records: list[InvoiceRecord]) -> None:
    by_supplier: dict[str, list[InvoiceRecord]] = defaultdict(list)
    for rec in records:
        by_supplier[rec.seller].append(rec)

    index_lines = [
        "---",
        "type: supplier-index",
        f"updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "---",
        "",
        "# Актуальные supplier cards",
        "",
        "| Поставщик | Карточка |",
        "|---|---|",
    ]

    for seller, recs in sorted(by_supplier.items()):
        item_names = []
        seen_items = set()
        product_types = set()
        total_amount = 0.0
        for rec in recs:
            total_amount += rec.total
            for item in rec.items:
                product_types.add(item.product_type)
                cleaned = clean_item_label(item.name)
                if cleaned not in seen_items and len(item_names) < 8:
                    seen_items.add(cleaned)
                    item_names.append(cleaned)

        invoice_count = len(recs)
        avg_invoice = total_amount / invoice_count if invoice_count else 0.0
        parsed_dates = [dt for dt in (parse_ru_date(r.invoice_date) for r in recs) if dt is not None]
        last_invoice_dt = max(parsed_dates) if parsed_dates else None
        last_invoice = last_invoice_dt.strftime("%d.%m.%Y") if last_invoice_dt else "TBD"
        legal_entity = recs[0].seller
        seller_inn = recs[0].seller_inn
        source_files = sorted({r.source_file for r in recs})
        contacts = contact_details_for_supplier(seller)

        lines = [
            "---",
            "type: supplier-card",
            f"supplier: {seller}",
            f"updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "status: active",
            "---",
            "",
            f"# Supplier Card — {seller}",
            "",
            "## Executive Summary",
            f"- Поставщик подтверждён по накладным: **да**",
            f"- Оборот за период: **{f'{total_amount:,.2f}'.replace(',', ' ')} руб**",
            f"- Последняя закупка: **{last_invoice}**",
            f"- Основная категория: **{', '.join(sorted(product_types)) or 'TBD'}**",
            "",
            "## Карточка",
            "| Поле | Значение |",
            "|---|---|",
            f"| Поставщик | {seller} |",
            f"| Юрлицо | {legal_entity} |",
            f"| ИНН/КПП | {seller_inn} |",
            f"| Категория | {', '.join(sorted(product_types)) or 'TBD'} |",
            f"| Последняя закупка | {last_invoice} |",
            f"| Оборот периода | {f'{total_amount:,.2f}'.replace(',', ' ')} руб |",
            "",
            "## Контакты",
            "| Канал | Значение |",
            "|---|---|",
            f"| Контактное лицо | {contacts['contact_person']} |",
            f"| Телефон | {contacts['phone']} |",
            f"| Telegram | {contacts['telegram']} |",
            f"| WhatsApp | {contacts['whatsapp']} |",
            f"| Email | {contacts['email']} |",
            f"| Основной канал заказа | {contacts['order_channel']} |",
            f"| Источник контакта | {contacts['source_of_contact']} |",
            "",
            "## Закупочный профиль",
            "| Поле | Значение |",
            "|---|---|",
            "| Cutoff для заказа | TBD |",
            "| Типичный lead time | TBD |",
            "| Статус контакта | частично подтверждён / требует дозаполнения |",
            "",
            "### Ключевые позиции",
        ]
        lines.extend(f"- {item}" for item in item_names or ["TBD"])
        lines.extend(
            [
                "",
                "## Метрики периода",
                "| Метрика | Значение |",
                "|---|---:|",
                f"| Оборот за период | {f'{total_amount:,.2f}'.replace(',', ' ')} руб |",
                f"| Количество накладных | {invoice_count} |",
                f"| Средний чек | {f'{avg_invoice:,.2f}'.replace(',', ' ')} руб |",
                f"| Последняя закупка | {last_invoice} |",
                "",
                "## Источники",
            ]
        )
        lines.extend(f"- `{path}`" for path in source_files[:10])
        lines.extend(
            [
                "",
                "## Заметки для руководителя",
                "- Карточка создана автоматически из PDF-накладных и supplier-справочника.",
                "- Если контакт не заполнен, значит он пока не подтверждён надёжным источником.",
            ]
        )
        filename = f"WH.SUPPLIER.CARD.{slugify(seller)}.md"
        (SUPPLIER_CARDS_DIR / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")
        index_lines.append(f"| {seller} | `02-domain-entities/suppliers/{filename}` |")

    SUPPLIER_INDEX_FILE.write_text("\n".join(index_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
