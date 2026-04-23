---
type: checklist
id: WH.CHECKLIST.001
created: 2026-04-23
updated: 2026-04-23
owner: Warehouse Demand Analyst
status: active
---

# WH.CHECKLIST.001 — Прогресс доведения кладовщика до сильного доменного агента

## Архитектура агента

- [x] Есть один основной агент склада: `Warehouse Demand Analyst / Кладовщик VK Coffee`
- [x] `ABC`, `PDF`, intake, supplier routing оформлены как internal capability слои, а не как случайные куски логики
- [ ] Есть завершённая mini knowledge base по складу: supplier facts, SKU rules, reorder rules, cost facts

## Intake и чтение документов

- [x] `csv/xlsx` читаются стабильно и без ложного truncation
- [x] `ABC` входит в production pipeline
- [x] `PDF` накладные читаются до line-item слоя
- [ ] OCR / extraction coverage по PDF доведён до устойчивого production качества
- [ ] Для каждого типа документа есть quality gate и понятный fallback path

## Decision chain

- [x] low-stock слой больше не обрезается искусственно до первых нескольких SKU
- [x] есть `family-level ABC fallback`
- [x] supplier routing стал materially лучше и убран блок `Уточнить у Жанны` из manager layer
- [ ] supplier routing полностью подтверждён для `UNICAVA`
- [ ] supplier routing полностью подтверждён для `Субмарина`
- [ ] supplier routing полностью подтверждён для остальных спорных SKU

## Price / cost layer

- [x] из PDF-накладных строится блок `Изменение цен`
- [x] аномальные `price delta` выводятся в `Проверить вручную`
- [x] materialized отдельный supporting artifact по себестоимости и валовой марже: `WH.REPORT.003`
- [ ] price-layer калиброван для manager-ready качества
- [x] есть первый живой слой `cost / margin cards`
- [ ] есть связка `закупочная цена -> цена продажи -> базовая маржа`

## Manager report

- [x] отчёт говорит языком решений, а не списком файлов
- [x] supplier order blocks собраны по поставщику
- [x] Telegram работает как доставщик, а не как источник логики
- [ ] есть стабильный `document -> fields -> metrics -> manager output` contract для всех типов документов
- [ ] есть category-aware compression для крупных supplier-order blocks
- [ ] есть полностью manager-ready шаблон заявки поставщику по каждому активному поставщику

## Document-to-decision map

- [ ] `ABC-анализ` формально описан: что читаем, что считаем, что показываем руководителю
- [ ] `Остатки` формально описаны: что читаем, что считаем, что показываем руководителю
- [ ] `Накладные PDF` формально описаны: что читаем, что считаем, что показываем руководителю
- [ ] `Каталог` формально описан: что читаем, что считаем, что показываем руководителю
- [ ] `Продажи / выручка` формально описаны: что читаем, что считаем, что показываем руководителю

## Truthful next focus

1. Убрать из `ABC/cost` manager-layer модификаторы и внутренние полуслужебные SKU вроде `Молоко / 50 гр`, если они не должны жить в руководительском слое.
2. Finish supplier channels for `UNICAVA` and `Субмарина`.
3. Дожать связку `закупочная цена -> цена продажи -> базовая маржа`.
