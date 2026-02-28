# Pack Manifest: HR Operations (Персонал)

## Идентификация
- **Имя:** PACK-hr
- **Префикс:** HR
- **Версия:** 1.0.0
- **Дата создания:** 2026-02-28
- **Владелец:** VK-offee Management Team

## Bounded Context

**Ubiquitous Language (Единый язык):**
- Hiring (Найм)
- Training (Обучение)
- Job Description (Должностная инструкция)
- Schedule (График)
- Onboarding (Адаптация)

## Границы домена

### ✅ Что ВХОДИТ в этот Pack:
- Найм персонала
- Обучение и адаптация новых сотрудников
- Должностные инструкции
- Планирование графиков работы
- Оценка персонала
- Обучающие материалы
- Карьерное развитие

### ❌ Что НЕ ВХОДИТ в этот Pack:
- Операционная деятельность (→ PACK-bar, PACK-kitchen, PACK-service)
- Управление сменой (→ PACK-management)
- Финансы и зарплаты (→ DS-cafe-strategy)

## Роли

| Роль | English | Русский | Ответственность |
|------|---------|---------|----------------|
| HR Manager | HR-менеджер | Найм, обучение, развитие персонала |
| Chef | Шеф | Обучение поваров, оценка кухонного персонала |

## Связи с другими BC

| BC | Тип связи | Описание |
|----|-----------|----------|
| Bar Operations | Published Language | Публикует ДИ для бариста |
| Kitchen Operations | Published Language | Публикует ДИ для поваров |
| Service Operations | Published Language | Публикует ДИ для официантов |
| Shift Management | Supplier | Поставляет графики смен |

## Структура

```
PACK-hr/
├── 00-pack-manifest.md (этот файл)
├── 01-domain-contract/
│   ├── bounded-context.md
│   └── distinctions.md
├── 02-domain-entities/
│   └── roles.md
├── 03-methods/
│   ├── HR.METHOD.001-hiring.md
│   ├── HR.METHOD.002-training.md
│   └── HR.METHOD.003-onboarding.md
├── 04-work-products/
│   ├── job-descriptions/
│   └── training-materials/
├── 05-failure-modes/
├── 06-sota/
└── 07-map/
```

## Принципы использования

1. **Single Source of Truth:** Этот Pack - единственный источник знаний о работе с персоналом
2. **Версионирование:** Все изменения через Git
3. **Актуальность:** Обновление при изменении ДИ или процессов найма
4. **Доступность:** Read-доступ для всех менеджеров, изменения через HR-менеджера

## Связи с другими репозиториями

- **Upstream:** Нет (базовый Pack)
- **Downstream:**
  - Telegram-бот (читает для ответов)
  - Обучающие материалы для новых сотрудников

---

*Последнее обновление: 2026-02-28*
