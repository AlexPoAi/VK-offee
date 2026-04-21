---
type: domain-entity
pack_id: PACK-codex-runtime
title: Шаблон session-card
status: draft
created: 2026-04-21
prefix: CODEX.ENTITY.005
---

# CODEX.ENTITY.005 — Шаблон session-card

## Назначение

`session-card` — каноническая карточка одной живой сессии пользователя в контуре `Codex Runtime`.

## Шаблон

```md
---
type: session-card
session_id: CODEX.SESSION.### 
channel: telegram
chat_id: ""
thread_key: ""
status: active
opened_at: YYYY-MM-DD HH:MM:SS
last_activity_at: YYYY-MM-DD HH:MM:SS
active_task_id: ""
owner_role: Session Operator
---

# Session `CODEX.SESSION.###`

## Назначение

Короткое описание, что это за ветка работы.

## Контекст

- кто инициатор;
- какая основная цель;
- какие домены уже затронуты;
- какие ограничения важны.

## Active Tasks

- `CODEX.TASK.###`

## Related Artifacts

- путь/ссылка на связанные файлы

## Current State

- `accepted` / `in_progress` / `waiting-user` / `closed`

## Last Truthful Summary

Короткая актуальная сводка состояния сессии.
```

## Обязательные поля

- `session_id`
- `channel`
- `chat_id`
- `status`
- `opened_at`
- `last_activity_at`

## Инвариант

Каждая `task-card` должна ссылаться на существующую `session-card`.
