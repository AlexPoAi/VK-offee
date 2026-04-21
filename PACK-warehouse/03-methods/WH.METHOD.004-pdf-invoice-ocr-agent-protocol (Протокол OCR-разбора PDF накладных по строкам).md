---
type: method
id: WH.METHOD.004
created: 2026-04-20
updated: 2026-04-20
owner: Engineer
status: active
---

# WH.METHOD.004 — Протокол OCR-разбора PDF накладных по строкам

## Цель

Сделать из `PDF` не просто текст, а структурированный закупочный источник.

## Канонический исполнитель

`Warehouse PDF Invoice OCR Analyst`

## Что он обязан делать

1. Открыть PDF накладную.
2. Определить тип документа:
- `text PDF`
- `scanned PDF`
3. Для `text PDF` сначала извлечь текст/таблицы без OCR.
4. Для `scanned PDF` использовать OCR-слой.
5. Разбить документ на строки накладной.
4. Найти:
- поставщика
- дату
- номер накладной
- итоговую сумму
- позиции по строкам

5. Для каждой строки извлечь:
- raw line
- SKU / наименование
- qty
- unit
- unit price
- line total
- confidence

6. Нормализовать строку:
- привести наименование к каноническому SKU
- связать с supplier type
- связать с supplier card

7. Если confidence низкий:
- не придумывать,
- вынести в `manual review`

## Обязательный каскад метода

### Ветвь A — text PDF

- сначала text extraction;
- затем table/line extraction;
- затем регуляризация числовых колонок;
- затем нормализация SKU.

### Ветвь B — scanned PDF

- rasterize page;
- preprocess image;
- OCR с confidence;
- line segmentation;
- нормализация строки и чисел.

### Ветвь C — evidence merge

После extraction:
- supplier/date/invoice number должны жить отдельно от line items;
- line items должны хранить raw text и normalized representation;
- любые спорные позиции должны иметь manual-review reason.

## Обязательные артефакты

- `invoice-ocr-ledger.csv`
- `invoice-price-delta-report.md`
- `invoice-manual-review.md`
- matched/unmatched SKU ledger
- supplier/date extraction evidence

## Использование результата

Результат этого метода должен идти дальше в:
- supplier cards
- закупочный контур
- manager report кладовщика
- ABC/pricing cross-check, если в периоде есть weekly ABC

## Чего нельзя делать

- нельзя ограничиваться preview text
- нельзя считать OCR удачным, если нет line-item extraction
- нельзя смешивать спорные позиции с подтверждёнными
- нельзя скрывать OCR uncertainty
- нельзя подменять machine-readable PDF OCR-веткой по умолчанию, если text/table extraction даёт более чистый результат
