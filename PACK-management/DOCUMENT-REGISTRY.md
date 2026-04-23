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

## Следующий слой доработки

1. Добавить project-timeline или management-timeline, когда в домене накопится больше factual updates.
2. Отдельно выделить управленческие factual cards по `repair / readiness / relocation / launch`.
3. Уточнить, какие legacy management-артефакты остаются актуальными, а какие уже только исторические.
