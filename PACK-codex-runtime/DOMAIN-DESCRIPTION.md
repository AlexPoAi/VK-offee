---
type: domain-description
pack_id: PACK-codex-runtime
title: Описание домена Codex Runtime
status: draft
created: 2026-04-21
updated: 2026-04-21
prefix: CODEX.DOMAIN.001
---

# Описание домена `PACK-codex-runtime`

## Что это за домен

`PACK-codex-runtime` — это домен про отдельный агентный контур `Codex`
внутри экосистемы `VK-offee`.

Это не домен про Telegram как мессенджер и не домен про RAG-поиск по базе знаний.
Это домен про:
- приём задач;
- ведение session;
- хранение контекста;
- хранение и выдачу артефактов;
- связку между transport-каналом, агентом и ответом пользователю.

Иными словами: это домен про **рабочую память и операционный контур агентного диалога**.

## Что входит в домен

- intake задач для `Codex` из Telegram и других transport-каналов;
- session management;
- task cards;
- context snapshots;
- artifact storage;
- outbox и truthful delivery state;
- привязка `chat/message/thread -> session/task`;
- runtime-контракт между VPS-ботом, локальным Codex и future cloud-worker.

## Что не входит в домен

- обычный RAG-режим `VK-offee` бота;
- база знаний кофейни как предметное содержимое;
- Pack-домены `bar`, `kitchen`, `service`, `design`, `park-development`;
- общий notification layer экзокортекса вне контекста Codex-session;
- инженерные работы по всей экосистеме как отдельный домен.

## Основные роли

- `User`
- `Codex Agent`
- `Transport Bot`
- `Session Operator`

## Основные объекты внимания

- `Session`
- `Task`
- `Context Snapshot`
- `Artifact`
- `Transport Binding`
- `Outbox Entry`

## Source-of-truth внутри домена

Главные документы домена на текущем этапе:

- [00-pack-manifest.md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/00-pack-manifest.md)
- [CODEX.CONCEPT.001-domain-selection-statement (Выбор домена Codex Runtime).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/01-concepts/CODEX.CONCEPT.001-domain-selection-statement%20%28%D0%92%D1%8B%D0%B1%D0%BE%D1%80%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%20Codex%20Runtime%29.md)
- [CODEX.CONCEPT.002-storage-contract (Контракт хранения session-task-outbox).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/01-concepts/CODEX.CONCEPT.002-storage-contract%20%28%D0%9A%D0%BE%D0%BD%D1%82%D1%80%D0%B0%D0%BA%D1%82%20%D1%85%D1%80%D0%B0%D0%BD%D0%B5%D0%BD%D0%B8%D1%8F%20session-task-outbox%29.md)
- [CODEX.METHOD.001-telegram-codex-intake (Приём задач из Telegram в Codex Runtime).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/03-methods/CODEX.METHOD.001-telegram-codex-intake%20%28%D0%9F%D1%80%D0%B8%D1%91%D0%BC%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%D0%B8%D0%B7%20Telegram%20%D0%B2%20Codex%20Runtime%29.md)
- [DOCUMENT-REGISTRY.md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/DOCUMENT-REGISTRY.md)

## Правило пополнения домена

Любой новый документ, артефакт, session contract, method card, runtime note
или rollout-результат сначала должен быть:

1. materialized как отдельный документ или файл;
2. внесён в [DOCUMENT-REGISTRY.md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/DOCUMENT-REGISTRY.md);
3. только после этого считаться частью домена.

Без записи в реестр документ не считается частью source-of-truth.
