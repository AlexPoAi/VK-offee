---
type: warehouse-production-readiness-verdict
id: WH.WP.009
date: 2026-04-26
owner: Warehouse Demand Analyst
wp: WP-63
status: partial-ready
---

# WH.WP.009 — Production readiness verdict по складскому контуру

## Итоговый verdict

**Verdict: `partial-ready`.**

Складской контур уже можно считать рабочим для регулярного manager-report и ручного управленческого цикла:

- документы регистрируются в `WH.REGISTRY.001`;
- битые или пустые источники попадают в DLQ/quarantine;
- повторный прогон не плодит карточки как новые решения, а фиксирует дубликаты;
- manager-report, decision queue, supplier cards, ABC/cost layer и PDF procurement layer материализуются;
- VPS timer `vk-warehouse-full-loop.timer` активен и последние циклы завершаются без hard-fail.

Но контур ещё нельзя честно назвать полностью production-ready, потому что подтверждённый VPS evidence сейчас покрывает в основном стабильный пустой цикл, а не полный цикл с новым входящим файлом от Жанны.

## Evidence на 2026-04-26

### Локальный manual-run

Команда:

```bash
python3 VK-offee/PACK-warehouse/tools/warehouse_reports_pipeline.py --hours 720 --manual-run
```

Результат:

- `sources=57`
- `cards=5`
- `bot_cards=5`
- `duplicates=52`
- `errors=0`
- procurement refresh: `ok`
- suppliers in procurement layer: `15`
- invoice/procurement records: `134`

Обновлены:

- `WH.REPORT.002-warehouse-sync-summary-latest.md`
- `WH.REPORT.003-cost-margin-signals-latest.md`
- `WH.SESSION.001-decision-queue-latest.md`
- `WH.REGISTRY.001-documents.csv`
- `WH.WP.007-invoice-procurement-supplier-map-2026-04-19`

### VPS evidence

Проверка VPS `72.56.4.61`:

- `vk-warehouse-full-loop.timer`: `active`
- последний service run: `status=0/SUCCESS`
- последние циклы идут каждые 30 минут;
- Google auth в последнем логе успешен;
- intake folder сейчас даёт `0` таблиц и `0` файлов;
- pipeline на VPS завершает цикл с `errors=0`;
- Telegram не шлётся при пустом цикле: `telegram=skip:no-new-cards`.

Важная оговорка: `sync.error.log` на VPS не обновлялся с `2026-04-19`; ошибки в нём являются старым хвостом, а не свежим падением.

## Acceptance по WP-63

| Критерий | Verdict | Evidence |
|---|---|---|
| `WH.REGISTRY` по входящим и обработанным документам | pass | `WH.REGISTRY.001-documents.csv`, свежий manual-run |
| DLQ/quarantine для ошибочных файлов | pass | `WH.DLQ.001-quarantine-report.md`, `03-quarantine/dlq-files/` |
| Идемпотентность без дублей карточек и ложных отчётов | pass | свежий manual-run: `duplicates=52`, `errors=0` |
| Google Drive архитектура закреплена как контракт | partial | `WH.CONTRACT.001`, но VPS loop пока смотрит в intake-only folder |
| Telegram health-report | partial | ручной/пустой цикл корректно skip-ит Telegram, но свежий non-empty боевой digest не подтверждён |
| 2-3 стабильных production cycles подряд | partial-pass | VPS timer стабилен на пустых циклах; новый входящий файл не проверен |
| Хронология изменений отражена в DS-инженерном контуре | pass | `ENGINEERING-CHRONOLOGY`, `WeekPlan`, `SESSION-CONTEXT` |

## Что уже можно использовать

1. Открывать `WH.REPORT.002` как текущий manager-report по складу.
2. Использовать `WH.SESSION.001` как список решений: срочные заказы, ручные проверки, ассортиментные решения.
3. Смотреть supplier cards как карту поставщиков и закупочного контура.
4. Считать registry/DLQ/idempotency слой достаточно устойчивым для дальнейших bounded итераций.

## Что нельзя обещать

1. Нельзя обещать, что новый файл от Жанны на VPS пройдет полный путь `intake -> processing -> processed-folder -> Telegram` без ручной проверки.
2. Нельзя считать supplier routing закрытым: у `UNICAVA` и `Субмарина` ещё нет подтверждённых каналов заказа.
3. Нельзя считать PDF price-ledger полным: накладные уже дают price delta, но coverage и качество extraction нужно усиливать.
4. Нельзя считать unit economics чистой: `ABC -> cost` работает, но `ABC -> полноценная товарная экономика` ещё требует modifier policy и связки с каталогом/накладными.

## Следующий bounded tail

Открывать не новый широкий складской проект, а один узкий production-tail:

1. выровнять VPS `warehouse_full_loop.sh` с локальным контрактом root-folder sync + intake move;
2. проверить новый тестовый входящий файл в `Новые документы`;
3. подтвердить move в `Обработано`;
4. подтвердить non-empty Telegram digest;
5. после этого повысить verdict с `partial-ready` до `ready`.

## Production-tail update: вход 24.04 утро

После выпуска verdict пользователь передал новый Google input:

- `1SFblPiukm69YrPI5ocgLQm50Odtj0cCE`
- тема: зерно и чай `Тэйсти`, `Бункер`, `Субмарина`
- папка: `Отчёты для бота -> Новые документы`

Результат:

- Google auth локально прошёл;
- общий Drive sync нашёл root-папку, но оборвался на file-search timeout/BrokenPipe;
- файл скачан напрямую по ссылке и положен в локальный intake;
- warehouse pipeline успешно обработал его как non-empty input:
  - `sources=58`
  - `processed=1`
  - `duplicates=57`
  - `errors=0`
- создан отдельный manager-readable артефакт: `WH.WP.010-tasty-bunker-submarine-stock-2026-04-24.md`.

Verdict после этого: контур подтвердил **локальный non-empty intake -> card -> manager-report -> decision queue**. До полного `ready` всё ещё не хватает автоматического Google Drive move в `Обработано` и подтверждения non-empty Telegram digest.

## Закрытие WP-63

`WP-63` можно закрывать как **verdict-issued / partial-ready**, потому что исходный production-hardening слой материализован и итоговый operational verdict выпущен.

Оставшийся хвост не должен размывать `WP-63`; его нужно вести как отдельный bounded production-tail, если требуется довести именно VPS full-intake acceptance до `ready`.
