---
type: domain-entity
pack_id: PACK-codex-runtime
title: Шаблон task-card
status: draft
created: 2026-04-21
prefix: CODEX.ENTITY.006
---

# CODEX.ENTITY.006 — Шаблон task-card

## Назначение

`task-card` — каноническая карточка отдельного входящего хода или задачи внутри `Codex Runtime`.

## Шаблон

```md
---
type: task-card
task_id: CODEX.TASK.###
session_id: CODEX.SESSION.###
kind: task
channel: telegram
source_message_id: ""
status: accepted
created_at: YYYY-MM-DD HH:MM:SS
updated_at: YYYY-MM-DD HH:MM:SS
owner_role: Codex Agent
---

# Task `CODEX.TASK.###`

## Вход

Оригинальная формулировка задачи или краткий faithful digest.

## Attachments

- имя файла / ссылка

## Domain Routing

- какие Pack или point-level domains затронуты

## Processing State

- `accepted`
- `queued`
- `in_progress`
- `waiting-user`
- `done`

## Result

Короткая truthful-сводка результата или текущего статуса.
```

## Виды задач

- `task`
- `design`
- `follow-up`
- `artifact-only`

## Инвариант

Ни одна входящая задача не должна существовать вне `task-card`.
