---
type: document-registry
pack_id: PACK-codex-runtime
title: Реестр документов домена Codex Runtime
status: active
owner: Session Operator
created: 2026-04-21
updated: 2026-04-21
prefix: CODEX.REGISTRY.001
---

# DOCUMENT-REGISTRY — `PACK-codex-runtime`

## Назначение

Единый реестр документов и артефактов домена `Codex Runtime`.

Этот реестр нужен, чтобы:
- видеть source-of-truth по домену;
- не терять новые входящие документы;
- понимать, что уже materialized, а что пока нет;
- поддерживать единый вход в домен при возврате к работе.

## Правило домена

Любой новый документ или артефакт в `PACK-codex-runtime` должен проходить через этот реестр.

Минимальный ритуал:
1. создать документ;
2. присвоить ему роль в контуре;
3. внести запись в этот реестр;
4. только после этого использовать его как source-of-truth.

## Главный source-of-truth

- [DOMAIN-DESCRIPTION.md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/DOMAIN-DESCRIPTION.md)
- [00-pack-manifest.md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/00-pack-manifest.md)

## Реестр артефактов

| Документ | Тип | Статус | Роль в контуре |
|---|---|---|---|
| [DOMAIN-DESCRIPTION.md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/DOMAIN-DESCRIPTION.md) | `domain-description` | draft | краткая входная карта домена |
| [00-pack-manifest.md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/00-pack-manifest.md) | `pack-manifest` | draft | bounded context и границы домена |
| [CODEX.CONCEPT.001-domain-selection-statement (Выбор домена Codex Runtime).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/01-concepts/CODEX.CONCEPT.001-domain-selection-statement%20%28%D0%92%D1%8B%D0%B1%D0%BE%D1%80%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%20Codex%20Runtime%29.md) | `domain-selection` | draft | формализация Stage 01 |
| [CODEX.CONCEPT.002-storage-contract (Контракт хранения session-task-outbox).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/01-concepts/CODEX.CONCEPT.002-storage-contract%20%28%D0%9A%D0%BE%D0%BD%D1%82%D1%80%D0%B0%D0%BA%D1%82%20%D1%85%D1%80%D0%B0%D0%BD%D0%B5%D0%BD%D0%B8%D1%8F%20session-task-outbox%29.md) | `storage-contract` | draft | модель хранения session/task/outbox |
| [CODEX.ENTITY.001-roles (Роли домена Codex Runtime).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/02-domain-entities/CODEX.ENTITY.001-roles%20%28%D0%A0%D0%BE%D0%BB%D0%B8%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%20Codex%20Runtime%29.md) | `domain-entity` | draft | роли домена |
| [CODEX.ENTITY.002-objects-of-attention (Объекты внимания домена Codex Runtime).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/02-domain-entities/CODEX.ENTITY.002-objects-of-attention%20%28%D0%9E%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D1%8B%20%D0%B2%D0%BD%D0%B8%D0%BC%D0%B0%D0%BD%D0%B8%D1%8F%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%20Codex%20Runtime%29.md) | `domain-entity` | draft | объекты внимания домена |
| [CODEX.ENTITY.003-methods-index (Индекс методов домена Codex Runtime).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/02-domain-entities/CODEX.ENTITY.003-methods-index%20%28%D0%98%D0%BD%D0%B4%D0%B5%D0%BA%D1%81%20%D0%BC%D0%B5%D1%82%D0%BE%D0%B4%D0%BE%D0%B2%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%20Codex%20Runtime%29.md) | `methods-index` | draft | карта методов домена |
| [CODEX.ENTITY.004-tools-index (Индекс инструментов домена Codex Runtime).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/02-domain-entities/CODEX.ENTITY.004-tools-index%20%28%D0%98%D0%BD%D0%B4%D0%B5%D0%BA%D1%81%20%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%BE%D0%B2%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%20Codex%20Runtime%29.md) | `tools-index` | draft | карта runtime-инструментов |
| [CODEX.ENTITY.005-session-card-template (Шаблон session-card).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/02-domain-entities/CODEX.ENTITY.005-session-card-template%20%28%D0%A8%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%20session-card%29.md) | `card-template` | draft | канонический шаблон session-card |
| [CODEX.ENTITY.006-task-card-template (Шаблон task-card).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/02-domain-entities/CODEX.ENTITY.006-task-card-template%20%28%D0%A8%D0%B0%D0%B1%D0%BB%D0%BE%D0%BD%20task-card%29.md) | `card-template` | draft | канонический шаблон task-card |
| [CODEX.METHOD.001-telegram-codex-intake (Приём задач из Telegram в Codex Runtime).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/03-methods/CODEX.METHOD.001-telegram-codex-intake%20%28%D0%9F%D1%80%D0%B8%D1%91%D0%BC%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%D0%B8%D0%B7%20Telegram%20%D0%B2%20Codex%20Runtime%29.md) | `method` | draft | intake-контур из Telegram |
| [CODEX.METHOD.002-session-binding-and-card-materialization (Привязка session и материализация карточек).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/03-methods/CODEX.METHOD.002-session-binding-and-card-materialization%20%28%D0%9F%D1%80%D0%B8%D0%B2%D1%8F%D0%B7%D0%BA%D0%B0%20session%20%D0%B8%20%D0%BC%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%D0%BA%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%B5%D0%BA%29.md) | `method` | draft | materialization слоя session/task |
| [CODEX.WP.000-runtime-registry (Реестр работ и артефактов Codex Runtime).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/04-work-products/CODEX.WP.000-runtime-registry%20%28%D0%A0%D0%B5%D0%B5%D1%81%D1%82%D1%80%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%20%D0%B8%20%D0%B0%D1%80%D1%82%D0%B5%D1%84%D0%B0%D0%BA%D1%82%D0%BE%D0%B2%20Codex%20Runtime%29.md) | `work-product-registry` | active | living registry WP и rollout-срезов |
| [CODEX.WP.001-domain-baseline-and-intake-contract (Базовый домен и intake-контракт Codex Runtime).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/04-work-products/CODEX.WP.001-domain-baseline-and-intake-contract%20%28%D0%91%D0%B0%D0%B7%D0%BE%D0%B2%D1%8B%D0%B9%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%20%D0%B8%20intake-%D0%BA%D0%BE%D0%BD%D1%82%D1%80%D0%B0%D0%BA%D1%82%20Codex%20Runtime%29.md) | `work-product` | draft | baseline-slice домена |
| [CODEX.WP.003-bot-codex-mode-first-slice (Первый slice режима Codex в Telegram-боте).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/04-work-products/CODEX.WP.003-bot-codex-mode-first-slice%20%28%D0%9F%D0%B5%D1%80%D0%B2%D1%8B%D0%B9%20slice%20%D1%80%D0%B5%D0%B6%D0%B8%D0%BC%D0%B0%20Codex%20%D0%B2%20Telegram-%D0%B1%D0%BE%D1%82%D0%B5%29.md) | `work-product` | draft | первый безопасный slice интеграции `Codex mode` |
| [runtime/README.md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/runtime/README.md) | `runtime-storage-map` | draft | карта живого runtime-хранилища |

## Incoming Queue Rule

Будущие входящие должны добавляться в реестр по одному из типов:

- `session-card`
- `task-card`
- `artifact`
- `context-snapshot`
- `outbox-entry`
- `runtime-note`
- `rollout-result`

## Чего ещё не хватает

1. Реестр `telegram-thread -> session`
2. Отдельный метод mode-switching `RAG -> Codex`
3. Первый pilot rollout кнопки `🤖 Codex`
4. Первый живой `session-card` и `task-card` из реального Telegram intake
