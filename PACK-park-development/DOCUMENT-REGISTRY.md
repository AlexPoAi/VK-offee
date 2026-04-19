# DOCUMENT-REGISTRY — Парк Голубинка

> Полный реестр всех документов проекта с момента подписания договора (21.07.2025) до текущего момента.

## Как читать

- `Оригинал` — физический файл: `pdf`, `docx`, `xlsx`, `jpg`, `txt`, `json`
- `Карточка` — markdown-описание, которое агент читает первым
- `Дата` — дата создания/получения документа
- `Статус`:
  - `ok` — оригинал и карточка есть
  - `card-only` — есть карточка, оригинал надо ещё точно привязать
  - `original-only` — оригинал есть, карточки ещё нет
  - `mixed` — есть несколько связанных файлов, нужна дальнейшая нормализация
  - `draft` — рабочий черновик
  - `active` — активный документ в работе

## Юридические документы (договоры, ДС, акты)

| ID | Дата | Тема | Оригинал | Карточка | Статус |
|---|---|---|---|---|---|
| PARK.DOC.020 | 2025-07-21 | **Оригинальный договор П240** | `06-documents/.../legal/PARK.DOC.020-original-contract-p240 (...).pdf` | `06-documents/.../legal/PARK.DOC.020-original-contract-p240 (...).md` | ok |
| PARK.DOC.019 | 2026-02-03 | **ДС1 расчёт конструкций** (80 000 ₽, НЕ ПОДПИСАН) | `06-documents/.../legal/PARK.DOC.019-ds1-construction-calculation (...).pdf` | `06-documents/.../legal/PARK.DOC.019-ds1-construction-calculation (...).md` | ok |
| PARK.DOC.015 | 2026-03-31 | **ДС2 АР полный и ПЗ** (224 772 ₽) | `06-documents/.../legal/PARK.DOC.015-ds2-ar-full-pz (...).pdf` | `06-documents/.../legal/PARK.DOC.015-ds2-ar-full-pz (...).md` | ok |
| PARK.DOC.017 | 2026-04-02 | **АВР №1** к ДС2 (224 772 ₽, ПОДПИСАН) | `06-documents/.../legal/PARK.DOC.017-avr1-invoices (...).pdf` | `06-documents/.../legal/PARK.DOC.017-avr1-invoices (...).md` | ok |
| PARK.DOC.016 | 2026-04-02 | ДС3 пакет РНС (черновик) | `06-documents/.../legal/PARK.DOC.016-ds3-rns-package (...).docx` | `06-documents/.../legal/PARK.DOC.016-ds3-rns-package (...).md` | ok |
| PARK.DOC.023 | 2026-04-09 | **ДС3 пакет РНС** (525 000 ₽, финальная версия, ПОДПИСАН) | `06-documents/.../legal/PARK.DOC.023-ds3-rns-package-april9 (...).pdf` | `06-documents/.../legal/PARK.DOC.023-ds3-rns-package-april9 (...).md` | ok |
| PARK.DOC.024 | 2026-04-09 | ДС2 повторно (справочная копия) | `06-documents/.../legal/PARK.DOC.024-ds2-ar-full-pz-resend-april9 (...).pdf` | `06-documents/.../legal/PARK.DOC.024-ds2-ar-full-pz-resend-april9 (...).md` | ok |
| PARK.DOC.001 | — | Реквизиты ООО Терра | `06-documents/.../legal/реквизиты Терра.pdf` | `06-documents/.../legal/PARK.DOC.001-requisites-terra (...).md` | ok |
| PARK.DOC.002 | — | Выписка ЕГРН | `06-documents/.../legal/Выписка из егрн.pdf` | `06-documents/.../legal/PARK.DOC.002-egrn-extract (...).md` | ok |
| PARK.DOC.003 | — | Договор аренды земли | `06-documents/.../legal/Парк Аренда Участка.pdf` | `06-documents/.../legal/PARK.DOC.003-land-lease-contract (...).md` | ok |
| PARK.DOC.018 | 2026-04-03 | Выжимка разговора с Еленой | источник в переписке | `06-documents/.../legal/PARK.DOC.018-elena-conversation-summary.md` | card-only |

### Source hints для PARK.DOC.015-020

Для этих позиций на текущий момент установлено:
- карточки есть и содержат анализ
- оригиналы `ДС1/ДС2/ДС3/АВР1` найдены и зеркально сохранены в `06-documents (...)/legal/`
- исходный `П240` найден, подтверждён и зеркально сохранён в `06-documents (...)/legal/`
- в `04-work-products/PARK.WP.005-telegram-export/files/` явных файлов `ДС1/ДС2/ДС3/П240/АВР` нет
- основными источниками сейчас выступают:
  - `PARK.COMM.011`
  - `PARK.COMM.012`
  - `PARK.COMM.014`
  - `PARK.WP.025`
  - `PARK.WP.026`
  - `PARK.WP.005-telegram-export/result.json`

