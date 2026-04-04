# Security Review Priority Checklist — 2026-04-04

Статус: inbox

Цель: быстро проверить уязвимые места хранения секретов и каналов авторизации, не ломая текущую экосистему и автоматизации.

## P0 — проверить сегодня

- Репозиторий GitHub `alexpoaiagent-sudo/VK-offee`: почему visibility не переключается в `private`.
- Историю git на старые `.env`, Telegram token, Anthropic/OpenAI keys, GitHub PAT.
- `.git/config` и `remote.origin.url`: нет ли токенов в URL и push-настройках.
- Каналы GitHub-аутентификации: `git`, VS Code, Claude Code, `gh`.
- `telegram-bot/.env`: какие реальные runtime-секреты используются сейчас.
- `$HOME/.config/aist/env`: есть ли там дублирующие или более актуальные ключи.
- Документы с уже известными следами утечек: `SECURITY-NOTICE.md`, `БЕЗОПАСНОСТЬ API КЛЮЧИ В GIT.md`, `СРОЧНО СМЕНИТЬ ТОКЕНЫ.md`.

## P1 — проверить после P0

- `.github/scripts/credentials.json`: актуальность и область доступа Google OAuth client.
- `.github/scripts/token.pickle` и `.github/scripts/token_upload.pickle`: какие сценарии реально завязаны на эти токены.
- Скрипты синхронизации Google Drive и Google Sheets: откуда они читают credentials и env.
- `saby-integration`: где реально хранятся `SABY_EMAIL`, `SABY_PASSWORD`, `SABY_APP_CLIENT_ID`, `SABY_APP_SECRET`, `SABY_SECRET_KEY`.
- Логи `sync-auto.log`, `sync-sheets.log`, `telegram-bot/*.log`, `.github/scripts/*.log`: не попадают ли туда чувствительные данные.
- Шаблоны `.env.example` и инструкции: нет ли в них реальных значений вместо placeholders.

## P2 — системные улучшения после инвентаризации

- Привести хранение секретов к одной модели: runtime secrets вне git, только шаблоны в репозитории.
- Перевести GitHub-доступ на единый безопасный способ без токенов в URL.
- Вынести внутренние IDs и чувствительные конфиги в env, если они не должны жить в коде.
- Добавить мягкий локальный secret-scan перед коммитом без жёсткой блокировки экосистемы.
- Подготовить runbook ротации секретов по одному сервису с обязательной проверкой после замены.
- Только после этого планировать очистку истории git/GitHub.

## Принцип выполнения

- Сначала изоляция доступа и инвентаризация.
- Потом ротация секретов по одному.
- После каждой замены проверяется только затронутый сервис.
- Переписывание истории выполняется последним этапом.
