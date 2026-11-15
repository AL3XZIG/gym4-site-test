# Gymnasium No. 4 — website redesign

Проект редизайна сайта МБОУ г. Астрахани «Гимназия №4».

- demo/ — статическая демонстрация для GitHub Pages.
- docs/ARCHITECTURE.md — целевая архитектура полноценного сайта.
- docs/PYTHON_SCRIPT_AUDIT.md — разбор исходных Python-генераторов.
- Qwen_python_*.py и Qwen_html_*.html — исходные итерации, сохранённые для истории.

Локальный запуск: перейти в demo/, выполнить python build_demo.py, затем python -m http.server 8000 --directory site.

> Это не официальный сайт гимназии. Новости и сведения в макете необходимо проверить и согласовать. Форма не отправляет и не сохраняет введённые данные.

GitHub Pages используется только для демонстрации. Production-система описана в docs/ARCHITECTURE.md.