Дополнительно подтверждено по Telegram-экспорту:
- `2026-01-14` есть явное сообщение: «Стоимость расчёта конструкций 80 000 рублей»
- `2026-02-24` есть сообщения о том, что расчёт конструкций на финальном этапе и затем начнётся стадия П

Вывод:
- физические оригиналы `ДС1/ДС2/ДС3/АВР1/П240` уже лежат внутри Pack
- для юридического блока ЛУКС Pack теперь самодостаточен: есть и оригиналы, и карточки, и OCR-слой

## Архитектурные документы

| ID | Тема | Оригинал | Карточка | Статус |
|---|---|---|---|---|
| PARK.DOC.007 | Архитектурный проект | `06-documents/.../architectural/PARK.WP.001-architectural-project (Архитектурный проект Голубинка).pdf` | `06-documents/.../architectural/PARK.DOC.007-architectural-project (...).md` | ok |
| PARK.DOC.008 | ГПЗУ участок | `06-documents/.../architectural/PARK.WP.002-land-plan (ГПЗУ участок).pdf` | `06-documents/.../architectural/PARK.DOC.008-land-plan (...).md` | ok |
| PARK.DOC.009 | План 1 этаж | `06-documents/.../architectural/PARK.WP.003-floor-plan (План 1 этаж).pdf` | `06-documents/.../architectural/PARK.DOC.009-floor-plan (...).md` | ok |
| PARK.DOC.010 | Планировки участка | `06-documents/.../architectural/PARK.WP.012-site-layout (Планировки участка).pdf` | `06-documents/.../architectural/PARK.DOC.010-site-layout (...).md` | ok |
| PARK.DOC.011 | Карта зонирования | `06-documents/.../architectural/PARK.WP.013-zoning-map (Карта градостроительного зонирования).pdf` | `06-documents/.../architectural/PARK.DOC.011-zoning-map (...).md` | ok |
| PARK.DOC.014 | Эскизы кофейни 1-10 | `06-documents/.../architectural/eskizy/*.jpg` | `06-documents/.../architectural/PARK.DOC.014-sketches (...).md` | ok |
| PARK.WP.020 | Отдел архитектуры | `06-documents/.../architectural/PARK.WP.020-architecture-department.pdf` | `06-documents/.../architectural/PARK.WP.020-architecture-department (Отдел архитектуры).md` | ok |
| PARK.WP.027 | Подсчёт площадей 1 этаж | `06-documents/.../architectural/PARK.WP.027-area-calculation-floor-1 (Подсчёт площадей 1 этаж).pdf` | `06-documents/.../architectural/PARK.WP.027-area-calculation-floor-1 (...).md` | ok |
| PARK.WP.028 | Подсчёт площадей 2 этаж | `06-documents/.../architectural/PARK.WP.028-area-calculation-floor-2 (Подсчёт площадей 2 этаж).pdf` | `06-documents/.../architectural/PARK.WP.028-area-calculation-floor-2 (...).md` | ok |

## Графики и административные документы

| ID | Дата | Тема | Оригинал | Карточка | Статус |
|---|---|---|---|---|---|
| PARK.DOC.012 | — | График РНС без АГО | `06-documents/.../administrative/График_для_получения_РНС_без_АГО_.xlsx` | `06-documents/.../administrative/PARK.DOC.012-schedule-rns-no-ago (...).md` | ok |
| PARK.DOC.013 | — | График РНС с АГО | `06-documents/.../administrative/График для получения РНС АГО..xlsx` | `06-documents/.../administrative/PARK.DOC.013-schedule-rns-with-ago (...).md` | ok |
| PARK.DOC.014 | 2026-03-26 | График РНС скорректированный | `06-documents/.../administrative/PARK.WP.019-construction-schedule-golubinka.xlsx` | `06-documents/.../administrative/PARK.DOC.014-schedule-updated-march26 (...).md` | ok |
| PARK.DOC.021 | 2026-04-08 | График РНС с АГО 08 апреля 2026 | `06-documents/.../administrative/PARK.DOC.021-schedule-rns-with-ago-april8 (...).xlsx` | `06-documents/.../administrative/PARK.DOC.021-schedule-rns-with-ago-april8 (...).md` | ok |
| PARK.DOC.022 | 2026-04-09 | **График РНС с АГО 09 апреля 2026** (финальная версия) | `06-documents/.../administrative/PARK.DOC.022-schedule-rns-with-ago-april9 (...).pdf` | `06-documents/.../administrative/PARK.DOC.022-schedule-rns-with-ago-april9 (...).md` | ok |
| PARK.DOC.025 | 2026-04-11 | Черновик заявления на согласование АГО | рабочий черновик | `06-documents/.../administrative/PARK.DOC.025-draft-ago-application-bahchisaray (...).md` | draft |
| PARK.DOC.026 | 2026-04-11 | Перечень приложений к заявлению на АГО | рабочий список | `06-documents/.../administrative/PARK.DOC.026-ago-submission-attachments-list (...).md` | draft |
| PARK.DOC.027 | 2026-04-11 | Заявление на АГО для печати | print-ready версия | `06-documents/.../administrative/PARK.DOC.027-ago-application-print-ready (...).md` | draft |
| PARK.DOC.028 | 2026-04-11 | Приложения к заявлению на АГО для печати | print-ready версия | `06-documents/.../administrative/PARK.DOC.028-ago-attachments-print-ready (...).md` | draft |
| PARK.DOC.029 | 2026-04-11 | Google Doc заявления на АГО | Google Doc: `19kceQ7z7xRDJ-asfcqhh9ma-HO-VkrmCO3-GiYlJYTs` | `06-documents/.../administrative/PARK.DOC.029-ago-application-google-doc (...).md` | active |
| PARK.DOC.033 | 2026-04-16 | **Заявление на АГО финальное** | Google Doc: `1_7KGTFFi6tDw_S4Bf-FGmbEsfLQIhkHP3LHMHTZPC2A` | `06-documents/.../administrative/PARK.DOC.033-ago-application-final (...).md` | submitted |
| PARK.DOC.034 | 2026-04-16 | **Сопроводительное письмо АГО финальное** | Google Doc: `1iREjRjFoKq1CEUKJDZTqHBVlYpodX1uMh11VVXQkPyM` | `06-documents/.../administrative/PARK.DOC.034-ago-cover-letter-final (...).md` | submitted |

