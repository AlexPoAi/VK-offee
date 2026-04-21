---
type: work-product
pack_id: PACK-codex-runtime
title: Реестр работ и артефактов Codex Runtime
status: living-document
created: 2026-04-21
prefix: CODEX.WP.000
---

# CODEX.WP.000 — Реестр работ и артефактов Codex Runtime

## Назначение

Живой реестр внедрений, pilot-срезов и ключевых решений по домену `PACK-codex-runtime`.

## Entries

| ID | Date | Status | Item | Note |
|----|------|--------|------|------|
| `CODEX.WP.001` | 2026-04-21 | draft | Выделение домена `Codex Runtime` | Созданы Domain Selection, Bounded Context и entity baseline |
| `CODEX.WP.002` | 2026-04-21 | draft | Intake-контракт `Telegram -> Codex` | Зафиксированы storage contract и `CODEX.METHOD.001` |
| `CODEX.WP.003` | 2026-04-21 | draft | Шаблоны карточек и runtime storage | Созданы session/task templates и runtime folders |
| `CODEX.WP.004` | 2026-04-21 | draft | Первый bot slice `RAG <-> Codex mode` | В `telegram-bot` добавлены `/codex`, `/rag`, session/task materialization и runtime routing |

## Next slices

- Безопасно отделить `Codex`-режим от текущего RAG-mode в Telegram-боте
- Материализовать session/task/outbox storage contract
- Подготовить pilot rollout на VPS без поломки рабочего бота
