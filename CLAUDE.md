# CLAUDE.md - Правила работы с VK-offee

> Инструкции для AI-агентов, работающих с репозиторием VK-offee

**Версия:** 3.1 (оптимизированная)
**Дата:** 2026-03-14

---

## 🎯 Миссия

VK-offee - операционная база знаний сети кофеен «Вкусный Кофе». Единый источник истины (Single Source of Truth) для всех процессов на базе FPF+SPF+SRT+FMT.

---

## 🏗️ Архитектура: 5 Bounded Contexts

| BC | Pack | Префикс | Описание |
|----|------|---------|----------|
| **Bar Operations** | PACK-bar | BAR | Барная стойка: напитки, эспрессо, бариста, касса |
| **Kitchen Operations** | PACK-kitchen | KITCHEN | Кухня: блюда, заготовки, повар, ТТК, себестоимость |
| **Service Operations** | PACK-service | SERVICE | Обслуживание: официант, заказы, подача, гости |
| **Shift Management** | PACK-management | MGMT | Управление сменой: планирование, контроль, отчёты |
| **HR Operations** | PACK-hr | HR | Персонал: найм, обучение, ДИ, графики |

### Маршрутизация знаний

Экстрактор распределяет captures по Pack:
- **Капучино, бариста, эспрессо** → PACK-bar
- **Боул, повар, заготовки, ТТК** → PACK-kitchen
- **Официант, заказ, гость** → PACK-service
- **Смена, план, контроль** → PACK-management
- **Найм, обучение, график** → PACK-hr

---

## 📁 Структура

```
VK-offee/
├── PACK-bar/           # Барная стойка
├── PACK-kitchen/       # Кухня
├── PACK-service/       # Обслуживание
├── PACK-management/    # Управление сменой
├── PACK-hr/            # Персонал
├── PACK-park-development/ # Развитие парка
├── knowledge-base/     # Сырые данные
├── telegram-bot/       # Боты
└── .github/scripts/    # Автоматизация
```

Каждый PACK содержит:
- `01-concepts/` - концепции
- `02-domain-entities/` - сущности
- `03-methods/` - методы
- `04-work-products/` - рабочие продукты
- `05-failure-modes/` - типовые ошибки

---

## 🤖 Правила для AI-агентов

### ОБЯЗАТЕЛЬНО

1. **Читать FPF** перед созданием процессов → `.fpf/FPF-Spec.md`
2. **Следовать SPF** процессам (00-11 стадий) → `process/`
3. **Использовать SRT** для организации → `SRT/F0-F9/`
4. **Запускать process-lint** перед коммитом
5. **Обновлять карты** после структурных изменений → `07-map/`
6. **Выдавать информацию блоками** (10-15 строк, пауза для вопросов)
7. **Обновлять MEMORY.md** после каждого git push

### ЗАПРЕЩЕНО

1. **Дидактический язык** - ❌ "step", "lesson", "try this"
2. **Сценарии вместо методов** - ❌ "Сначала X, потом Y"
3. **Смешивание понятий** - ❌ Роль = Метод = Работа
4. **Коммит без process-lint**
5. **Embeddings как source-of-truth** - только Markdown

---

## 📋 SPF: 12 стадий

| # | Стадия | Файл |
|---|--------|------|
| 00 | Обзор процесса | process-overview.md |
| 01 | Выбор домена | domain-selection.md |
| 02 | Границы контекста | bounded-context.md |
| 03 | Различения | distinctions-work.md |
| 04 | Сущности | domain-entities-identification.md |
| 05 | Приём информации | information-ingestion.md |
| 06 | Анализ | analysis-and-formalization.md |
| 07 | Методы и продукты | method-and-product-extraction.md |
| 08 | Типовые ошибки | failure-modes-extraction.md |
| 09 | SoTA-аннотации | sota-annotation.md |
| 10 | Карты | map-maintenance.md |
| 11 | Ревью | review-and-evolution-cycle.md |

---

## 🗂️ SRT: Systems-Roles-Table

```
                 Предприниматель  Инженер      Менеджер
Suprasystem      F1               F2           F3
SoI              F4               F5           F6
Constructor      F7               F8           F9
```

**F0** = метасемейство (управление хранилищем)

---

## 🔧 Протоколы FMT

### Open-Work-Close

**Open:** Создай ветку → обнови MEMORY.md → создай задачу в WeekPlan.md
**Work:** Следуй process/ → используй шаблоны → запускай process-lint
**Close:** Обнови карты → обнови MEMORY.md → создай PR

### Extraction Protocol

1. Найди информацию в `knowledge-base/`
2. Примени `process/06-analysis-and-formalization.md`
3. Создай карточку в соответствующем PACK
4. Обнови индекс и карту

---

## 📝 Чек-лист

**Перед началом:**
- [ ] Прочитал CLAUDE.md
- [ ] Прочитал MEMORY.md
- [ ] Понял текущую задачу

**При создании знаний:**
- [ ] Определил стадию процесса (00-11)
- [ ] Использовал шаблоны
- [ ] Применил различения
- [ ] Определил систему и роль (F0-F9)

**Перед коммитом:**
- [ ] Запустил process-lint
- [ ] Обновил карты
- [ ] Обновил индексы
- [ ] Обновил MEMORY.md

---

**Версия:** 3.1
**Последнее обновление:** 2026-03-14
