# План интеграции FPF+SPF+SRT+FMT в VK-offee

**Дата создания:** 2026-02-20
**Статус:** В разработке
**Цель:** Полная перестройка VK-offee и творческого конвейера на базе FPF+SPF+SRT+FMT

---

## 🎯 Видение

Создать единую архитектуру знаний, где:
- **FPF** - фундамент (первые принципы)
- **SPF** - методология создания Pack (вторые принципы)
- **SRT** - организация знаний через F0-F9 (третьи принципы)
- **FMT** - практические протоколы работы
- **Агенты** реально используют эту архитектуру при работе с репозиториями

---

## 📊 Текущее состояние (Аудит)

### ✅ Что уже есть

**Фундамент (FPF):**
- `.fpf/FPF-Spec.md` (3.8 МБ, полная спецификация)
- `.fpf/FPF-Readme.md`
- `.fpf/INDEX.md`

**Pack (частично):**
- `PACK-cafe-operations/00-pack-manifest.md`
- `PACK-cafe-operations/01-domain-contract/distinctions.md`
- `PACK-cafe-operations/F1-Context/README.md`

**Данные:**
- `knowledge-base/` (299 файлов, синхронизация с Google Drive)
- `telegram-bot/` (бот для доступа к знаниям)

**Документация:**
- `CLAUDE.md` (правила для агентов)
- `MEMORY.md` (оперативная память проекта)
- `WeekPlan.md` (недельное планирование)

### ❌ Что отсутствует

**SPF структура:**
- `process/` - процессы создания знаний (00-11 стадий)
- `spec/` - спецификации (downstream-contract, ai-view, ids-and-references)
- `PACK-cafe-operations/02-domain-entities/` - роли, продукты, индексы
- `PACK-cafe-operations/03-methods/` - карточки методов
- `PACK-cafe-operations/04-work-products/` - рабочие продукты
- `PACK-cafe-operations/05-failure-modes/` - типовые ошибки
- `PACK-cafe-operations/06-sota/` - SoTA-аннотации
- `PACK-cafe-operations/07-map/` - карты связей

**SRT структура (F0-F9):**
- F0 - Метасемейство (управление хранилищем)
- F1 - Suprasystem/Предприниматель (контекст и рынок)
- F2 - Suprasystem/Инженер (окружение и интерфейсы)
- F3 - Suprasystem/Менеджер (взаимодействие и партнёрства)
- F4 - System-of-Interest/Предприниматель (требования и ценность)
- F5 - System-of-Interest/Инженер (архитектура продукта)
- F6 - System-of-Interest/Менеджер (реализация и процессы)
- F7 - Constructor/Предприниматель (принципы и экономика)
- F8 - Constructor/Инструменты (платформа и инструменты)
- F9 - Constructor/Менеджер (команда и методология)

**Процессы для агентов:**
- Протоколы Open-Work-Close
- Process lint (проверка перед коммитом)
- Hard gates (блокировка некорректных изменений)
- Extraction protocols (извлечение знаний)

### ⚠️ Legacy структура (требует миграции)

```
ru/                    → нужно мигрировать в SRT
ops/                   → нужно мигрировать в PACK
content/               → нужно мигрировать в SRT
system/                → нужно мигрировать в PACK
training/              → нужно мигрировать в PACK
```

---

## 🏗️ Целевая архитектура

```
VK-offee/
├── .fpf/                           # 🏛️ ФУНДАМЕНТ (FPF)
│   ├── FPF-Spec.md
│   ├── FPF-Readme.md
│   └── INDEX.md
│
├── process/                        # 📋 ПРОЦЕССЫ (SPF)
│   ├── README.md
│   ├── 00-process-overview.md
│   ├── 01-domain-selection.md
│   ├── 02-bounded-context.md
│   ├── 03-distinctions-work.md
│   ├── 04-domain-entities-identification.md
│   ├── 05-information-ingestion.md
│   ├── 06-analysis-and-formalization.md
│   ├── 07-method-and-product-extraction.md
│   ├── 08-failure-modes-extraction.md
│   ├── 09-sota-annotation.md
│   ├── 10-map-maintenance.md
│   ├── 11-review-and-evolution-cycle.md
│   └── process-lint.md
│
├── spec/                           # 📐 СПЕЦИФИКАЦИИ
│   ├── downstream-contract.md
│   ├── ai-view.md
│   ├── ids-and-references.md
│   └── human-guides.md
│
├── PACK-cafe-operations/           # 📦 PACK (Доменное знание)
│   ├── 00-pack-manifest.md
│   ├── 01-domain-contract/
│   │   ├── 01A-bounded-context.md
│   │   ├── 01B-distinctions.md
│   │   └── 01C-ontology.md
│   ├── 02-domain-entities/
│   │   ├── 02A-roles.md
│   │   ├── 02B-products.md
│   │   └── 02C-methods-index.md
│   ├── 03-methods/
│   │   ├── CAFE.METHOD.001-espresso.md
│   │   ├── CAFE.METHOD.002-cappuccino.md
│   │   └── ...
│   ├── 04-work-products/
│   │   ├── CAFE.WP.001-menu.md
│   │   ├── CAFE.WP.002-checklist.md
│   │   └── ...
│   ├── 05-failure-modes/
│   │   ├── CAFE.FAIL.001-burnt-milk.md
│   │   └── ...
│   ├── 06-sota/
│   │   └── CAFE.SOTA.001-coffee-extraction.md
│   └── 07-map/
│       └── CAFE.MAP.001.md
│
├── SRT/                            # 🗂️ SRT (F0-F9)
│   ├── F0-Meta/                    # Управление хранилищем
│   │   ├── F0.1-logic.md
│   │   ├── F0.4-reports.md
│   │   └── F0.9-inbox.md
│   ├── F1-Suprasystem-Entrepreneur/  # Контекст и рынок
│   ├── F2-Suprasystem-Engineer/      # Окружение и интерфейсы
│   ├── F3-Suprasystem-Manager/       # Взаимодействие
│   ├── F4-SoI-Entrepreneur/          # Требования и ценность
│   ├── F5-SoI-Engineer/              # Архитектура
│   ├── F6-SoI-Manager/               # Реализация
│   ├── F7-Constructor-Entrepreneur/  # Принципы и экономика
│   ├── F8-Constructor-Engineer/      # Платформа и инструменты
│   └── F9-Constructor-Manager/       # Команда и методология
│
├── knowledge-base/                 # 🗄️ ДАННЫЕ (сырые)
│   ├── БАР/
│   ├── КУХНЯ/
│   ├── ДЛЯ ШЕФА/
│   └── ...
│
├── telegram-bot/                   # 🤖 ИНСТРУМЕНТЫ
│   └── bot.py
│
├── .github/                        # ⚙️ АВТОМАТИЗАЦИЯ
│   └── scripts/
│       └── sync_google_drive.py
│
├── CLAUDE.md                       # 📖 Правила для агентов
├── MEMORY.md                       # 🧠 Оперативная память
├── WeekPlan.md                     # 📅 Недельное планирование
└── INTEGRATION-PLAN.md             # 📋 Этот файл
```

