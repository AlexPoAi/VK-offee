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
| PARK.COMM.016 | source | 2026-04-08 | Елена / Александр | Telegram | Эскалация по графику, срокам и дисциплине ответов | sent | `04-communications/PARK.COMM.016-april8-escalation-on-schedule-and-response-discipline (...).md` |
| PARK.COMM.017 | source | 2026-04-09 | Елена / Александр | Telegram | Пакет документов ЛУКС: график, ДС3, ДС2 | in_progress | `04-communications/PARK.COMM.017-april9-luks-package-documents (...).md` |
| PARK.COMM.018 | source | 2026-04-09 | Александр / Елена | Telegram | Ответ по графику, срокам после АГО и юридической формулировке | next-action | `04-communications/PARK.COMM.018-april9-reply-on-graph-and-legal-wording (...).md` |
| PARK.COMM.019 | source | 2026-04-09 | Елена / Александр | Telegram | Подтверждение: все уточнения уже есть в графике | next-action | `04-communications/PARK.COMM.019-april9-elena-confirms-graph-signed (...).md` |
| PARK.COMM.020 | source | 2026-04-09 | Александр / Елена | Telegram | Организация оплаты, забора пакета АГО и подписания оригиналов | next-action | `04-communications/PARK.COMM.020-april9-office-pickup-and-signing (...).md` |
| PARK.COMM.021 | source | 2026-04-10 | Александр / ЛУКС | internal-fixation | Оплачены предоплата по ДС3 и остаток по ДС2 | confirmed | `04-communications/PARK.COMM.021-april10-payments-ds3-and-ds2 (...).md` |
| PARK.COMM.022 | source | 2026-04-11 | Главный инженер ЛУКС / Александр | image-message | Фото-ответ по составу расчёта конструкций ДС1 | in_progress | `04-communications/PARK.COMM.022-chief-engineer-ds1-photo-response-april11 (...).md` |
| PARK.COMM.023 | source | 2026-04-15 | Александр, Елена, Главный инженер ЛУКС | встреча | **Встреча в офисе ЛУКС — задержка пакета АГО** | confirmed | `04-communications/PARK.COMM.023-meeting-april15-ago-package-delay (...).md` |
| PARK.COMM.024 | source | 2026-04-17 | Александр, секретарь отдела архитектуры | личная подача | Подача документов АГО в Администрацию | confirmed | `04-communications/PARK.COMM.024-ago-submission-april17 (...).md` |
| PARK.COMM.025 | source | 2026-04-22 | Александр, приёмная архитектуры, Меметов Артур Заферович | телефон | Подтверждена регистрация АГО, входящий номер и ответственный | confirmed | `04-communications/PARK.COMM.025-bahchisaray-ago-registration-status-april22 (...).md` |
| PARK.COMM.026 | draft/source | 2026-04-22..24 | Александр → ГУП РК "Вода Крыма" | email / ручная подача | Запрос по статусу канализационной трубы; email-ответ не получен, подготовлена ручная подача через `PARK.DOC.038` | next-action | `04-communications/PARK.COMM.026-draft-letter-water-crimea-sewage-pipe (...).md` |
| PARK.COMM.027 | draft/source | 2026-04-22..27 | Александр → Администрация Бахчисарайского района | письмо / личная подача | Письмо по балансодержателю / статусу канализационной трубы, подано 27.04.2026 | submitted | `04-communications/PARK.COMM.027-draft-letter-bahchisaray-district-sewage-pipe (...).md` |
| PARK.COMM.028 | source | 2026-04-27 | Александр / Крымэнерго | личный визит | Подписанный договор Крымэнерго получен; следующий шаг — личный кабинет 29.04.2026 | confirmed | `04-communications/PARK.COMM.028-crimea-energy-signed-contract-april27 (...).md` |
| PARK.COMM.029 | source | 2026-04-27 | Александр → Администрация Бахчисарая | личная подача | Заявление по канализационной трубе подано; ждём ответ | submitted | `04-communications/PARK.COMM.029-bahchisaray-pipe-application-submitted-april27 (...).md` |
| PARK.COMM.030 | source | 2026-04-27 | constantnine, ValerON, Александр | Telegram | Вопрос по скамейкам и урнам для СПОЗУ; ответ отправлен: заложить минимальный объём лавочек и урн | sent | `04-communications/PARK.COMM.030-spozu-benches-urns-question-april27 (...).md` |

