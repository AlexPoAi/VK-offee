# Runtime Storage for `PACK-codex-runtime`

Этот каталог хранит живые runtime-артефакты домена:

- `sessions/` — карточки сессий
- `tasks/` — карточки задач
- `artifacts/` — вложения и результаты
- `memory/` — context snapshots
- `outbox/` — исходящие ответы
- `registry/` — runtime-индексы

Правило:

если runtime-файл становится частью source-of-truth или долгоживущего контекста,
он должен быть внесён в [DOCUMENT-REGISTRY.md](/Users/alexander/Github/VK-offee/PACK-codex-runtime/DOCUMENT-REGISTRY.md).
