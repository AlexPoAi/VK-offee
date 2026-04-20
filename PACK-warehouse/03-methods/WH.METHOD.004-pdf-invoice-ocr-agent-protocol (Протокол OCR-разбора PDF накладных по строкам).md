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
2. Извлечь текст OCR-слоем.
3. Разбить документ на строки накладной.
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

## Обязательные артефакты

- `invoice-ocr-ledger.csv`
- `invoice-price-delta-report.md`
- `invoice-manual-review.md`

## Использование результата

Результат этого метода должен идти дальше в:
- supplier cards
- закупочный контур
- manager report кладовщика

## Чего нельзя делать

- нельзя ограничиваться preview text
- нельзя считать OCR удачным, если нет line-item extraction
- нельзя смешивать спорные позиции с подтверждёнными
- нельзя скрывать OCR uncertainty
