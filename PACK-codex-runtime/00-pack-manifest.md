---
type: pack-manifest
pack_id: PACK-codex-runtime
title: Codex Runtime и агентный диалоговый контур
version: 0.1
created: 2026-04-21
domain: VK-offee
prefix: CODEX
fpf_edition: local VK-offee FPF/SRT stack
status: draft
---

# PACK-codex-runtime — Codex Runtime и агентный диалоговый контур

## Назначение

Паспорт домена для отдельного контра работы `Codex` внутри экосистемы `VK-offee`.

Этот Pack нужен для того, чтобы Telegram-диалог с агентом, intake задач,
контекст сессий, артефакты ответов и transport-layer не растворялись
между RAG-ботом, локальным Codex и разовыми файлами.

> **Почему этот Pack нужен:** `Telegram` сам по себе не является доменом.
> Доменом является практика приёма задач, ведения агентных сессий,
> хранения контекста и выдачи результатов через разные transport-каналы.

## Bounded Context

### Что входит в этот Pack

- приём входящих задач для `Codex` через Telegram и другие transport-каналы;
- управление агентными сессиями;
- хранение краткой памяти и state-снимков по сессиям;
- хранение артефактов ответа: текстов, изображений, документов, ссылок;
- маршрутизация между inbox, обработкой и outbox;
- runtime-контракт между Telegram-ботом, локальным Codex и cloud/VPS worker.

### Что не входит в этот Pack

- RAG-поиск по базе знаний `VK-offee` как предметная функция бота;
- предметные домены кофейни: бар, кухня, сервис, парк, дизайн;
- инженерный ремонт всей экосистемы целиком
  (→ `DS-strategy/PACK-exocortex-engineering`);
- общий Telegram notification layer экзокортекса вне контекста Codex-сессий.

## Практики и участники домена

### Primary practitioners

- `User` — ставит задачу и продолжает сессию;
- `Codex Agent` — исполняет задачу и ведёт ответ;
- `Transport Bot` — принимает/отправляет сообщения и файлы;
- `Session Operator` — поддерживает связность сессий и маршрутов.

### Excluded practitioners

- `RAG Search User` как отдельный предметный пользователь базы знаний;
- `Store Staff` в их операционных ролях бариста/официант/повар;
- `Environment Engineer` вне задач Codex-runtime.

## FPF Dependencies

| FPF distinction | Как используется |
|-----------------|------------------|
| method vs tool | Telegram — инструмент, а не домен и не метод |
| role vs person | `User`, `Codex Agent`, `Transport Bot`, `Session Operator` описываются как роли |
| work product vs description | session-card, task-card, context snapshot и outbox-entry считаются WP |
| system vs environment | runtime-контур отделяется от предметной базы знаний |

## Связи

| Pack / Репо | Связь |
|-------------|-------|
| `VK-offee/telegram-bot` | Входной и выходной transport для Codex-сессий |
| `VK-offee/PACK-design` | Один из downstream-потребителей Codex-задач и артефактов |
| `DS-strategy/PACK-exocortex-engineering` | Соседний инженерный домен runtime и transport-слоя |
| `FMT-exocortex-template` | Скрипты отправки и orchestration transport-каналов |

## Структура

| Папка | Содержимое |
|-------|-----------|
| `01-concepts/` | Domain selection, runtime model, transport boundaries |
| `02-domain-entities/` | Роли, объекты внимания, индексы методов и инструментов |
| `03-methods/` | Intake, session routing, context snapshot, reply loop |
| `04-work-products/` | Реестры сессий, pilot-работы, rollout-артефакты |
| `05-failure-modes/` | Типовые сбои: context drift, wrong routing, silent drop |

## Статус

`draft` — домен выделен и описан, но transport/runtime loop ещё не доведён до боевого 24/7 acceptance.

## Domain Entry Documents

- [DOMAIN-DESCRIPTION.md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/DOMAIN-DESCRIPTION.md)
- [DOCUMENT-REGISTRY.md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/DOCUMENT-REGISTRY.md)

---

*Создан: 2026-04-21. Версия: 0.1.*
