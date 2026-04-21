---
type: work-product
pack_id: PACK-codex-runtime
title: Первый slice режима Codex в Telegram-боте
status: draft
created: 2026-04-21
prefix: CODEX.WP.003
---

# CODEX.WP.003 — Первый slice режима Codex в Telegram-боте

## Что сделано

В `VK-offee/telegram-bot` подготовлен первый безопасный slice для разделения режимов:

1. добавлен явный `Codex mode`;
2. добавлен возврат в обычный `RAG mode`;
3. `RAG` оставлен режимом по умолчанию;
4. в `Codex mode` входящие materialize в:
   - `session-card`
   - `task-card`
   - `artifacts/`
5. runtime-хранилище привязано к `PACK-codex-runtime/runtime`.

## Что это даёт

- рабочие задачи больше не смешиваются с вопросами к базе знаний;
- Telegram-бот получает отдельный агентный контур без разрушения текущего RAG;
- появляются первые реальные следы домена в runtime-структуре.

## Что ещё не доведено

- не реализован явный `thread -> session registry` поверх всех edge-cases;
- нет отдельного `reply loop` worker-а;
- cloud/VPS rollout ещё не выполнен;
- первый живой acceptance test через Telegram ещё впереди.

## Связанные файлы

- [bot.py](/Users/alexander/Github/VK-offee/telegram-bot/bot.py)
- [README.md](/Users/alexander/Github/VK-offee/telegram-bot/README.md)
- [CODEX.METHOD.001-telegram-codex-intake (Приём задач из Telegram в Codex Runtime).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/03-methods/CODEX.METHOD.001-telegram-codex-intake%20%28%D0%9F%D1%80%D0%B8%D1%91%D0%BC%20%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%20%D0%B8%D0%B7%20Telegram%20%D0%B2%20Codex%20Runtime%29.md)
- [CODEX.METHOD.002-session-binding-and-card-materialization (Привязка session и материализация карточек).md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/03-methods/CODEX.METHOD.002-session-binding-and-card-materialization%20%28%D0%9F%D1%80%D0%B8%D0%B2%D1%8F%D0%B7%D0%BA%D0%B0%20session%20%D0%B8%20%D0%BC%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%D0%BA%D0%B0%D1%80%D1%82%D0%BE%D1%87%D0%B5%D0%BA%29.md)
