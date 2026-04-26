---
type: warehouse-live-input-analysis
id: WH.WP.010
date: 2026-04-26
source_date: 2026-04-24 morning
owner: Warehouse Demand Analyst
status: active
---

# WH.WP.010 — Зерно и чай Тэйсти / Бункер / Субмарина, вход 24.04 утро

## Источник

- Google input: `1SFblPiukm69YrPI5ocgLQm50Odtj0cCE`
- Локальный intake: `knowledge-base/Отчёты для бота/Новые документы/Остатки по складам зерно и чай Тэйсти Бункер Субмарина 24.04.2026.xlsx`
- Warehouse card: `PACK-warehouse/02-domain-entities/report-cards/WH.CARD.остатки-по-складам-зерно-и-чай-тэйсти-бункер-субмарина-24-04-2026-725f7b9c.md`
- Bot card: `knowledge-base/Отчёты для бота/Склад/WH.BOT.остатки-по-складам-зерно-и-чай-тэйсти-бункер-субмарина-24-04-2026-725f7b9c.md`

## Pipeline result

Fresh manual run:

```bash
python3 VK-offee/PACK-warehouse/tools/warehouse_reports_pipeline.py --hours 720 --manual-run
```

Result:

- `sources=58`
- `processed=1`
- `duplicates=57`
- `errors=0`
- latest manager report updated: `2026-04-26 19:37`

Important note: direct Google Drive sync saw the folder but timed out during full file search, so the linked XLSX was downloaded directly and placed into local intake. Pipeline processing itself is successful.

## Stock picture

| Категория | SKU | Общий остаток | Луговая | Тургенева | Самокиша |
|---|---:|---:|---:|---:|---:|
| Зерно бункер | 1 | 89.601 кг | 5.199 кг | 80.917 кг | 3.485 кг |
| Дрипы | 26 | 90 шт | 23 | 48 | 19 |
| Зерно 1 кг | 18 | 180 шт | 32 | 102 | 46 |
| Зерно фильтр 250 гр | 9 | 87 шт | 17 | 27 | 43 |
| Зерно эспрессо 250 гр | 15 | 215 шт | 36 | 89 | 90 |
| Субмарина 250 гр / 1 кг | 1 | 2 шт | 2 | 0 | 0 |
| Субмарина дрипы | 9 | 32 шт | 7 | 17 | 8 |
| Чай 100 гр Tasty | 14 | 95 шт | 20 | 39 | 36 |

## Manager verdict

The new input is actionable. It narrows the order focus to:

- `Тэйсти Кофе`: drips, зерно, чай;
- `Субмарина`: drips and one 200 гр position;
- `Бункер`: current bulk bean stock is high overall, but Samokisha has only `3.485 кг`.

Current warehouse manager report:

- critical SKU: `30`
- planned replenishment SKU: `0`
- suppliers in cycle: `2`
- ABC for this isolated input: unavailable, so decisions are stock-driven.

## Critical stock <= 1

### Тэйсти Кофе

- `Дрип Бэрри 10 шт` — total `1`, Тургенева `1`
- `Дрип Кения маунт (10 шт)` — total `1`, Тургенева `1`
- `Дрип Эфиопия Мукера 120 часов / 10 шт` — total `1`, Луговая `1`
- `Дрип Эфиопия Сидамо 50 шт` — total `1`, Луговая `1`
- `Дрип Эфиопия Сидамо (10 шт)` — total `1`, Тургенева `1`
- `Коста Рика Сан Хосе 1 кг` — total `1`, Луговая `1`
- `Фрутти 1кг` — total `1`, Тургенева `1`
- `Компетишн Колумбия Гейша Хардинес Дель Эден 100 гр` — total `1`, Самокиша `1`
- `Чай Молочный улун 100 гр` — total `1`, Самокиша `1`
- `Чай Черная смородина 100 гр` — total `1`, Самокиша `1`

### Субмарина

- `Субмарина МЕГА ДРИПЫ Бразилия Перископ Мармелада` — total `1`, Луговая `1`

## Low stock <= 3

### Субмарина

- `Субмарина Бразилия Перископ Мармелада 200 гр` — total `2`, Луговая `2`
- `Субмарина МЕГА ДРИПЫ Бразилия Перископ Мармелада` — total `1`, Луговая `1`
- `Субмарина МЕГА ДРИПЫ Эфиопия Челбеса` — total `2`, Тургенева `2`
- `Субмарина Набор дрипов №24 / 16 шт` — total `2`, Тургенева `1`, Самокиша `1`

### Тэйсти Кофе

- `Дрип Боливия Каранави 10 шт` — total `2`
- `Дрип Бэрри (30 шт)` — total `3`
- `Дрип Бэрри 10 шт` — total `1`
- `Дрип Кения маунт (10 шт)` — total `1`
- `Дрип Кения Маунт 30шт` — total `2`
- `Дрип Колумбия Декаф 50 шт` — total `2`
- `Дрип Колумбия Декаф (30 шт)` — total `2`
- `Дрип микс (Подарочный набор)` — total `3`
- `Дрип Руанда Киву 10 шт` — total `3`
- `Дрип Эфиопия Мукера 120 часов / 10 шт` — total `1`
- `Дрип Эфиопия Мукера 200 часов / 10 шт` — total `2`
- `Дрип Эфиопия Сидамо 50 шт` — total `1`
- `Дрип Эфиопия Сидамо (10 шт)` — total `1`
- `Дрип Эфиопия Сидамо 30шт` — total `3`
- `Дрип-пакеты Коста-Рика 2025, 12 шт` — total `2`
- `Колумбия Декаф 1кг` — total `2`
- `Коста Рика Сан Хосе 1 кг` — total `1`
- `Руанда Кигали 1кг` — total `2`
- `Фрутти 1кг` — total `1`
- `Компетишн Колумбия Гейша Хардинес Дель Эден 100 гр` — total `1`
- `Руанда Киву 250 гр` — total `2`
- `Чай Женьшень улун 100 гр` — total `3`
- `Чай Молочный улун 100 гр` — total `1`
- `Чай Рухуна 250 гр / НА БАР` — total `3`
- `Чай Тегуанинь 100 гр` — total `2`
- `Чай Черная смородина 100 гр` — total `1`

## Ready order draft from decision queue

### Субмарина

Здравствуйте. Хотим оформить заказ по поставщику Субмарина:

1. Субмарина Мега Дрипы Бразилия Перископ Мармелада — 9 шт.

Просьба подтвердить наличие, цену и ближайшую дату отгрузки.

### Тэйсти Кофе

Здравствуйте. Хотим оформить заказ по поставщику Тэйсти Кофе:

1. Дрип Бэрри 10 Шт — 9 шт.
2. Дрип Кения Маунт (10 Шт) — 9 шт.
3. Дрип Эфиопия Мукера 120 Часов / 10 Шт — 9 шт.
4. Дрип Эфиопия Сидамо (10 Шт) — 9 шт.
5. Дрип Эфиопия Сидамо 50 Шт — 9 шт.
6. Компетишн Колумбия Гейша Хардинес Дель Эден 100 Гр — 9 шт.
7. Коста Рика Сан Хосе 1 Кг — 9 шт.

Просьба подтвердить наличие, цену и ближайшую дату отгрузки.

Контакт в контуре: `8 (800) 500-41-70 / sales@tastycoffee.ru`

## Data gaps

- `Субмарина` channel is still unconfirmed.
- This input is stock-only; no sales/ABC context was loaded with it, so order priority is stock-driven.
- Current standard parser does not fully understand category header + units format; this artifact is the truthful manager-readable interpretation for the 24.04 input.
