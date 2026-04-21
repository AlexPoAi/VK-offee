---
type: domain-entity
pack_id: PACK-codex-runtime
title: Роли домена Codex Runtime
status: draft
created: 2026-04-21
prefix: CODEX.ENTITY.001
---

# CODEX.ENTITY.001 — Роли домена Codex Runtime

## Назначение

Фиксирует функциональные роли домена. Это роли, а не конкретные люди или процессы.

## Роли

### User

Ставит задачу, продолжает сессию, присылает уточнения и вложения.

### Codex Agent

Разбирает задачу, держит рабочий контекст, исполняет действия и формирует ответ.

### Transport Bot

Принимает входящее сообщение, фиксирует его как артефакт и доставляет ответ обратно.

### Session Operator

Поддерживает связность между `chat/message/thread`, внутренней `session`,
task-карточками, context snapshots и outbox.

## Первичный role-method mapping

| Роль | Типовые методы |
|------|----------------|
| `User` | create-task, continue-session, attach-artifact |
| `Codex Agent` | analyze-task, produce-artifact, write-reply |
| `Transport Bot` | receive-message, persist-artifact, send-reply |
| `Session Operator` | bind-thread, update-session-state, rotate-context |
