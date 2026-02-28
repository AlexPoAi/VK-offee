# Архитектурное проектирование VK-offee

> Документ проектирования архитектуры согласно FPF+SPF+SRT+DDD
> Дата начала: 2026-02-28
> Статус: В разработке

---

## 🎯 Принятые решения

### Q1: System-of-Interest (Целевая система)
**Решение:** SoI = Сеть кофеен VK-offee (3 кофейни)
- Каждая кофейня = компонент SoI
- Сеть = целостная система с общими стандартами

### Q2: Количество Bounded Contexts
**Решение:** Максимально подробно (чем больше, тем лучше)
- Детальное разделение по предметным областям
- Каждый BC = чёткая граница ответственности

### Q3: Pack = BC
**Решение:** 1 Pack = 1 BC (вариант A)
- PACK-bar, PACK-kitchen, PACK-service, PACK-management, PACK-hr
- Чёткое соответствие между Pack и предметной областью

### Q4: Творческий конвейер
**Решение:** Отдельная платформа (Constructor/F8)
- creativ-convector = платформа обработки знаний
- Не часть VK-offee, а инструмент создания знаний

### Язык документации
**Решение:** Английский + русский в скобках
- Термины: English (Русский)
- Для русскоязычной команды

---

## 📐 Системная архитектура (FPF)

### Три системы

