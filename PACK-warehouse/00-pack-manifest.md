# PACK-warehouse (Склад и остатки)

> Домен складского учета, инвентаризации, поставщиков и накладных.

## Назначение
Хранение карточек товаров, остатков, накладных от поставщиков для возможности поиска ботом ответов на вопросы типа "какой остаток у товара X" или "какие накладные были от поставщика Y".

## Структура
- `01-domain-contract/` — контракты домена
- `02-domain-entities/` — сущности (карточки товаров, накладные, поставщики, report-cards)
- `04-work-products/` — рабочие продукты (интеграция данных и аналитика)
- `tools/` — автоматизация складского контура (pipeline карточек и Telegram-отчётов)

## Автоконтур склада
1. `sync-google-sheets.py` подтягивает данные из Google Drive папки для бота в `knowledge-base/`.
2. `PACK-warehouse/tools/warehouse_reports_pipeline.py`:
   - создает карточку на каждый свежий складской отчет,
   - обновляет сводный отчет склада,
   - ведёт реестр документов `PACK-warehouse/04-work-products/WH.REGISTRY.001-documents.csv` со статусами `new/processed/duplicate/error`,
   - отправляет проблемные файлы в quarantine `PACK-warehouse/03-quarantine/dlq-files/` и пишет `WH.DLQ.001-quarantine-report.md`,
   - публикует зеркальные карточки в `knowledge-base/Отчёты для бота/Склад` (доступно RAG/Telegram-боту),
   - отправляет краткий Telegram-отчет.
3. Регулярный запуск full-loop:
   - `PACK-warehouse/tools/warehouse_full_loop.sh` (entrypoint `sync -> cards -> telegram`);
   - `PACK-warehouse/tools/com.vkoffee.warehouse-full-loop.plist` (шаблон launchd, каждые 30 минут).

## Telegram env fallback
- `WAREHOUSE_REPORT_CHAT_ID` (приоритетный chat для складского отчета),
- `TELEGRAM_CHAT_ID`,
- fallback на `~/.config/aist/env` и `~/.config/exocortex/telegram-chat-id`.
