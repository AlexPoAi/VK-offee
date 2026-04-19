# PACK-warehouse (Склад и остатки)

> Домен складского учета, инвентаризации, поставщиков и накладных.

## Назначение
Хранение карточек товаров, остатков, накладных от поставщиков для возможности поиска ботом ответов на вопросы типа "какой остаток у товара X" или "какие накладные были от поставщика Y".

## Структура
- `01-domain-contract/` — контракты домена
- `02-domain-entities/` — сущности (карточки товаров, накладные, поставщики, report-cards)
- `03-methods/` — доменные скиллы и операционные методы обработки
- `04-work-products/` — рабочие продукты (интеграция данных и аналитика)
- `tools/` — автоматизация складского контура (pipeline карточек и Telegram-отчётов)

## Автоконтур склада

### Google Drive — структура папок
```
Складские отчёты (1oo1j86l7hGZ-E1HIbAApc3PdCA3o80GX)
├── Новое       (1LcTqSJ7n8bl70Ifk0crcL2dYKp3qhL92) <- Жанна кладёт сюда
└── Обработано  (1pHugGbDKpyXqAvGjULiNIMOl64vCc29V) <- скрипт перемещает
```

### Режим: ручной запуск
Склад обрабатывается по команде пользователя, НЕ автоматически.
Триггер: Жанна прислала отчёт -> пользователь говорит агенту «обнови склад».

### Pipeline
1. `sync-google-sheets.py` скачивает файлы из папки «Новое» в `knowledge-base/`
2. `warehouse_reports_pipeline.py`:
   - создаёт карточку на каждый отчёт (остатки, ABC, инвентаризация)
   - ведёт реестр `WH.REGISTRY.001-documents.csv`
   - ABC-анализ: парсит категории A/B/C и кросс-сверяет с остатками
   - отправляет аналитический Telegram-отчёт с рекомендациями
   - проблемные файлы -> quarantine `03-quarantine/dlq-files/`
3. После обработки файлы перемещаются из «Новое» в «Обработано»

> Текущий статус: автоматический шаг `Обработано -> Архив` пока не внедрён (в roadmap).

### Запуск
```bash
cd ~/Github/VK-offee && bash PACK-warehouse/tools/warehouse_full_loop.sh
```

### Env-переменные
- `WAREHOUSE_DRIVE_FOLDER_ID` — папка «Новое»
- `WAREHOUSE_DRIVE_PROCESSED_FOLDER_ID` — папка «Обработано»
- `WAREHOUSE_REPORT_BASE_URL` — GitHub URL для кликабельных ссылок
- `WAREHOUSE_REPORT_CHAT_ID` / `TELEGRAM_CHAT_ID` — Telegram chat

### Ключевые рабочие продукты
- `WH.REPORT.002-warehouse-sync-summary-latest.md` — сводка последнего цикла
- `WH.SESSION.001-decision-queue-latest.md` — очередь управленческих сессий
- `WH.REQUEST.001-zhanna-data-supply-contract.md` — контракт данных (что догружаем от Жанны)
- `WH.WP.005-manager-report-structure-and-warehouse-agent-operating-protocol-2026-04-19 (Структура управленческого отчёта и протокол работы кладовщика).md` — канон структуры управленческого отчёта
- `WH.WP.006-warehouse-full-cycle-architecture-2026-04-19 (...)` — E2E архитектура цикла кладовщика и reporting contract

### Ключевые сущности
- `WH.SUPPLIER.001-directory.md` — справочник поставщиков и типов продукции
- `WH.WP.006-warehouse-full-cycle-architecture-2026-04-19 (Архитектура полного цикла кладовщика: document flow, processing, reporting contract).md` — полная архитектура E2E-цикла кладовщика

### Ключевые методы
- `WH.METHOD.001-zhanna-biweekly-intake-and-processing-skill (...)` — intake/обработка biweekly пакета Жанны
- `WH.METHOD.002-report-first-manager-digest-skill (...)` — report-first протокол перед отправкой digest

### Ключевой контракт домена
- `01-domain-contract/WH.CONTRACT.001-warehouse-intake-processing-reporting-contract.md` — обязательный контракт этапов intake, обработки и руководительской отчётности
