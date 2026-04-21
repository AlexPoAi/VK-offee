---
type: domain-entity
pack_id: PACK-codex-runtime
title: Объекты внимания домена Codex Runtime
status: draft
created: 2026-04-21
prefix: CODEX.ENTITY.002
---

# CODEX.ENTITY.002 — Объекты внимания домена Codex Runtime

## Основные объекты внимания

### Session

Устойчивая единица диалога с пользователем, внутри которой накапливается контекст.

### Task

Отдельная входящая задача или ход в рамках сессии.

### Context Snapshot

Краткая рабочая память: что уже известно, что важно не забыть, что остаётся открытым.

### Artifact

Файл, картинка, документ, текстовый результат или ссылка, которые участвуют в работе.

### Transport Binding

Связь между Telegram-сообщением и внутренними идентификаторами сессии/задачи.

### Outbox Entry

Зафиксированный ответ или пакет материалов, отправленный обратно пользователю.

## Наблюдаемость

| Объект | Как наблюдается |
|--------|-----------------|
| `Session` | session-id, состояние, история продолжений |
| `Task` | входящий markdown/json card, статус обработки |
| `Context Snapshot` | отдельный memory/state файл |
| `Artifact` | физический файл + ссылка из task/session |
| `Transport Binding` | mapping chat/message/thread -> session/task |
| `Outbox Entry` | запись о доставленном ответе |
