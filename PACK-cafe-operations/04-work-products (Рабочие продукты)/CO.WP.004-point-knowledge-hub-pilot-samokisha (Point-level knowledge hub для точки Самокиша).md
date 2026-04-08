---
id: CO.WP.004
name: Point-level knowledge hub для точки Самокиша
type: wp
status: active
created: 2026-04-08
last_updated: 2026-04-08
location: Самокиша (ул. Самокиша, 5Б)
pilot: true
---

# CO.WP.004 — Point-level knowledge hub для точки Самокиша

## Зачем открыт этот РП

По точке Самокиша уже накопился отдельный operational contour:
- договоры;
- согласования;
- материалы по вывеске;
- локальные фото;
- point-specific решения и follow-up'ы.

Если держать это только в общих папках `knowledge-base`, агенты и люди теряют связность. Поэтому нужен отдельный point-level hub, который собирает контекст точки, но не дублирует общесетевые документы.

## Цель

Сделать для Самокиша первый рабочий `point-level source-of-truth` слой, который потом можно тиражировать на Тургенева и Луговую.

## Что считается результатом

1. У точки есть свой каталог верхнего уровня.
2. Внутри есть минимум:
   - контекст точки;
   - статус точки;
   - каталог документов;
   - навигация на связанные work products и vendor-карточки.
3. Общесетевые документы не дублируются, а связываются перекрёстными ссылками.
4. Появляется reusable pattern для следующих точек сети.

## Состав point-hub

- [POINT-samokisha/README.md](/Users/alexander/Github/VK-offee/POINT-samokisha/README.md)
- [POINT-samokisha/CONTEXT.md](/Users/alexander/Github/VK-offee/POINT-samokisha/CONTEXT.md)
- [POINT-samokisha/PROJECT-STATUS.md](/Users/alexander/Github/VK-offee/POINT-samokisha/PROJECT-STATUS.md)
- [POINT-samokisha/DOCUMENTS-INDEX.md](/Users/alexander/Github/VK-offee/POINT-samokisha/DOCUMENTS-INDEX.md)

## Агентный состав на этот контур

### Strategist

Отвечает за логику структуры:
- что должно считаться point-specific;
- что остаётся общим сетевым слоем;
- в каком порядке разворачивать Самокиша, Тургенева, Луговая.

### Extractor

Отвечает за сбор и возврат материалов:
- документы;
- заметки;
- старые карточки;
- файлы из legacy knowledge-base.

### Knowledge Engineer

Отвечает за каталогизацию:
- индексы;
- связи;
- навигацию;
- единый source-of-truth слой без дублирования.

### Environment Engineer

Отвечает за ритуальную дисциплину:
- открытие такого структурного цикла;
- фиксацию РП;
- обновление контекста;
- корректное закрытие микроциклов.

## Что уже сделано

1. Поднят пилотный `POINT-samokisha`.
2. Собраны основные ссылки на point-related документы.
3. Связаны:
   - договор по рекламной конструкции;
   - разбор договора;
   - карточка подрядчика;
   - базовые документы по точке;
   - фото-материалы.
4. В корневой навигации `VK-offee` появилась ссылка на point-hub.

## Что дальше

### Ближайший слой

1. Дождаться ответа подрядчика по договору и обновить point-status.
2. Добрать point-specific документы:
   - аренда;
   - собственник / арендодатель;
   - фасад и входная группа;
   - согласования и переписка.

### Следующий structural layer

После стабилизации Самокиша тем же паттерном открыть:
- `POINT-turgeneva`
- `POINT-lugovaya`

## Принцип открытия и закрытия

Этот контур считается не просто папочной работой, а отдельным структурным РП.

Открытие должно включать:
- проверку WP Gate;
- фиксацию active WP;
- явный агентный состав.

Закрытие микроцикла должно включать:
- обновление point-status;
- фиксацию изменений в git;
- запись в session/inbox, если открыт новый follow-up.

## Связанные документы

- [POINT-samokisha/README.md](/Users/alexander/Github/VK-offee/POINT-samokisha/README.md)
- [POINT-samokisha/PROJECT-STATUS.md](/Users/alexander/Github/VK-offee/POINT-samokisha/PROJECT-STATUS.md)
- [CO.WP.003-samokisha-signage-design-contract-review (Проверка договора на архитектурное решение рекламной конструкции Самокиша).md](/Users/alexander/Github/VK-offee/PACK-cafe-operations/04-work-products%20%28%D0%A0%D0%B0%D0%B1%D0%BE%D1%87%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D1%8B%29/CO.WP.003-samokisha-signage-design-contract-review%20%28%D0%9F%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%D0%B4%D0%BE%D0%B3%D0%BE%D0%B2%D0%BE%D1%80%D0%B0%20%D0%BD%D0%B0%20%D0%B0%D1%80%D1%85%D0%B8%D1%82%D0%B5%D0%BA%D1%82%D1%83%D1%80%D0%BD%D0%BE%D0%B5%20%D1%80%D0%B5%D1%88%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%80%D0%B5%D0%BA%D0%BB%D0%B0%D0%BC%D0%BD%D0%BE%D0%B9%20%D0%BA%D0%BE%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D0%B8%20%D0%A1%D0%B0%D0%BC%D0%BE%D0%BA%D0%B8%D1%88%D0%B0%29.md)
- [signage-project-contractor (Проектная организация для вывески).md](/Users/alexander/Github/VK-offee/vendors/contractors/signage-project-contractor%20%28%D0%9F%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%BD%D0%B0%D1%8F%20%D0%BE%D1%80%D0%B3%D0%B0%D0%BD%D0%B8%D0%B7%D0%B0%D1%86%D0%B8%D1%8F%20%D0%B4%D0%BB%D1%8F%20%D0%B2%D1%8B%D0%B2%D0%B5%D1%81%D0%BA%D0%B8%29.md)
