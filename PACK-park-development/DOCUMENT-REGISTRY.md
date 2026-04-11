# DOCUMENT-REGISTRY — Парк Голубинка

> Реестр оригиналов, markdown-карточек и рабочих артефактов по проекту.

## Как читать

- `Оригинал` — физический файл: `pdf`, `docx`, `xlsx`, `jpg`, `txt`, `json`
- `Карточка` — markdown-описание, которое агент читает первым
- `Статус`:
  - `ok` — оригинал и карточка есть
  - `card-only` — есть карточка, оригинал надо ещё точно привязать
  - `original-only` — оригинал есть, карточки ещё нет
  - `mixed` — есть несколько связанных файлов, нужна дальнейшая нормализация

## Юридические документы

| ID | Тема | Оригинал | Карточка | Статус |
|---|---|---|---|---|
| PARK.DOC.001 | Реквизиты ООО Терра | `06-documents/.../legal/реквизиты Терра.pdf` | `06-documents/.../legal/PARK.DOC.001-requisites-terra (Реквизиты ООО Терра).md` | ok |
| PARK.DOC.002 | Выписка ЕГРН | `06-documents/.../legal/Выписка из егрн.pdf` | `06-documents/.../legal/PARK.DOC.002-egrn-extract (Выписка из ЕГРН).md` | ok |
| PARK.DOC.003 | Договор аренды земли | `06-documents/.../legal/Парк Аренда Участка.pdf` | `06-documents/.../legal/PARK.DOC.003-land-lease-contract (Договор аренды земли).md` | ok |
| PARK.DOC.004 | Договор с архитектором | `06-documents/.../legal/PARK.WP.004-architect-contract (Договор с архитектором Лукс).pdf` | `06-documents/.../legal/PARK.DOC.004-architect-contract (Договор с архитектором).md` | ok |
| PARK.DOC.015 | ДС2 АР полный и ПЗ | `06-documents/.../legal/PARK.DOC.015-ds2-ar-full-pz (ДС2 АР полный и ПЗ 31 марта 2026).pdf` | `06-documents/.../legal/PARK.DOC.015-ds2-ar-full-pz (...).md` | ok |
| PARK.DOC.016 | ДС3 пакет РНС | `06-documents/.../legal/PARK.DOC.016-ds3-rns-package (ДС3 пакет документов для РНС 07 апреля 2026).docx`, `06-documents/.../legal/PARK.DOC.016-ds3-rns-package-and-invoice (ДС3 пакет документов и счёт 02 апреля 2026).pdf` | `06-documents/.../legal/PARK.DOC.016-ds3-rns-package (...).md` | ok |
| PARK.DOC.017 | АВР1 и счета 74/75 | `06-documents/.../legal/PARK.DOC.017-avr1-and-invoices (АВР1 и счета 74 75 от 02 апреля 2026).pdf` | `06-documents/.../legal/PARK.DOC.017-avr1-invoices (...).md` | ok |
| PARK.DOC.018 | Выжимка разговора с Еленой | источник в переписке | `06-documents/.../legal/PARK.DOC.018-elena-conversation-summary.md` | card-only |
| PARK.DOC.019 | ДС1 расчёт конструкций | `06-documents/.../legal/PARK.DOC.019-ds1-construction-calculation (ДС1 расчёт конструкций 03 февраля 2026).pdf`, `06-documents/.../legal/PARK.DOC.019-ds1-advance-invoice (Счёт аванс расчёт конструкций 05 февраля 2026).pdf` | `06-documents/.../legal/PARK.DOC.019-ds1-construction-calculation (...).md` | ok |
| PARK.DOC.020 | Оригинальный договор П240 | `06-documents/.../legal/PARK.DOC.020-original-contract-p240 (Оригинальный договор П240 от 21 июля 2025).pdf` | `06-documents/.../legal/PARK.DOC.020-original-contract-p240 (...).md` | ok |
| PARK.DOC.023 | ДС3 пакет РНС 09 апреля 2026 | `06-documents/.../legal/PARK.DOC.023-ds3-rns-package-april9 (ДС3 пакет документов для РНС 09 апреля 2026).pdf` | `06-documents/.../legal/PARK.DOC.023-ds3-rns-package-april9 (...).md` | ok |
| PARK.DOC.024 | ДС2 повторно от 09 апреля 2026 | `06-documents/.../legal/PARK.DOC.024-ds2-ar-full-pz-resend-april9 (ДС2 АР полный и ПЗ повторно от 09 апреля 2026).pdf` | `06-documents/.../legal/PARK.DOC.024-ds2-ar-full-pz-resend-april9 (...).md` | ok |
| PARK.DOC.025 | Черновик заявления на согласование АГО | рабочий черновик под Бахчисарай и ООО «ТЕРРА» | `06-documents/.../administrative/PARK.DOC.025-draft-ago-application-bahchisaray (...).md` | draft |
| PARK.DOC.026 | Перечень приложений к заявлению на АГО | рабочий список для подачи | `06-documents/.../administrative/PARK.DOC.026-ago-submission-attachments-list (...).md` | draft |
| PARK.DOC.027 | Заявление на АГО для печати | локальная print-ready версия заявления | `06-documents/.../administrative/PARK.DOC.027-ago-application-print-ready (...).md` | draft |
| PARK.DOC.028 | Приложения к заявлению на АГО для печати | локальная print-ready версия списка приложений | `06-documents/.../administrative/PARK.DOC.028-ago-attachments-print-ready (...).md` | draft |
| PARK.DOC.029 | Google Doc заявления на АГО | `Google Doc`: `19kceQ7z7xRDJ-asfcqhh9ma-HO-VkrmCO3-GiYlJYTs` | `06-documents/.../administrative/PARK.DOC.029-ago-application-google-doc (...).md` | active |
| PARK.WP.017 | Договор аренды земли | `06-documents/.../legal/PARK.WP.017-land-lease-contract.pdf` | `06-documents/.../legal/PARK.WP.017-land-lease-contract (Договор аренды земли).md` | ok |
| PARK.WP.018 | Выписка ЕГРН | `06-documents/.../legal/PARK.WP.018-egrn-extract.pdf` | `06-documents/.../legal/PARK.WP.018-egrn-extract (Выписка ЕГРН).md` | ok |

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

