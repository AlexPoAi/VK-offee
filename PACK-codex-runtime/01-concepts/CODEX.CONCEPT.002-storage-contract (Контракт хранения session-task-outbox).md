---
type: concept
pack_id: PACK-codex-runtime
title: Контракт хранения session-task-outbox
status: draft
created: 2026-04-21
prefix: CODEX.CONCEPT.002
---

# CODEX.CONCEPT.002 — Контракт хранения session-task-outbox

## Назначение

Зафиксировать минимальный storage contract для домена `Codex Runtime`,
чтобы intake через Telegram, локальная обработка и reply loop работали
с одними и теми же объектами.

## Почему это нужно

Без storage contract сообщения из `Codex`-режима начинают жить как случайные файлы:
- контекст теряется;
- невозможно безопасно продолжать session;
- непонятно, что уже отправлено обратно пользователю;
- transport и agent loop расходятся по модели данных.

## Канонические контейнеры

```text
PACK-codex-runtime/
├── runtime/
│   ├── sessions/
│   ├── tasks/
│   ├── artifacts/
│   ├── memory/
│   ├── outbox/
│   └── registry/
```

## Контейнеры и их смысл

### `sessions/`

Карточки сессий. Одна session = одна продолжаемая ветка работы с пользователем.

Минимальные поля:
- `session_id`
- `channel`
- `chat_id`
- `status`
- `opened_at`
- `last_activity_at`
- `active_task_id`

### `tasks/`

Отдельные входящие задачи и ходы внутри session.

Минимальные поля:
- `task_id`
- `session_id`
- `kind`
- `source_message_id`
- `status`
- `text`
- `attachments`

### `artifacts/`

Файлы, полученные от пользователя или созданные агентом:
- изображения;
- документы;
- экспортированные отчёты;
- рабочие вложения.

### `memory/`

Context snapshots:
- краткая рабочая память по сессии;
- открытые вопросы;
- важные решения;
- ссылки на связанные домены и артефакты.

### `outbox/`

Записи об уже отправленных ответах:
- текст ответа;
- вложения;
- timestamp;
- delivery status;
- привязка к `task_id`/`session_id`.

### `registry/`

Живые индексы:
- список активных session;
- список pending/in_progress tasks;
- карта `telegram-thread -> session`.

## Инварианты

1. Ни один входящий ход не должен существовать без `session_id`.
2. Ни один исходящий ответ не должен существовать без `outbox entry`.
3. Артефакт не считается частью контекста, пока не привязан к `task` или `session`.
4. Telegram message/thread не является source-of-truth; source-of-truth — внутренняя storage model.

## Следующий шаг

Материализовать этот контракт в методе intake и затем в pilot-реализации `🤖 Codex`-режима.
