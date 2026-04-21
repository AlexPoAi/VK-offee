---
type: method
pack_id: PACK-codex-runtime
id: CODEX.METHOD.002
title: Привязка session и материализация карточек
status: draft
owner_role: Session Operator
created: 2026-04-21
updated: 2026-04-21
---

# CODEX.METHOD.002 — Привязка session и материализация карточек

## Назначение

Единый метод, который превращает входящий ход пользователя в пару:
- `session-card`
- `task-card`

и не даёт Telegram-сообщениям оставаться без внутренней модели.

## Каноническая последовательность

1. Проверить, есть ли у пользователя активная `session-card`.
2. Если активной сессии нет, создать новую `session-card`.
3. Если сессия есть, обновить `last_activity_at`.
4. Создать новую `task-card` для конкретного входящего хода.
5. Привязать `task_id` к `session-card` как `active_task_id` или добавить в список active tasks.
6. Если есть вложения, записать их в `artifacts/` и сослаться на них из `task-card`.
7. Внести карточки в `registry` и `DOCUMENT-REGISTRY`, если они становятся частью source-of-truth слоя.
8. Вернуть пользователю truthful acknowledgement.

## Критерий завершения

- входящее не потеряно;
- `session-card` существует;
- `task-card` существует;
- связь `session -> task` материальна и наблюдаема.

## Типовые ошибки

### E1. Создание task без session

Коррекция: сначала session binding, потом task materialization.

### E2. Одна длинная session без обновляемой сводки

Коррекция: каждая session должна иметь `Last Truthful Summary`.
