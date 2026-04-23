---
type: work-product
domain: management
wp_id: MGMT.WP.018
status: ready
created: 2026-04-23
---

# MGMT.WP.018 — FPF -> SRT -> SPF pass по PACK-management

## FPF

- `domain`: `management`
- `subdomain`: `cafe-management / readiness / change-coordination`
- `boundary`:
  - здесь живут управленческие решения и factual events про готовность точки,
    ремонты, переезды, запуск зон и крупные координационные изменения;
  - здесь не живут узкие операционные регламенты бара, кухни и сервиса.
- `not-this-domain`:
  - приготовление напитков -> `PACK-bar`
  - приготовление блюд -> `PACK-kitchen`
  - обслуживание гостей -> `PACK-service`
  - найм/увольнение -> `PACK-hr`
- `source-of-truth`:
  - для `repair / readiness / relocation / launch / major equipment` —
    `PACK-management`

## SRT

- `placement`: management-layer над operational domains
- `why here`:
  - этот слой держит координацию между доменами, а не работу одного цеха;
  - события ремонта кухни и покупки машины для обучения влияют сразу на несколько
    operational contours и не должны иметь первичный домен в `PACK-kitchen`
    или `barista-class`.
- `doubtful placements`:
  - факт новой машины должен эхом отражаться в `barista-class`;
  - статус готовности кухни должен эхом отражаться в `PACK-kitchen`.

## SPF

- `role-card`:
  - `MGMT.ROLE.001-cafe-manager`
- `registry / wp / context`:
  - `WP-106`
  - `MGMT.WP.018`
- `acceptance`:
  - management-domain расширен до роли `управляющего кофейней`;
  - новые factual updates типа `ремонт / readiness / launch` дальше можно вести
    здесь как primary layer.

## Truthful verdict

`PACK-management` существовал и раньше, но был раздвоен между:

- `shift-management`;
- общим `management draft`;
- отдельными управленческими артефактами без чёткой границы.

После этого pass домен различён так:

- ядро: управленческий контур кофейни;
- явная роль: `управляющий кофейней`;
- operational Pack остаются downstream-получателями последствий.
