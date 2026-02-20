# RULES - Правила работы с VK-offee

Детальные правила для всех AI-агентов.

---

## ⚠️ КРИТИЧЕСКИЕ ЗАПРЕТЫ

### ЗАПРЕЩЕНО создавать:

❌ **Дубликаты информации**
- Одна информация в одном месте
- Используй ссылки вместо копирования

❌ **Дидактический язык в Pack**
- "step 1", "step 2"
- "lesson", "module", "week 1"
- "try this", "exercise"
- "first/then", "in N days"
- **Причина:** Pack фиксирует ЧТО существует, не КАК учить

❌ **Сценарии вместо методов**
- Метод — рецепт (как делать)
- Сценарий — конкретный случай (что произошло)

❌ **Смешивание понятий**
- Меню ≠ Рецепт
- Смена ≠ Сотрудник
- Клиент ≠ Постоянный клиент
- Процесс ≠ Сервис
- Стандарт ≠ Навык
- Калькуляция ≠ Себестоимость
- Должностная инструкция ≠ Чек-лист

---

## ✅ ОБЯЗАТЕЛЬНЫЕ ДЕЙСТВИЯ

### При создании Method:

1. ✅ Используй шаблон `_template/03-methods/_method-card-template.md`
2. ✅ Присвой ID: `CAFE.METHOD.<NNN>-name.md`
3. ✅ Добавь ссылку на Work Product
4. ✅ Добавь ссылку на Distinction
5. ✅ Обнови `02C-methods-index.md`
6. ✅ Обнови карту в `07-map/`
7. ✅ Запусти process-lint

### При создании Work Product:

1. ✅ Используй шаблон `_template/04-work-products/_work-product-card-template.md`
2. ✅ Присвой ID: `CAFE.WP.<NNN>-name.md`
3. ✅ Добавь **observability criteria** (как проверить существование)
4. ✅ Добавь ссылку на Method
5. ✅ Обнови карту в `07-map/`
6. ✅ Запусти process-lint

### При создании Failure Mode:

1. ✅ Используй шаблон `_template/05-failure-modes/_failure-mode-template.md`
2. ✅ Присвой ID: `CAFE.FAIL.<NNN>-name.md`
3. ✅ Добавь **detection test** (как обнаружить)
4. ✅ Укажи связанные Method и Distinction
5. ✅ Обнови карту в `07-map/`
6. ✅ Запусти process-lint

### Перед КАЖДЫМ коммитом:

1. ✅ Запусти process-lint
2. ✅ Проверь все Hard Gates
3. ✅ Обнови карты в `07-map/`
4. ✅ Обнови индексы
5. ✅ Обнови MEMORY.md (если нужно)

---

## 🎯 Правила навигации

### Как найти информацию:

**Шаг 1:** Определи тип вопроса
- Концептуальный → `.fpf/`
- Процессный → `process/`
- Доменный → `PACK-cafe-operations/`
- Организационный → `SRT/`
- Сырые данные → `knowledge-base/`

**Шаг 2:** Определи систему и роль (для SRT)
- Suprasystem (F1-F3) — окружение
- System-of-Interest (F4-F6) — кофейни
- Constructor (F7-F9) — команда

**Шаг 3:** Используй индексы
- `PACK-cafe-operations/02C-methods-index.md`
- `PACK-cafe-operations/07-map/CAFE.MAP.001.md`
- `SRT/README.md`

---

## 📝 Правила именования

### Файлы:

| Тип | Паттерн | Пример |
|-----|---------|--------|
| Method | `CAFE.METHOD.<NNN>-name.md` | `CAFE.METHOD.001-espresso.md` |
| Work Product | `CAFE.WP.<NNN>-name.md` | `CAFE.WP.001-menu.md` |
| Failure Mode | `CAFE.FAIL.<NNN>-name.md` | `CAFE.FAIL.001-burnt-milk.md` |
| SoTA | `CAFE.SOTA.<NNN>-name.md` | `CAFE.SOTA.001-extraction.md` |
| Map | `CAFE.MAP.<NNN>.md` | `CAFE.MAP.001.md` |

### Коммиты:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` — новая функциональность
- `fix:` — исправление
- `docs:` — документация
- `refactor:` — рефакторинг
- `test:` — тесты
- `chore:` — рутина

