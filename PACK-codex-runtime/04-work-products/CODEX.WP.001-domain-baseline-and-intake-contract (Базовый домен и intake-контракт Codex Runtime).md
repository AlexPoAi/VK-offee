---
type: work-product
pack_id: PACK-codex-runtime
title: Базовый домен и intake-контракт Codex Runtime
status: draft
created: 2026-04-21
prefix: CODEX.WP.001
---

# CODEX.WP.001 — Базовый домен и intake-контракт Codex Runtime

## Что сделано

В рамках первого baseline-slice материализован отдельный домен `Codex Runtime`:

1. Зафиксирован `Domain Selection Statement`.
2. Создан `00-pack-manifest` с bounded context.
3. Описаны роли и объекты внимания домена.
4. Заведены индексы методов и инструментов.
5. Зафиксирован storage contract `session/task/outbox`.
6. Описан первый канонический метод intake из Telegram.

## Что это даёт

- новый `Codex`-контур можно строить отдельно от RAG;
- transport, session и context получают общую модель данных;
- rollout кнопки `🤖 Codex` можно делать безопасно и поэтапно.

## Следующий slice

1. Добавить `CODEX.METHOD.002` для session binding и mode switching.
2. Материализовать папки `runtime/sessions`, `runtime/tasks`, `runtime/outbox`.
3. Внедрить в Telegram-боте отдельную кнопку `🤖 Codex` без поломки текущего RAG-mode.