```
┌─────────────────────────────────────────────────────────────────┐
│ SUPRASYSTEM (Надсистема)                                        │
│ Что содержит VK-offee?                                          │
│                                                                 │
│ - Рынок HoReCa Крыма                                            │
│ - Клиенты кофеен (гости)                                        │
│ - Поставщики (кофе, продукты, оборудование)                     │
│ - Конкуренты (другие кофейни)                                   │
│ - Регуляторы (СЭС, налоговая, пожарная)                        │
│ - Партнёры (Шеф Умами, картинги)                               │
└─────────────────────────────────────────────────────────────────┘
                            ↓ содержит (∋)
┌─────────────────────────────────────────────────────────────────┐
│ SYSTEM-OF-INTEREST (Целевая система)                            │
│ Что мы создаём?                                                 │
│                                                                 │
│ Сеть кофеен VK-offee (3 кофейни):                               │
│ - Кофейня #1 (Тургенева)                                        │
│ - Кофейня #2 (...)                                              │
│ - Кофейня #3 (...)                                              │
│                                                                 │
│ Компоненты:                                                     │
│ - Операционная модель (как работают кофейни)                    │
│ - Стандарты качества                                            │
│ - Меню и рецепты                                                │
│ - Процессы обслуживания                                         │
│ - Система управления                                            │
└─────────────────────────────────────────────────────────────────┘
                            ↑ создаёт (→)
┌─────────────────────────────────────────────────────────────────┐
│ CONSTRUCTOR (Система создания)                                  │
│ Кто/что создаёт SoI?                                            │
│                                                                 │
│ Команда:                                                        │
│ - Владелец (Александр)                                          │
│ - Шеф                                                           │
│ - Менеджеры                                                     │
│                                                                 │
│ Платформа (F8):                                                 │
│ - Экзокортекс (FMT + агенты)                                    │
│ - Творческий конвейер (creativ-convector)                       │
│ - Инструменты (Telegram-бот, Google Sheets, GitHub)             │
│                                                                 │
│ Методология (F9):                                               │
│ - FPF (First Principles Framework)                              │
│ - SPF (Second Principles Framework)                             │
│ - SRT (Systems-Roles-Table)                                     │
│ - DDD Strategic Design                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ SRT: Systems-Roles-Table (F0-F9)

| Система | Предприниматель (Зачем?) | Инженер (Как устроено?) | Менеджер (Как работает?) |
|---------|-------------------------|------------------------|-------------------------|
| **Suprasystem** (Надсистема) | F1: Контекст рынка | F2: Окружение | F3: Взаимодействие с партнёрами |
| **System-of-Interest** (Целевая система) | F4: Требования клиентов | F5: Архитектура кофейни | F6: Операции (бар, кухня, сервис) |
| **Constructor** (Система создания) | F7: Принципы управления | F8: Платформа (экзокортекс) | F9: Команда и методология |

**F0:** Метасемейство (управление хранилищем знаний)

---

## 🏗️ Ключевые сущности (Domain Entities)

### Роли (Roles) — кто действует

| Роль | English | Русский | BC |
|------|---------|---------|-----|
| Barista | Бариста | Готовит напитки | Bar Operations |
| Waiter | Официант | Обслуживает гостей | Service Operations |
| Cook | Повар | Готовит блюда | Kitchen Operations |
| Assistant Cook | Помощник повара | Помогает повару | Kitchen Operations |
| Shift Manager | Менеджер смены | Управляет сменой | Shift Management |
| Chef | Шеф | Управляет кухней | Kitchen Operations |
| Cashier | Кассир | Работает с кассой | Bar Operations |
| Runner | Раннер | Доставляет заказы | Service Operations |

### Объекты внимания (Objects of Attention) — с чем работают

| Объект | English | Русский | BC |
|--------|---------|---------|-----|
| Beverage | Напиток | Эспрессо, капучино, латте | Bar Operations |
| Dish | Блюдо | Боул, сэндвич, салат | Kitchen Operations |
| Ingredient | Ингредиент | Кофе, молоко, лепёшка | Kitchen Operations |
| Preparation | Заготовка | Маринованная сёмга, варёный рис | Kitchen Operations |
| Order | Заказ | Заказ от клиента | Service Operations |
| Shift | Смена | Рабочая смена | Shift Management |
| Menu | Меню | Список позиций | All |
| Recipe (TTK) | Рецепт (ТТК) | Технологическая карта | Kitchen Operations |
| Checklist | Чек-лист | Контрольный список | All |
| Report | Отчёт | Отчёт смены | Shift Management |
| Calculation | Калькуляция | Расчёт себестоимости | Kitchen Operations |

### Методы (Methods) — как действуют

| Метод | English | Русский | BC |
|-------|---------|---------|-----|
| Beverage Preparation | Приготовление напитка | Эспрессо, капучино | Bar Operations |
| Dish Preparation | Приготовление блюда | Боул, сэндвич | Kitchen Operations |
| Guest Service | Обслуживание гостя | Приём заказа, подача | Service Operations |
| Cash Operation | Кассовая операция | Приём оплаты, возврат | Bar Operations |
| Shift Planning | Планирование смены | План на день | Shift Management |
| Quality Control | Контроль качества | Проверка стандартов | Shift Management |
| Ingredient Change | Изменение ингредиента | Замена компонента | Kitchen Operations |
| Writeoff/Rework | Списание/переработка | Утилизация продуктов | Kitchen Operations |

### Рабочие продукты (Work Products) — что создают

| WP | English | Русский | BC |
|-----|---------|---------|-----|
| Menu | Меню | Список позиций для гостей | All |
| Recipe (TTK) | Рецепт (ТТК) | Технологическая карта | Kitchen Operations |
| Checklist | Чек-лист | Контрольный список | All |
| Shift Report | Отчёт смены | Итоги смены | Shift Management |
| Cost Calculation | Калькуляция | Расчёт себестоимости | Kitchen Operations |
| Job Description | Должностная инструкция | ДИ сотрудника | HR Operations |
| Training Material | Обучающий материал | Материалы для обучения | HR Operations |
| Production System STA | Производственная система STA | Документ стандартов кухни | Kitchen Operations |

---

## 📦 Bounded Contexts (Предметные области)

### BC1: Bar Operations (Барная стойка)

**Ubiquitous Language (Единый язык):**
- Beverage (Напиток)
- Espresso (Эспрессо)
- Milk Foam (Молочная пена)
- Tamper (Темпер)
- Extraction (Пролив)
- Grind (Помол)
- Shot (Шот)

**Границы:**
- **Входит:** От зерна до готового напитка в руках клиента
- **Не входит:** Приготовление блюд, управление сменой

**Роли:**
- Barista (Бариста)
- Cashier (Кассир)

**Ключевые методы:**
- Espresso Preparation (Приготовление эспрессо)
- Cappuccino Preparation (Приготовление капучино)
- Latte Art (Латте-арт)
- Cash Operation (Кассовая операция)

**Связи с другими BC:**
- → Service Operations: Partnership (совместное обслуживание)
- → Kitchen Operations: Customer-Supplier (заказ заготовок)

---

### BC2: Kitchen Operations (Кухня)

**Ubiquitous Language:**
- Dish (Блюдо)
- Preparation (Заготовка)
- TTK (ТТК)
- Yield (Выход)
- Cost Price (Себестоимость)
- Ingredient (Ингредиент)
- Recipe (Рецепт)

**Границы:**
- **Входит:** От ингредиентов до готового блюда
- **Не входит:** Напитки, обслуживание гостей

**Роли:**
- Cook (Повар)
- Assistant Cook (Помощник повара)
- Chef (Шеф)

**Ключевые методы:**
- Dish Preparation (Приготовление блюда)
- Preparation Making (Создание заготовок)
- Ingredient Change (Изменение ингредиента)
- Writeoff/Rework (Списание/переработка)
- Cost Calculation (Расчёт себестоимости)

**Связи с другими BC:**
- → Bar Operations: Supplier (поставка заготовок)
- → Shift Management: Conformist (следует планам)

---

### BC3: Service Operations (Обслуживание)

**Ubiquitous Language:**
- Order (Заказ)
- Guest (Гость)
- Serving (Подача)
- Table Service (Сервировка)
- Delivery (Доставка)

**Границы:**
- **Входит:** Взаимодействие с клиентом от входа до ухода
- **Не входит:** Приготовление напитков и блюд

**Роли:**
- Waiter (Официант)
- Runner (Раннер)

**Ключевые методы:**
- Guest Service (Обслуживание гостя)
- Order Taking (Приём заказа)
- Serving (Подача)
- Table Cleaning (Уборка стола)

**Связи с другими BC:**
- → Bar Operations: Partnership (совместная работа)
- → Kitchen Operations: Customer (заказ блюд)

---

### BC4: Shift Management (Управление сменой)

**Ubiquitous Language:**
- Shift (Смена)
- Plan (План)
- Control (Контроль)
- Report (Отчёт)
- Calculation (Калькуляция)
- Standard (Стандарт)

**Границы:**
- **Входит:** Планирование и контроль операций
- **Не входит:** Приготовление, обслуживание

**Роли:**
- Shift Manager (Менеджер смены)
- Chef (Шеф)

**Ключевые методы:**
- Shift Planning (Планирование смены)
- Quality Control (Контроль качества)
- Shift Report (Отчёт смены)
- Standard Enforcement (Контроль стандартов)

**Связи с другими BC:**
- → All Operations: Published Language (публикует стандарты)

---

### BC5: HR Operations (Персонал)

**Ubiquitous Language:**
- Hiring (Найм)
- Training (Обучение)
- Job Description (Должностная инструкция)
- Schedule (График)
- Onboarding (Адаптация)

**Границы:**
- **Входит:** Работа с персоналом
- **Не входит:** Операционная деятельность

**Роли:**
- HR Manager (HR-менеджер)
- Chef (Шеф)

**Ключевые методы:**
- Hiring Process (Процесс найма)
- Training Process (Процесс обучения)
- Job Description Creation (Создание ДИ)
- Schedule Planning (Планирование графика)

**Связи с другими BC:**
- → All: Published Language (публикует ДИ)

---

## 🗺️ Context Map (Карта связей)

```
┌─────────────────┐
│  Bar Operations │
│   (Барная)      │
└────────┬────────┘
         │ Partnership
         ↓