## Активная цепочка переговоров

Для текущего решения по ЛУКС читать в таком порядке:
1. `PARK.COMM.011` — Ответ Елены на юридические вопросы (03.04)
2. `PARK.COMM.012` — Спор по расчёту конструкций (04.04)
3. `PARK.COMM.013` — Запрос графика сроков (02.04)
4. `PARK.COMM.014` — Новый вариант ДС3 (07.04)
5. `PARK.COMM.015` — Условное принятие ДС3, позиция по ДС1 (08.04)
6. `PARK.COMM.016` — Эскалация по графику и дисциплине (08.04)
7. `PARK.COMM.017` — Пакет документов ЛУКС (09.04)
8. `PARK.COMM.018` — Ответ по графику и юридической формулировке (09.04)
9. `PARK.COMM.019` — Подтверждение графика Еленой (09.04)
10. `PARK.COMM.020` — Организация оплаты и забора АГО (09.04)
11. `PARK.COMM.021` — Оплачены ДС3 и ДС2 (10.04)
12. `PARK.COMM.022` — Фото-ответ главного инженера по ДС1 (11.04)
13. `PARK.COMM.023` — Встреча 15.04: пакет АГО не выдан (15.04)
14. `PARK.COMM.024` — Подача документов АГО в Администрацию (17.04)
15. **`PARK.COMM.025` — Подтверждена регистрация АГО, входящий номер и ответственный (22.04)**
16. **`PARK.COMM.028` — Получен подписанный договор Крымэнерго (27.04)**
17. **`PARK.COMM.029` — Подано заявление по трубе в администрацию Бахчисарая (27.04)**
18. **`PARK.COMM.030` — Срочный вопрос проектировщиков по скамейкам/урнам для СПОЗУ (27.04)**
19. `PARK.WP.026-draft-message-luks`

## Текущий статус переговоров (27.04.2026)

**Подписано:**
- ✅ ДС2 (АР полный + ПЗ, 224 772 ₽)
- ✅ ДС3 (пакет РНС, 525 000 ₽)
- ✅ АВР №1 (акт выполненных работ по ДС2)

**НЕ подписано:**
- ❌ Договор П240 (оригинал) — требуется консультация юриста
- ❌ ДС1 (расчёт конструкций, 80 000 ₽) — требуется письменное обоснование

**Документы АГО:**
- ✅ Поданы в Администрацию Бахчисарайского района 17.04.2026
- ✅ Зарегистрированы: входящий номер `02-124/6973`
- ✅ Назначен ответственный: `Меметов Артур Заферович`

**Инженерные сети:**
- ✅ Подписанный договор Крымэнерго получен 27.04.2026
- ⏭️ 29.04.2026 зарегистрироваться в личном кабинете Крымэнерго
- ✅ Заявление по канализационной трубе подано в администрацию Бахчисарая 27.04.2026
- ⏭️ 28.04.2026 подать `PARK.DOC.038` в Водоканал / `Воду Крыма` в Симферополе

**Следующие действия:**
1. При следующем звонке в архитектуру уточнить стадию рассмотрения по номеру `02-124/6973`
2. 28.04.2026 подать `PARK.DOC.038` в `ГУП РК "Вода Крыма"` и взять входящий номер / отметку о приёме
3. 29.04.2026 зарегистрироваться в личном кабинете Крымэнерго
4. Дождаться ответа администрации Бахчисарая по трубе
5. Запросить письменную фиксацию причины задержки АГО от ЛУКС
6. Запросить письменное разграничение ДС1 vs ДС3
7. Консультация юриста по оригиналу П240

## Привязка к документам

- `PARK.COMM.011-022` связаны с:
  - `PARK.DOC.015`
  - `PARK.DOC.016`
  - `PARK.DOC.022`
  - `PARK.DOC.023`
  - `PARK.DOC.024`
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
4. Если коммуникация меняет картину проекта — обновить `PROJECT-STATUS.md` и `PROJECT-TIMELINE.md`
