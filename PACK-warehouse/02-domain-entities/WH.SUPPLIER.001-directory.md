---
type: domain-entity
id: WH.SUPPLIER.001
created: 2026-04-19
updated: 2026-04-19
status: active
---

# WH.SUPPLIER.001 — Справочник поставщиков и типов продукции

## Назначение
Единый справочник `кто поставляет какой тип товара`, чтобы в отчёте сразу было:
- что заканчивается,
- у кого заказать,
- по какому контакту,
- до какого дедлайна.

## Формат записи (обязательные поля)
- `supplier_name`
- `supplier_legal_entity`
- `supplier_contact`
- `product_types`
- `items_examples`
- `order_channel` (телефон/whatsapp/telegram/email)
- `order_cutoff_time` (до какого времени принимают заказ)
- `typical_lead_time_days`
- `notes`

## Таблица поставщиков (заполняется из накладных + подтверждается менеджером)

| supplier_name | supplier_legal_entity | supplier_contact | product_types | items_examples | order_channel | order_cutoff_time | typical_lead_time_days | notes |
|---|---|---|---|---|---|---|---|---|
| Testi Coffee | TBD | TBD | кофе_зерно, кофе_drip, чай | зерно 250г/1кг, drip, чай | TBD | TBD | TBD | Подтвердить фактом из накладных |
| Unica | TBD | TBD | шоколад | белый/тёмный шоколад, какао | TBD | TBD | TBD | Подтвердить фактом из накладных |

## Правило обновления
1. После каждого цикла накладных агент проверяет новые поставки.
2. Если найден новый поставщик или новый тип товара — добавляет строку.
3. Если в накладной нет контакта/юр.лица — ставит `TBD` и добавляет задачу на уточнение.
