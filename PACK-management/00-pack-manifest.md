# Pack Manifest: Shift Management (Управление сменой)

## Идентификация
- **Имя:** PACK-management
- **Префикс:** MGMT
- **Версия:** 1.0.0
- **Дата создания:** 2026-02-28
- **Владелец:** VK-offee Management Team

## Bounded Context

**Ubiquitous Language (Единый язык):**
- Shift (Смена)
- Plan (План)
- Control (Контроль)
- Report (Отчёт)
- Calculation (Калькуляция)
- Standard (Стандарт)

## Границы домена

### ✅ Что ВХОДИТ в этот Pack:
- Планирование смены
- Контроль качества операций
- Отчёты смены
- Контроль стандартов
- Калькуляции
- Координация работы всех зон (бар, кухня, зал)
- Решение операционных проблем

### ❌ Что НЕ ВХОДИТ в этот Pack:
- Приготовление напитков (→ PACK-bar)
- Приготовление блюд (→ PACK-kitchen)
- Обслуживание гостей (→ PACK-service)
- Найм и увольнение персонала (→ PACK-hr)

## Роли

| Роль | English | Русский | Ответственность |
|------|---------|---------|----------------|
| Shift Manager | Менеджер смены | Управляет сменой, контролирует стандарты |
| Chef | Шеф | Управляет кухней, контроль качества блюд |

## Связи с другими BC

| BC | Тип связи | Описание |
|----|-----------|----------|
| Bar Operations | Published Language | Публикует стандарты для бара |
| Kitchen Operations | Published Language | Публикует стандарты для кухни |
| Service Operations | Published Language | Публикует стандарты для обслуживания |
| HR Operations | Customer-Supplier | Получает графики смен |

## Структура

```
PACK-management/
├── 00-pack-manifest.md (этот файл)
├── 01-domain-contract/
│   ├── bounded-context.md
│   └── distinctions.md
├── 02-domain-entities/
│   └── roles.md
├── 03-methods/
│   ├── MGMT.METHOD.001-shift-planning.md
│   ├── MGMT.METHOD.002-quality-control.md
│   └── MGMT.METHOD.003-shift-report.md
├── 04-work-products/
│   ├── shift-checklist.md
│   └── standards.md
├── 05-failure-modes/
├── 06-sota/
└── 07-map/
```

## Принципы использования

1. **Single Source of Truth:** Этот Pack - единственный источник стандартов и процессов управления
2. **Версионирование:** Все изменения через Git
3. **Актуальность:** Обновление при изменении стандартов
4. **Доступность:** Read-доступ для всех менеджеров, изменения через владельца

## Связи с другими репозиториями

- **Upstream:** Нет (базовый Pack)
- **Downstream:**
  - Telegram-бот (читает для ответов)
  - Обучающие материалы для менеджеров

---

*Последнее обновление: 2026-02-28*