---

## 🚀 План реализации

### Фаза 0: Подготовка (1 день)
- [x] Аудит текущей структуры
- [x] Создание INTEGRATION-PLAN.md
- [ ] Бэкап текущего состояния
- [ ] Создание ветки `feature/fpf-srt-integration`

### Фаза 1: Создание SPF структуры (2 дня)
- [ ] Создать `process/` с 12 файлами процессов
- [ ] Создать `spec/` с 4 спецификациями
- [ ] Дополнить `PACK-cafe-operations/` недостающими папками
- [ ] Создать шаблоны для методов, WP, FM

### Фаза 2: Создание SRT структуры (2 дня)
- [ ] Создать `SRT/F0-Meta/`
- [ ] Создать `SRT/F1-F9/` с README в каждой
- [ ] Мигрировать контент из legacy папок
- [ ] Создать индексы и карты связей

### Фаза 3: Наполнение Pack (3 дня)
- [ ] Извлечь методы из knowledge-base
- [ ] Создать карточки методов (03-methods/)
- [ ] Создать рабочие продукты (04-work-products/)
- [ ] Задокументировать failure modes (05-failure-modes/)
- [ ] Создать карты связей (07-map/)

### Фаза 4: Интеграция с творческим конвейером (1 день)
- [ ] Создать связь VK-offee ↔ creativ-convector
- [ ] Настроить протоколы извлечения знаний
- [ ] Создать процесс Open-Work-Close

### Фаза 5: Обновление CLAUDE.md (1 день)
- [ ] Добавить правила работы с SPF
- [ ] Добавить правила работы с SRT
- [ ] Добавить process lint
- [ ] Добавить hard gates
- [ ] Добавить примеры использования

### Фаза 6: Обновление бота (1 день)
- [ ] Научить бота использовать SRT-структуру
- [ ] Научить бота использовать PACK-структуру
- [ ] Добавить поиск по F0-F9
- [ ] Добавить поиск по методам

### Фаза 7: Тестирование и документация (1 день)
- [ ] Протестировать работу агентов
- [ ] Создать примеры использования
- [ ] Обновить README.md
- [ ] Создать MIGRATION-GUIDE.md

---

## 🎯 Критерии успеха

1. **Структура соответствует SPF:**
   - Есть все папки process/, spec/, PACK/01-07/
   - Есть шаблоны для методов, WP, FM
   - Есть process lint

2. **Структура соответствует SRT:**
   - Есть все папки F0-F9
   - Контент распределён по семействам
   - Есть индексы и карты

3. **Агенты используют архитектуру:**
   - CLAUDE.md содержит правила SPF/SRT
   - Бот ищет по SRT-структуре
   - Process lint работает

4. **Связь с творческим конвейером:**
   - Есть протоколы извлечения знаний
   - Есть процесс Open-Work-Close
   - Заметки из Obsidian попадают в Pack

---

## 📚 Ссылки

- [SPF Personal](https://github.com/alexpoaiagent-sudo/spf-personal)
- [FMT Exocortex Template](https://github.com/TserenTserenov/FMT-exocortex-template)
- [Творческий конвейер](~/Documents/creativ-convector.nocloud/)
- [ШПАРГАЛКА FPF-SRT](~/Documents/creativ-convector.nocloud/ШПАРГАЛКА FPF-SRT.md)

---

**Следующий шаг:** Фаза 0 - Бэкап и создание ветки