## Финансовые документы (счета, платежи)

| Дата | Документ | Сумма | Статус оплаты | Связь |
|---|---|---|---|---|
| 2025-07-21 | Аванс по П240 | 200 000 ₽ | ✅ Оплачен | PARK.DOC.020 |
| 2026-04-02 | Счёт №74 (доплата по ДС2) | 24 772 ₽ | ✅ Оплачен 10.04.2026 | PARK.DOC.017, PARK.COMM.021 |
| 2026-04-02 | Счёт №75 (аванс по ДС3) | 262 500 ₽ | ✅ Оплачен 10.04.2026 | PARK.DOC.017, PARK.COMM.021 |

**Итого оплачено:** 487 272 ₽ из 1 005 000 ₽ (П240 400к + ДС1 80к + ДС2 225к + ДС3 525к - аванс 200к = 1 030к, но ДС1 не подписан)

## Технические документы

| ID | Тема | Оригинал | Карточка | Статус |
|---|---|---|---|---|
| PARK.DOC.005 | Геологические изыскания | `06-documents/.../technical/PARK.WP.011-geology-survey (Геологические изыскания).pdf` | `06-documents/.../technical/PARK.DOC.005-geology-survey (...).md` | ok |
| PARK.DOC.006 | Электропроект | `06-documents/.../technical/PARK.WP.009-electrical-project (Электропроект).pdf` | `06-documents/.../technical/PARK.DOC.006-electrical-project (...).md` | ok |
| PARK.WP.008 | ТЗ на кухню | `06-documents/.../technical/PARK.WP.008-kitchen-specification (ТЗ на кухню).docx` | нет | original-only |
| PARK.WP.015 | Отчёт по геологии | `06-documents/.../technical/PARK.WP.015-geology-report.pdf` | `06-documents/.../technical/PARK.WP.015-geology-report (Отчёт по геологии).md` | ok |
| PARK.WP.016 | Акт геологических изысканий | `06-documents/.../technical/PARK.WP.016-geology-act.docx` | `06-documents/.../technical/PARK.WP.016-geology-act (Акт геологических изысканий).md` | ok |

## Рабочие продукты по активным блокерам

| ID | Дата | Тема | Оригинал | Карточка | Статус |
|---|---|---|---|---|---|
| PARK.WP.041 | 2026-04-19 | Канализационная труба — статус, официальный verdict, следующий шаг | — | `04-work-products/.../PARK.WP.041-sewage-pipe-status-and-expert-next-step (...).md` | active |

## Внешние и не-нормализованные оригиналы

Есть ещё важные оригиналы без нормализованных карточек или с неочевидной связью:
- `administrative/RNS_meeting_document_v2.pdf`
- `administrative/RNS_документ для встречи.pdf`
- `administrative/answer_question1_konstantin.docx`
- `administrative/answers_all_konstantin_questions.docx`
- `administrative/Интересы.pdf`
- `administrative/Парк Документы.pdf`
- `administrative/таблица от Елены Лукс.png`
- `architectural/Градостроительный План Парк.pdf`
- `architectural/ОТДЕЛ ПО ВОПРОСАМ АРХИТЕКТУРЫ,.pdf`
- `technical/Вода Крыма.pdf`
- `technical/Крым энерго терра.pdf`

## Следующий слой доработки

1. Досоздать карточки для `original-only`
2. Развести `PARK.WP.019` и `PARK.WP.026`, где под одним номером сейчас больше одного файла
3. Добавить столбец `source` / `superseded` / `active`
4. Перейти к полной `TELEGRAM-TIMELINE` из сырого экспорта
