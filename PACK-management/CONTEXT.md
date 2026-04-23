# CONTEXT — PACK-management

> Рабочий контекст для быстрого входа в домен управления кофейней VK-offee.

**Последнее обновление:** 2026-04-23  
**Статус:** active  
**Текущий фокус:** домен различён как management-layer кофейни; роль `управляющего кофейней` materialized и готова принимать factual updates типа `repair / readiness / relocation / launch`.

---

## Краткое summary

`PACK-management` больше не стоит читать только как узкий `shift-management`.

После `FPF -> SRT -> SPF` pass домен различён как:

- управленческий контур кофейни;
- readiness точки и помещений;
- ремонтные работы и сроки;
- переезды, перепланировки и запуск новых зон;
- крупные управленческие закупки оборудования;
- междоменная координация между баром, кухней, сервисом, складом и подрядчиками.

Это значит:

- operational Pack (`bar`, `kitchen`, `service`, `warehouse`) остаются своими
  source-of-truth для узкой работы;
- но события, которые меняют всю систему как объект управления, идут сюда как
  primary layer.

## Что уже materialized

Главные опорные артефакты домена:

1. [00-pack-manifest.md](/Users/alexander/Github/VK-offee/PACK-management/00-pack-manifest.md:1)
2. [MANIFEST.md](/Users/alexander/Github/VK-offee/PACK-management/MANIFEST.md:1)
3. [DOMAIN-MODEL-v1](/Users/alexander/Github/VK-offee/PACK-management/01-domain-contract%20%28%D0%9A%D0%BE%D0%BD%D1%82%D1%80%D0%B0%D0%BA%D1%82%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29/DOMAIN-MODEL-v1%20%28%D0%9E%D0%B1%D1%8A%D0%B5%D0%BA%D1%82%D0%BD%D0%B0%D1%8F%20%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C%20PACK-management%20v1%29.md:1)
4. [MGMT.ROLE.001](/Users/alexander/Github/VK-offee/PACK-management/02-domain-entities%20%28%D0%A1%D1%83%D1%89%D0%BD%D0%BE%D1%81%D1%82%D0%B8%20%D0%B4%D0%BE%D0%BC%D0%B5%D0%BD%D0%B0%29/MGMT.ROLE.001-cafe-manager%20%28%D0%A0%D0%BE%D0%BB%D1%8C%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D1%8F%D1%8E%D1%89%D0%B5%D0%B3%D0%BE%20%D0%BA%D0%BE%D1%84%D0%B5%D0%B9%D0%BD%D0%B5%D0%B9%29.md:1)
5. [MGMT.WP.018](/Users/alexander/Github/VK-offee/PACK-management/04-work-products%20%28%D0%A0%D0%B0%D0%B1%D0%BE%D1%87%D0%B8%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D1%8B%29/MGMT.WP.018-management-domain-fpf-srt-spf-pass%20%28FPF-SRT-SPF%20pass%20%D0%BF%D0%BE%20PACK-management%20%D0%B8%20%D1%80%D0%BE%D0%BB%D0%B8%20%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D1%8F%D1%8E%D1%89%D0%B5%D0%B3%D0%BE%20%D0%BA%D0%BE%D1%84%D0%B5%D0%B9%D0%BD%D0%B5%D0%B9%29.md:1)

## Что считать primary source-of-truth

Именно сюда теперь логично класть:

- ремонт кухни или других зон;
- готовность помещения к запуску;
- переезд / перепланировку;
- запуск новой лаборатории / учебной зоны;
- покупку крупного оборудования, если это не просто локальная замена, а change
  management уровня кофейни.

Примеры secondary echo:

- в `PACK-kitchen` можно отражать влияние ремонта на kitchen operations;
- в `barista-class` можно отражать, что для обучения появилась новая машина;
- но primary management fact должен жить здесь.

## Открытые вопросы

- Нужен ли домену отдельный `PROJECT-TIMELINE` или пока достаточно `CONTEXT + DOCUMENT-REGISTRY`.
- Какие legacy management-артефакты относятся к старому `shift-management`, а какие к новому более широкому `cafe management`.
- Нужен ли отдельный method-layer для:
  - readiness review,
  - ремонтного контроля,
  - launch decision.

## Следующий честный шаг

Отдельным bounded WP завести первые реальные management factual updates:

1. срок плиточных работ по кухне;
2. покупка `Victoria Arduino Eagle One` как management-level equipment fact с эхом в `barista class`.
