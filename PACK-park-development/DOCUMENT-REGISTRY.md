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
| PARK.DOC.015 | ДС2 АР полный и ПЗ | путь оригинала ещё уточнить | `06-documents/.../legal/PARK.DOC.015-ds2-ar-full-pz (...).md` | card-only |
| PARK.DOC.016 | ДС3 пакет РНС | путь оригинала ещё уточнить | `06-documents/.../legal/PARK.DOC.016-ds3-rns-package (...).md` | card-only |
| PARK.DOC.017 | АВР1 и счета 74/75 | путь оригинала ещё уточнить | `06-documents/.../legal/PARK.DOC.017-avr1-invoices (...).md` | card-only |
| PARK.DOC.018 | Выжимка разговора с Еленой | источник в переписке | `06-documents/.../legal/PARK.DOC.018-elena-conversation-summary.md` | card-only |
| PARK.DOC.019 | ДС1 расчёт конструкций | путь оригинала ещё уточнить | `06-documents/.../legal/PARK.DOC.019-ds1-construction-calculation (...).md` | card-only |
| PARK.DOC.020 | Оригинальный договор П240 | путь оригинала ещё уточнить | `06-documents/.../legal/PARK.DOC.020-original-contract-p240 (...).md` | card-only |
| PARK.WP.017 | Договор аренды земли | `06-documents/.../legal/PARK.WP.017-land-lease-contract.pdf` | `06-documents/.../legal/PARK.WP.017-land-lease-contract (Договор аренды земли).md` | ok |
| PARK.WP.018 | Выписка ЕГРН | `06-documents/.../legal/PARK.WP.018-egrn-extract.pdf` | `06-documents/.../legal/PARK.WP.018-egrn-extract (Выписка ЕГРН).md` | ok |

### Source hints для PARK.DOC.015-020

Для этих позиций на текущий момент установлено:
- карточки есть и содержат анализ
- прямые оригиналы в `06-documents (...)` не найдены
- в `04-work-products/PARK.WP.005-telegram-export/files/` тоже не найдено явных файлов с именами `ДС1/ДС2/ДС3/П240/АВР`
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
- физические оригиналы `ДС1/ДС2/ДС3/АВР1/П240` нужно либо отдельно дозагрузить в пакет,
- либо извлечь/переименовать из внешнего хранилища и после этого привязать сюда.

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

## Административные документы и рабочие продукты

| ID | Тема | Оригинал | Карточка | Статус |
|---|---|---|---|---|
| PARK.DECISION.001 | Решение по АГО | источник в анализе/переговорах | `06-documents/.../administrative/PARK.DECISION.001-ago-position (Решение по АГО).md` | card-only |
| PARK.DOC.012 | График РНС без АГО | `06-documents/.../administrative/График_для_получения_РНС_без_АГО_.xlsx` | `06-documents/.../administrative/PARK.DOC.012-schedule-rns-no-ago (...).md` | ok |
| PARK.DOC.013 | График РНС с АГО | `06-documents/.../administrative/График для получения РНС АГО..xlsx` | `06-documents/.../administrative/PARK.DOC.013-schedule-rns-with-ago (...).md` | ok |
| PARK.DOC.014 | График РНС скорректированный | `06-documents/.../administrative/PARK.WP.019-construction-schedule-golubinka.xlsx` | `06-documents/.../administrative/PARK.DOC.014-schedule-updated-march26 (...).md` | ok |
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

1. Привязать физические оригиналы для `PARK.DOC.015-020`
2. Досоздать карточки для `original-only`
3. Развести `PARK.WP.019` и `PARK.WP.026`, где под одним номером сейчас больше одного файла
4. Добавить столбец `source` / `superseded` / `active`