**Примеры:**
```
feat(pack): добавлен метод приготовления латте
fix(bot): исправлен поиск по зарплате
docs(agents): создана папка AGENTS/
```

---

## 🔍 Правила поиска

### В knowledge-base/:

1. Используй синонимы:
   - зарплата → з/п, оплата, зарплат
   - себестоимость → себестоим, стоимость
   - рецепт → приготовление, готовить

2. Фильтруй служебные файлы:
   - Игнорируй `sync-reports/`
   - Игнорируй `~$` (временные файлы)

3. Поддерживаемые форматы:
   - ✅ .md, .csv, .xlsx
   - ❌ .docx, .pdf (не индексируются)

### В PACK:

1. Используй ID для точного поиска
2. Используй индексы для обзора
3. Используй карты для связей

---

## 🚦 Hard Gates (блокируют коммит)

| Gate | Проверка | Как исправить |
|------|----------|---------------|
| **HG-1** | Method без WP link | Добавь ссылку на Work Product |
| **HG-2** | Method без distinction | Добавь ссылку на Distinction |
| **HG-3** | WP без existence criteria | Добавь критерии наблюдаемости |
| **HG-4** | FM без detection test | Добавь тест обнаружения |
| **HG-5** | Structural change без map update | Обнови карту в 07-map/ |
| **HG-6** | Didactic language | Убери "step", "lesson", "try this" |
| **HG-7** | Scenario вместо method | Переформулируй как метод |
| **HG-8** | SoTA без revision criterion | Добавь критерий пересмотра |

---

## 📚 Правила документирования

### Структура Method:

```markdown
# CAFE.METHOD.XXX - Название

## Назначение
Зачем этот метод

## Входы
Что нужно для выполнения

## Процесс
Как выполнять (НЕ "step 1, step 2")

## Выходы
Что получается (ссылка на Work Product)

## Связанные различения
Ссылки на distinctions

## Failure modes
Ссылки на типовые ошибки
```

### Структура Work Product:

```markdown
# CAFE.WP.XXX - Название

## Описание
Что это

## Observability criteria
Как проверить существование (ОБЯЗАТЕЛЬНО!)

## Создаётся методом
Ссылка на Method

## Используется в
Где применяется
```

### Структура Failure Mode:

```markdown
# CAFE.FAIL.XXX - Название

## Описание
Что ломается

## Detection test
Как обнаружить (ОБЯЗАТЕЛЬНО!)

## Причины
Почему происходит

## Связанные методы
Ссылки на Methods

## Связанные различения
Ссылки на Distinctions
```

---

## 🔗 Правила ссылок

### Внутренние ссылки:

```markdown
[Метод эспрессо](../03-methods/CAFE.METHOD.001-espresso.md)
[Различение меню/рецепт](../01-domain-contract/01B-distinctions.md#1-меню--рецепт)
```

### Ссылки на FPF:

```markdown
[U.BoundedContext](../../.fpf/INDEX.md#uboundedcontext)
[A.7 Strict Distinction](../../.fpf/FPF-Spec.md#a7-strict-distinction)
```

---

## 🎓 Правила обучения

### Для новых агентов:

**День 1:**
1. Прочитай AGENTS/START-HERE.md
2. Прочитай AGENTS/ARCHITECTURE.md
3. Прочитай AGENTS/RULES.md (этот файл)

**День 2:**
1. Изучи PACK-cafe-operations/01-domain-contract/
2. Изучи SRT/README.md
3. Попробуй найти информацию

**День 3:**
1. Создай тестовый Method
2. Запусти process-lint
3. Исправь ошибки

---

## ⚡ Быстрая справка

**Создать Method:**
```bash
1. Копируй _template/03-methods/_method-card-template.md
2. Переименуй в CAFE.METHOD.XXX-name.md
3. Заполни все секции
4. Добавь в 02C-methods-index.md
5. Обнови 07-map/
6. Запусти process-lint
```

**Найти информацию:**
```bash
1. Определи тему
2. Найди семейство SRT (F0-F9)
3. Проверь PACK-cafe-operations/
4. Проверь knowledge-base/
```

**Перед коммитом:**
```bash
1. process-lint
2. Hard Gates
3. Карты
4. Индексы
5. MEMORY.md
```

---

**Версия:** 1.0
**Дата:** 2026-02-20
