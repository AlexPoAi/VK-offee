# DOCUMENT-REGISTRY — PACK-management

> Базовый реестр ключевых документов и карточек домена `PACK-management`.

## Как читать

- `Оригинал` — физический источник, если он существует отдельно.
- `Карточка` — markdown-описание, которое агент читает первым.
- `Статус`:
  - `ok` — артефакт materialized и пригоден для работы;
  - `draft` — контур существует, но ещё требует развития;
  - `active` — активный рабочий продукт / актуальный слой истины.

## Доменные контракты и манифесты

| ID | Тема | Оригинал | Карточка | Статус |
|---|---|---|---|---|
| MGMT.MANIFEST.001 | Pack manifest управления кофейней | — | `00-pack-manifest.md` | ok |
| MGMT.MANIFEST.002 | Краткий manifest домена | — | `MANIFEST.md` | ok |
| MGMT.CONTRACT.001 | Объектная модель PACK-management v1 | — | `01-domain-contract (Контракт домена)/DOMAIN-MODEL-v1 (Объектная модель PACK-management v1).md` | ok |

## Роли

| ID | Тема | Оригинал | Карточка | Статус |
|---|---|---|---|---|
| MGMT.ROLE.001 | Управляющий кофейней | — | `02-domain-entities (Сущности домена)/MGMT.ROLE.001-cafe-manager (Роль управляющего кофейней).md` | active |

## Рабочие продукты

| ID | Тема | Оригинал | Карточка | Статус |
|---|---|---|---|---|
| MGMT.WP.001 | История разработки AI-агентов | — | `04-work-products (Рабочие продукты)/MGMT.WP.001-ai-agent-development-history.md` | draft |
| MGMT.WP.015 | Счёт-фактура ИП Шмилов | внешний документ | `04-work-products (Рабочие продукты)/MGMT.WP.015-invoice-shmilov-2026-03-02 (Счет-фактура ИП Шмилов).md` | ok |
| MGMT.WP.016 | Счёт-фактура Мёуд | внешний документ | `04-work-products (Рабочие продукты)/MGMT.WP.016-invoice-meud-2026-03-02 (Счет-фактура Мёуд).md` | ok |
| MGMT.WP.017 | Отчёт по продажам март 2026 | внешний отчёт | `04-work-products (Рабочие продукты)/MGMT.WP.017-sales-report-march-2026 (Отчёт по продажам март 2026).md` | ok |
| MGMT.WP.018 | FPF-SRT-SPF pass по PACK-management и роли управляющего кофейней | — | `04-work-products (Рабочие продукты)/MGMT.WP.018-management-domain-fpf-srt-spf-pass (FPF-SRT-SPF pass по PACK-management и роли управляющего кофейней).md` | active |

## Обучающие материалы и управленческие SOP

| ID | Тема | Оригинал | Карточка | Статус |
|---|---|---|---|---|
| MGMT.TRAIN.001 | Складской учет / Отчетность: скринкаст `Отчет по продажам` | [Google Drive](https://drive.google.com/file/d/1naXmYDz1Yj5iOpGvil7WwuIDzUcUnRQD/view?usp=drivesdk) | `03-methods (Методы)/MGMT.TRAIN.001-sales-report-screencast (Скринкаст Отчет по продажам).md` | active |
| MGMT.TRAIN.002 | Складской учет / Отчетность: скринкаст `Выгрузка Каталога` | [Google Drive](https://drive.google.com/file/d/1P5UKOkwj9HZCvKIq_9ZvgTdJLvogSSFl/view?usp=drivesdk) | `03-methods (Методы)/MGMT.TRAIN.002-catalog-export-screencast (Скринкаст Выгрузка Каталога).md` | active |
| MGMT.TRAIN.003 | Складской учет / Отчетность: скринкаст `Выручка` | [Google Drive](https://drive.google.com/file/d/1q_W2Kr2587m-Nmhv_w-Hk9k5aRyD4lZX/view?usp=drivesdk) | `03-methods (Методы)/MGMT.TRAIN.003-revenue-screencast (Скринкаст Выручка).md` | active |

### Placement note

Эти скринкасты определены в `PACK-management` как primary management/training layer, потому что они нужны:

- руководителю как резервному исполнителю роли менеджера;
- новому управляющему / операционному менеджеру при передаче дел;
- для контроля, что управленческая отчётность не держится только на устной памяти Жанны.

Secondary echo допустим позже:

- в `PACK-warehouse`, если из скринкаста делается складской SOP;
- в Saby/runtime-контуре, если из скринкаста делается техническая инструкция по выгрузке.

## Следующий слой доработки

1. Добавить project-timeline или management-timeline, когда в домене накопится больше factual updates.
2. Отдельно выделить управленческие factual cards по `repair / readiness / relocation / launch`.
3. Уточнить, какие legacy management-артефакты остаются актуальными, а какие уже только исторические.
4. Для `MGMT.TRAIN.001-003` сделать короткие markdown-конспекты/SOP, чтобы руководитель или новый менеджер могли выполнить процесс без пересмотра полного скринкаста.
