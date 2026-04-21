---
type: concept
pack_id: PACK-codex-runtime
title: Выбор домена Codex Runtime
status: draft
created: 2026-04-21
prefix: CODEX.CONCEPT.001
---

# CODEX.CONCEPT.001 — Выбор домена Codex Runtime

## Stage 01: Domain Selection Statement

### Domain

`Codex Runtime`

### Почему это домен, а не тема

Это не просто "Telegram" и не просто "чат с агентом".

У этого поля практики есть:
- практики и участники;
- методы работы;
- рабочие продукты;
- типовые failure modes.

Значит это соответствует критерию `bounded field of practice`,
а не является просто topic-level ярлыком.

### Scope

Домен покрывает:
- intake входящих задач к `Codex`;
- управление сессиями;
- хранение краткого контекста;
- маршрутизацию между transport, обработкой и ответом;
- фиксацию артефактов диалога и результатов.

### Exclusions

Явно не покрывает:
- предметный RAG по базе знаний `VK-offee`;
- операционные знания кофеен;
- дизайн как предметную область;
- Telegram как универсальный notification layer всего экзокортекса.

### Practitioners

- `User`
- `Codex Agent`
- `Transport Bot`
- `Session Operator`

### Adjacent Domains

- `PACK-exocortex-engineering` — инфраструктура и починка runtime;
- `telegram-bot` — transport-реализация;
- `PACK-design`, `PACK-cafe-operations`, point-level domains — downstream-домены задач.

### Boundary Test

| Вопрос | Ответ |
|--------|-------|
| Входит ли обычный поиск по базе знаний? | Нет |
| Входит ли приём задач через кнопку `Codex`? | Да |
| Входит ли session memory и outbox? | Да |
| Входит ли общая архитектура Telegram уведомлений без Codex-сессий? | Нет |

## Решение

Создавать отдельный Pack имеет смысл, потому что:
1. границы домена артикулируемы;
2. участники и роли устойчивы;
3. рабочие продукты повторяемы;
4. контур будет расти как отдельная система, а не как случайные папки.