┌─────────────────┐       Customer-Supplier      ┌──────────────────┐
│Service Operations│ ←──────────────────────────→ │Kitchen Operations│
│  (Обслуживание) │                              │     (Кухня)      │
└─────────────────┘                              └────────┬─────────┘
         ↑                                                │
         │ Published Language                            │ Conformist
         │                                                ↓
┌─────────────────────────────────────────────────────────────────┐
│              Shift Management (Управление сменой)               │
└─────────────────────────────────────────────────────────────────┘
         ↑
         │ Published Language
         │
┌─────────────────┐
│  HR Operations  │
│   (Персонал)    │
└─────────────────┘
```

---

## 📦 Структура Pack

### Соответствие BC → Pack

| Bounded Context | Pack | Префикс | Путь |
|----------------|------|---------|------|
| Bar Operations | PACK-bar | BAR | `/Users/alexander/Github/VK-offee/PACK-bar/` |
| Kitchen Operations | PACK-kitchen | KITCHEN | `/Users/alexander/Github/VK-offee/PACK-kitchen/` |
| Service Operations | PACK-service | SERVICE | `/Users/alexander/Github/VK-offee/PACK-service/` |
| Shift Management | PACK-management | MGMT | `/Users/alexander/Github/VK-offee/PACK-management/` |
| HR Operations | PACK-hr | HR | `/Users/alexander/Github/VK-offee/PACK-hr/` |

---

## 🔄 Интеграция с экосистемой

### Творческий конвейер (creativ-convector)

**Роль:** Constructor/F8 (Платформа)

**Поток:**
```
Obsidian (сырые мысли)
    ↓
creativ-convector (обработка)
    ↓
DS-strategy/inbox/captures.md
    ↓
Extractor (формализация)
    ↓
VK-offee/PACK-* (знания)
```

### Экзокортекс (FMT + агенты)

**Роль:** Constructor/F8 (Платформа)

**Агенты:**
- Strategist: планирование (WeekPlan, DayPlan)
- Extractor: извлечение знаний (captures → Pack)
- Session-watcher: обработка сессий стратегирования
- Scheduler: координация агентов

### Routing (маршрутизация знаний)

**Файл:** `FMT-exocortex-template/roles/extractor/config/routing.md`

**Логика:**
1. Capture содержит ключевые слова домена
2. Extractor определяет BC по ключевым словам
3. Extractor определяет Pack по BC
4. Extractor пишет в соответствующий Pack

---

## ✅ Следующие шаги

1. ✅ Определить три системы (Suprasystem, SoI, Constructor)
2. ✅ Выделить ключевые сущности (Roles, Objects, Methods, WP)
3. ✅ Определить Bounded Contexts (5 BC)
4. ✅ Спроектировать Context Map
5. ⏳ Создать структуру 5 Pack
6. ⏳ Обновить routing.md
7. ⏳ Мигрировать существующие файлы
8. ⏳ Протестировать интеграцию

---

**Дата последнего обновления:** 2026-02-28
**Статус:** Фаза 1-4 завершены, переход к реализации
