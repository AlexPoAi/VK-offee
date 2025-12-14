# База знаний «Вкусный Кофе»

1. **Русская навигация базы:** [перейти к витрине](./ru/README.md).

## Быстрые ссылки по структуре
- `ops/` — операции: [роли](ops/roles/README.md) и [чек-листы](ops/checklists/README.md).
- `training/` — обучение: [система бариста](training/barista-system-description.md) и [staff-docs](training/staff-docs/README.md).
- `vendors/` — поставщики: [каталог прайсов](vendors/README.md).
- `finance/` — расчёты: [себестоимость](finance/drink-costing.xlsx) и [калькуляции](finance/drink-calculations.xlsx).
- `assets/menus/` — визуалы меню: [оглавление](assets/menus/README.md).
- `assets/job-aids/` — фото-подсказки: [оглавление](assets/job-aids/README.md).
- `system/` — ценности и глоссарий: [культура](system/culture/README.md), [glossary](system/glossary.md).
- `franchise/` — материалы для партнёров: [презентация](franchise/presentation.md).

## Что нового
- Все пути переведены в латиницу и kebab-case для корректной автоматизации.
- Поставщики и прайсы собраны в `vendors/suppliers/`.
- Фото-подсказки перенесены в `assets/job-aids/barista-helper/` и связаны с чек-листами.
- Добавлена русская витрина `/ru/` с оглавлениями разделов.

## Как добавлять новые документы
- Клади файл в подходящий раздел (`ops/`, `training/`, `vendors/`, `finance/`, `assets/`, `system/`, `franchise/`).
- Используй `kebab-case` в латинице, без пробелов и скобок.
- Обновляй оглавления: профильный `README.md` + витрина `/ru/`.
- Добавляй строку в `knowledge-inventory.md` (таблица реестра).
- Проверяй ссылки и пути перед коммитом.
