# Статус компонентов v4

Обновлять этот файл после фактической реализации и проверки. Статус документации не равен статусу кода.

Легенда: `PLANNED` — запланировано; `SPECIFIED` — требования описаны; `IN PROGRESS` — код пишется; `IMPLEMENTED` — код есть; `VERIFIED` — тесты пройдены; `BLOCKED` — есть внешняя зависимость.

| Компонент | Статус | Основа / примечание |
|---|---|---|
| Изолированная зона v4 | SPECIFIED | `release/`, ветка `v4-release-work` |
| Инвентаризация v0.3 | PLANNED | нужно проверить все текущие страницы и модули |
| URL migration map | PLANNED | требуется карта маршрутов и redirects |
| Django core v4 | PLANNED | существующий `server/` сначала аудировать |
| CMS pages | SPECIFIED | модель описана в DATA_MODEL.md, кода v4 ещё нет |
| CMS news | SPECIFIED | модель описана в DATA_MODEL.md, кода v4 ещё нет |
| Documents / media | SPECIFIED | нужна безопасная загрузка и review |
| Editorial workflow | SPECIFIED | draft → review → publish |
| Role permissions | SPECIFIED | нужны object-level tests |
| Public frontend | PLANNED | текущий сайт — дизайн/контентный reference |
| Search | PLANNED | поиск только по опубликованным данным |
| Seasonal effects | PLANNED | переносить после проверки reduced motion |
| Elections integration | PLANNED | существующий модуль требует аудита; бюллетень не реализовывать |
| Playwright E2E | PLANNED | обязательный release gate |
| Docker production build | PLANNED | проверить clean install и restore |
| Content verification | BLOCKED | нужны подтверждения школы и права на медиа |

## Известные решения

- Корневой сайт v0.3 не переписывается в рамках подготовительного этапа.
- Полная CMS — серверная, а не localStorage-редактор.
- Контент и медиа должны проходить публикационный workflow.
- Реальное электронное голосование не входит в v4 по умолчанию.
- GitHub Pages не является production backend.

## Следующий технический шаг

Провести инвентаризацию текущего `server/`, `deploy/`, `assets/` и списка страниц, после чего определить точный объём повторного использования и подготовить каркас Django v4 с отдельными настройками и тестами.
