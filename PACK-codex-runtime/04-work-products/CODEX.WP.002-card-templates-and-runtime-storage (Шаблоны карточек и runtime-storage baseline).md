---
type: work-product
pack_id: PACK-codex-runtime
title: Шаблоны карточек и runtime-storage baseline
status: draft
created: 2026-04-21
prefix: CODEX.WP.002
---

# CODEX.WP.002 — Шаблоны карточек и runtime-storage baseline

## Что сделано

В домене `Codex Runtime` материализованы:

1. Шаблон `session-card`
2. Шаблон `task-card`
3. Метод `CODEX.METHOD.002` для привязки session и materialization карточек
4. Базовая структура runtime storage:
   - `sessions/`
   - `tasks/`
   - `artifacts/`
   - `memory/`
   - `outbox/`
   - `registry/`

## Зачем это нужно

Теперь новый `Codex`-режим можно строить не на случайных файлах,
а на канонических карточках и заранее определённой runtime-структуре.

## Следующий шаг

Материализовать routing method для переключения `RAG mode -> Codex mode`
и затем безопасно врезать кнопку `🤖 Codex` в Telegram-бот.
