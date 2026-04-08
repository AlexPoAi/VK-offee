# COMMUNICATION-REGISTRY — Парк Голубинка

> Единая карта переписок, писем, ответов и черновиков коммуникации по проекту.

## Как читать

- `Тип`:
  - `source` — зафиксированная реальная коммуникация
  - `draft` — подготовленный, но не обязательно отправленный текст
  - `support` — вспомогательная карточка/служебный артефакт
- `Статус`:
  - `sent` — отправлено
  - `in_progress` — коммуникация влияет на текущий контекст
  - `confirmed` — позиция/результат подтверждены
  - `waiting` — ждём обещанный документ или ответ
  - `archived-source` — сводный источник, а не живая точка переговоров
  - `next-action` — последняя активная точка, от которой зависит следующий ход

## Реестр коммуникаций

| ID | Тип | Дата | Участники | Канал | Тема | Статус | Файл |
|---|---|---|---|---|---|---|---|
| PARK.COMM.005 | source | 2026-03-19 | Александр → Константин, Елена | письмо | Ответ на графики и уточнения | sent | `04-communications/PARK.COMM.005-letter-to-architects-march18 (...).md` |
| PARK.COMM.006 | source | 2026-03-19 | Елена, Константин, Александр | Telegram | Ответ архитекторов по проекту и РНС | in_progress | `04-communications/PARK.COMM.006-telegram-response-march19 (...).md` |
| PARK.COMM.006-card | support | 2026-03-19 | system | card | Служебная карточка к COMM.006 | support | `04-communications/PARK.COMM.006-card.md` |
| PARK.COMM.007 | source | 2026-03-26 | Константин, Александр | Telegram | Передача АР в КР и новый визуал | in_progress | `04-communications/PARK.COMM.007-telegram-response-march26 (...).md` |
| PARK.COMM.007-visual | support | 2026-03-26 | Константин | image | АР визуал первой очереди | support | `04-communications/PARK.COMM.007-ar-visual-march26 (...).jpg` |
| PARK.COMM.008 | draft/source | 2026-03-26 | Александр → Валерий | Telegram | Ответ Валерию по КР и срокам | sent | `04-communications/PARK.COMM.008-reply-to-valery-march26 (...).md` |
| PARK.COMM.009 | source | 2026-03-27 | Валерий / Александр | Telegram | Подтверждение АР и ТУ | confirmed | `04-communications/PARK.COMM.009-valery-ar-confirmed-march27 (...).md` |
| PARK.COMM.010 | source | 2026-03-10..19 | ЛУКС / Александр | Telegram export | Сводная переписка TG ЛУКС | archived-source | `04-communications/PARK.COMM.010-telegram-export-march10-19 (...).md` |
| PARK.COMM.011 | source | 2026-04-03 | Елена / Александр | Telegram | Ответ на юридические вопросы | in_progress | `04-communications/PARK.COMM.011-elena-response-legal-questions (...).md` |
| PARK.COMM.012 | source | 2026-04-04 | Елена / Александр | Telegram | Спор по расчёту конструкций | in_progress | `04-communications/PARK.COMM.012-elena-response-april4 (...).md` |
| PARK.COMM.013 | source | 2026-04-02 | Елена / Александр | Telegram | Запрос графика сроков | waiting | `04-communications/PARK.COMM.013-schedule-request-april2 (...).md` |
| PARK.COMM.014 | source | 2026-04-07 | Елена / Александр | Telegram | Новый вариант ДС3 | confirmed | `04-communications/PARK.COMM.014-elena-april7-ds3-update (...).md` |
| PARK.COMM.015 | source | 2026-04-08 | Елена / Александр | Telegram | Условное принятие ДС3, позиция по ДС1, дедлайн графика | next-action | `04-communications/PARK.COMM.015-april8-response-on-ds3-and-deadline (...).md` |

## Активная цепочка переговоров

Для текущего решения по ЛУКС читать в таком порядке:
1. `PARK.COMM.011`
2. `PARK.COMM.012`
3. `PARK.COMM.013`
4. `PARK.COMM.014`
5. `PARK.COMM.015`
6. `PARK.WP.026-draft-message-luks`

## Привязка к документам

- `PARK.COMM.011-015` связаны с:
  - `PARK.DOC.015`
  - `PARK.DOC.016`
  - `PARK.DOC.017`
  - `PARK.DOC.019`
  - `PARK.DOC.020`
  - `PARK.WP.025`
  - `PARK.WP.026`

## Правило обновления

Когда появляется новое важное письмо или ответ:
1. Сохранить сырой источник
2. Создать `PARK.COMM.0NN`
3. Добавить запись сюда
4. Если коммуникация меняет картину проекта — обновить `PROJECT-STATUS.md` и `TELEGRAM-TIMELINE.md`