## Административные документы и рабочие продукты

| ID | Тема | Оригинал | Карточка | Статус |
|---|---|---|---|---|
| PARK.DECISION.001 | Решение по АГО | источник в анализе/переговорах | `06-documents/.../administrative/PARK.DECISION.001-ago-position (Решение по АГО).md` | card-only |
| PARK.DOC.012 | График РНС без АГО | `06-documents/.../administrative/График_для_получения_РНС_без_АГО_.xlsx` | `06-documents/.../administrative/PARK.DOC.012-schedule-rns-no-ago (...).md` | ok |
| PARK.DOC.013 | График РНС с АГО | `06-documents/.../administrative/График для получения РНС АГО..xlsx` | `06-documents/.../administrative/PARK.DOC.013-schedule-rns-with-ago (...).md` | ok |
| PARK.DOC.014 | График РНС скорректированный | `06-documents/.../administrative/PARK.WP.019-construction-schedule-golubinka.xlsx` | `06-documents/.../administrative/PARK.DOC.014-schedule-updated-march26 (...).md` | ok |
| PARK.DOC.021 | График РНС с АГО 08 апреля 2026 | `06-documents/.../administrative/PARK.DOC.021-schedule-rns-with-ago-april8 (График РНС с АГО 08 апреля 2026).xlsx` | `06-documents/.../administrative/PARK.DOC.021-schedule-rns-with-ago-april8 (...).md` | ok |
| PARK.DOC.022 | График РНС с АГО 09 апреля 2026 | `06-documents/.../administrative/PARK.DOC.022-schedule-rns-with-ago-april9 (График РНС с АГО 09 апреля 2026).pdf` | `06-documents/.../administrative/PARK.DOC.022-schedule-rns-with-ago-april9 (...).md` | ok |
| PARK.WP.005 | Telegram correspondence JSON | `06-documents/.../administrative/PARK.WP.005-telegram-correspondence (Переписка Telegram).json` | нет | original-only |
| PARK.WP.007 | Пояснительная записка | `06-documents/.../administrative/PARK.WP.007-explanatory-note (Пояснительная записка).docx` | нет | original-only |
| PARK.WP.010 | Градостроительные регламенты | `06-documents/.../administrative/PARK.WP.010-urban-regulations (Градостроительные регламенты).docx` | нет | original-only |
| PARK.WP.014 | Регламент выдачи согласований | `06-documents/.../administrative/PARK.WP.014-approval-regulations (Регламент выдачи согласований).pdf` | нет | original-only |
| PARK.WP.017 | Вопросы и ответы архитектору | `06-documents/.../administrative/PARK.WP.017-konstantin-questions-answers.docx` | `06-documents/.../administrative/PARK.WP.017-konstantin-questions-answers (Вопросы и ответы архитектору).md` | ok |
| PARK.WP.019 | Документы парка / construction schedule | `06-documents/.../administrative/PARK.WP.019-park-documents.pdf`, `.../PARK.WP.019-construction-schedule-golubinka.xlsx` | `06-documents/.../administrative/PARK.WP.019-park-documents (Документы парка).md` | mixed |
| PARK.WP.021 | План действий по РНС | нет | `06-documents/.../administrative/PARK.WP.021-rns-action-plan (План действий по РНС).md` | card-only |
| PARK.WP.022 | Письмо Константину | нет | `06-documents/.../administrative/PARK.WP.022-letter-to-konstantin (Письмо архитектору Константину).md` | card-only |
| PARK.WP.023 | Сообщение Константину в Telegram | нет | `06-documents/.../administrative/PARK.WP.023-telegram-message-konstantin (Сообщение архитектору в Telegram).md` | card-only |
| PARK.WP.024 | Письмо архитекторам: подготовка к строительству | нет | `06-documents/.../administrative/PARK.WP.024-letter-construction-preparation (Письмо архитекторам: подготовка к строительству).md` | card-only |
| PARK.WP.025 | Стратегия по ЛУКС | нет | `06-documents/.../administrative/PARK.WP.025-luks-strategy.md` | card-only |
| PARK.WP.026 | Письма/черновики по ЛУКС | нет | `06-documents/.../administrative/PARK.WP.026-draft-message-luks.md`, `.../PARK.WP.026-letter-to-luks-discrepancies.md` | card-only |

## Технические документы

| ID | Тема | Оригинал | Карточка | Статус |
|---|---|---|---|---|
| PARK.DOC.005 | Геологические изыскания | `06-documents/.../technical/PARK.WP.011-geology-survey (Геологические изыскания).pdf` | `06-documents/.../technical/PARK.DOC.005-geology-survey (...).md` | ok |
| PARK.DOC.006 | Электропроект | `06-documents/.../technical/PARK.WP.009-electrical-project (Электропроект).pdf` | `06-documents/.../technical/PARK.DOC.006-electrical-project (...).md` | ok |
| PARK.WP.008 | ТЗ на кухню | `06-documents/.../technical/PARK.WP.008-kitchen-specification (ТЗ на кухню).docx` | нет | original-only |
| PARK.WP.015 | Отчёт по геологии | `06-documents/.../technical/PARK.WP.015-geology-report.pdf` | `06-documents/.../technical/PARK.WP.015-geology-report (Отчёт по геологии).md` | ok |
| PARK.WP.016 | Акт геологических изысканий | `06-documents/.../technical/PARK.WP.016-geology-act.docx` | `06-documents/.../technical/PARK.WP.016-geology-act (Акт геологических изысканий).md` | ok |

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
