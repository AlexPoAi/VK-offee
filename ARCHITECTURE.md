# Архитектура VK-offee

> Краткий обзор архитектуры репозитория VK-offee на основе FPF+SPF+SRT+DDD

**Версия:** 3.0
**Дата:** 2026-02-28
**Полная документация:** [ARCHITECTURE-DESIGN.md](ARCHITECTURE-DESIGN.md)

---

## Три системы (FPF)

```
┌─────────────────────────────────────────────────────────┐
│ SUPRASYSTEM (Надсистема)                                │
│ Рынок HoReCa, клиенты, поставщики, конкуренты          │
└─────────────────────────────────────────────────────────┘
                            ↓ содержит
┌─────────────────────────────────────────────────────────┐
│ SYSTEM-OF-INTEREST (Целевая система)                    │
│ Сеть кофеен VK-offee (3 кофейни)                        │
└─────────────────────────────────────────────────────────┘
                            ↑ создаёт
┌─────────────────────────────────────────────────────────┐
│ CONSTRUCTOR (Система создания)                          │
│ Команда + Экзокортекс + Творческий конвейер             │
└─────────────────────────────────────────────────────────┘
```

---

## 5 Bounded Contexts (DDD)

| BC | Pack | Префикс | Роли | Ключевые объекты |
|----|------|---------|------|------------------|
| **Bar Operations** | PACK-bar | BAR | Бариста, Кассир | Напитки, Эспрессо, Молочная пена |
| **Kitchen Operations** | PACK-kitchen | KITCHEN | Повар, Помощник, Шеф | Блюда, Заготовки, ТТК, Калькуляция |
| **Service Operations** | PACK-service | SERVICE | Официант, Раннер | Заказы, Гости, Подача |
| **Shift Management** | PACK-management | MGMT | Менеджер смены, Шеф | Смена, План, Отчёт, Стандарты |
| **HR Operations** | PACK-hr | HR | HR-менеджер | Найм, Обучение, ДИ, График |

---

## Context Map (Связи)

```
Bar ←Partnership→ Service
 ↓                   ↓
 Customer-Supplier   Customer
 ↓                   ↓
Kitchen ←────────────┘
 ↓ Conformist
Management (Published Language → All)
 ↑
HR (Supplier: графики)
```

**Паттерны связей:**
- **Partnership:** Bar ↔ Service (совместное обслуживание)
- **Customer-Supplier:** Kitchen → Bar, Kitchen → Service
- **Conformist:** Kitchen → Management (следует стандартам)
- **Published Language:** Management → All (публикует стандарты)

---

## Структура Pack

Каждый Pack содержит:

```
PACK-{name}/
├── 00-pack-manifest.md         # Границы домена, роли, связи
├── 01-domain-contract/         # Bounded Context, различения
├── 02-domain-entities/         # Роли, объекты, методы
├── 03-methods/                 # Методы (IPO-карточки)
├── 04-work-products/           # Рабочие продукты (меню, ТТК, ДИ)
├── 05-failure-modes/           # Типовые ошибки
├── 06-sota/                    # SoTA-аннотации
└── 07-map/                     # Карты связей
```

---

## Интеграция с экосистемой

### Творческий конвейер (creativ-convector)

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

**Агенты:**
- `com.exocortex.scheduler` — координация агентов
- `com.strategist.morning` — утреннее планирование
- `com.strategist.weekreview` — недельный обзор
- `com.extractor.inbox-check` — извлечение знаний (каждые 3ч)
- `com.extractor.session-watcher` — обработка сессий стратегирования

### Маршрутизация знаний

**Файл:** `FMT-exocortex-template/roles/extractor/config/routing.md`

Экстрактор читает ключевые слова в capture и определяет целевой Pack:

| Ключевые слова | Pack |
|----------------|------|
| капучино, бариста, эспрессо, латте-арт | PACK-bar |
| боул, повар, заготовки, ТТК, себестоимость | PACK-kitchen |
| официант, заказ, гость, подача | PACK-service |
| смена, план, контроль, отчёт | PACK-management |
| найм, обучение, график, ДИ | PACK-hr |

---

## Миграция из PACK-cafe-operations

**Статус:** Завершена (2026-02-28)

Мигрированы файлы:
- `CO.METHOD.001` → `KITCHEN.METHOD.001` (изменение ингредиентов)
- `CO.METHOD.002` → `KITCHEN.METHOD.002` (списание/переработка)
- `CO.ENTITY.001` → `KITCHEN.ENTITY.001` (концепция кухни)
- `CO.WP.001` → `KITCHEN.WP.001` (производственная система STA)

**Следующий шаг:** Удаление PACK-cafe-operations после проверки.

---

## Быстрый старт

### Для агентов

1. Читай `CLAUDE.md` — полные правила работы
2. Читай `ARCHITECTURE-DESIGN.md` — детальная архитектура
3. Читай `00-pack-manifest.md` целевого Pack — границы домена
4. Используй routing.md для маршрутизации captures

### Для разработчиков

1. Клонируй репозиторий
2. Изучи `CLAUDE.md` (правила работы)
3. Изучи `ARCHITECTURE-DESIGN.md` (архитектура)
4. Выбери Pack для работы
5. Используй шаблоны из `PACK-{name}/_template/`

---

**Дата последнего обновления:** 2026-02-28
**Автор архитектуры:** FPF+SPF+SRT+DDD
**Статус:** Активная разработка
