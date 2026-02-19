# 📁 Google Drive Синхронизация — Полная инструкция

**Дата:** 2026-02-19
**Версия:** 2.0

---

## 🎯 Что это?

**Google Drive → VK-offee** — автоматическая синхронизация документов из Google Drive в репозиторий VK-offee.

**Зачем?**
- Менеджер работает в Google Drive (создаёт документы, таблицы)
- Ты работаешь в Google Drive (составляешь документы)
- Telegram-бот и AI-агенты работают с GitHub
- Нужна автоматическая синхронизация между ними

---

## 📦 Архитектура

### Поток данных:

```
Google Drive (источник)
    ↓ sync_google_drive_v2.py
knowledge-base/ (рабочие документы)
    ↓ Telegram-бот / AI-агенты
Ответы пользователям
```

### Роль в Pack/Downstream:

**Google Drive** → **knowledge-base/** → часть **Pack** (VK-offee)

- Google Drive — источник рабочих документов
- knowledge-base/ — синхронизированная копия
- content/ — формализованное знание (Pack)

---

## ✅ Текущий статус

### Что уже настроено:

1. ✅ **Google Cloud Project** — создан
2. ✅ **Google Drive API** — включён
3. ✅ **OAuth 2.0 credentials** — настроены
4. ✅ **token.pickle** — авторизация выполнена
5. ✅ **Скрипт sync_google_drive.py** — работает
6. ✅ **Последняя синхронизация** — 19.02.2026

### Что нужно улучшить:

1. ⚠️ **Кодировка** — файлы сохраняются в неправильной кодировке
2. ⚠️ **Версия скрипта** — старая версия без UTF-8
3. ⚠️ **Автоматизация** — нет автоматического запуска

---

## 🔧 Улучшения (версия 2.0)

### Что добавлено:

**1. Автоматическое исправление кодировки**
- Определение кодировки файла (chardet)
- Конвертация в UTF-8
- Статистика исправлений

**2. Улучшенная обработка Google Docs**
- Google Docs → Markdown (.md)
- Google Sheets → CSV (.csv)
- Google Slides → PDF (.pdf)

**3. Детальная статистика**
- Скачано файлов
- Обновлено файлов
- Исправлено кодировок
- Размер данных

**4. Отчёты в отдельной папке**
- `knowledge-base/sync-reports/sync-YYYY-MM-DD.md`
- Не засоряют основную папку

**5. Проверка изменений**
- Скачивает только изменённые фа��лы
- Экономит время и трафик

---

## 🚀 Как использовать

### Вариант 1: Ручной запуск (сейчас)

```bash
cd ~/VK-offee/.github/scripts
python3 sync_google_drive_v2.py
```

**Что произойдёт:**
1. Подключение к Google Drive API
2. Получение списка файлов из папки
3. Скачивание новых/изменённых файлов
4. Исправление кодировки в UTF-8
5. Создание отчёта

**Время:** 2-5 минут (зависит от количества файлов)

### Вариант 2: Автоматический запуск (настроить)

**Через cron (macOS/Linux):**

```bash
# Редактировать crontab
crontab -e

# Добавить строку (каждый день в 9:00)
0 9 * * * cd ~/VK-offee/.github/scripts && python3 sync_google_drive_v2.py >> ~/VK-offee/sync.log 2>&1
```

**Через GitHub Actions (в облаке):**

Создать `.github/workflows/sync-drive.yml`:

```yaml
name: Sync Google Drive

on:
  schedule:
    - cron: '0 9 * * *'  # Каждый день в 9:00 UTC
  workflow_dispatch:  # Ручной запуск

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd .github/scripts
          pip install -r requirements.txt
      - name: Sync Google Drive
        env:
          GOOGLE_CREDENTIALS: ${{ secrets.GOOGLE_CREDENTIALS }}
        run: |
          cd .github/scripts
          python3 sync_google_drive_v2.py
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add knowledge-base/
          git commit -m "Sync: Google Drive $(date +'%Y-%m-%d')" || exit 0
          git push
```

---

## 🔑 Доступ к Google Drive

### Текущая настройка:

**Папка:** `120x7kqYeV0Vb4TLbdCC0esv0WkF5JROC`

**Доступ:**
- ✅ Чтение (readonly)
- ❌ Запись (не нужна)

### Как дать доступ к новой папке:

1. Открой Google Drive
2. Найди папку
3. Нажми "Поделиться"
4. Добавь email из `credentials.json`:
   ```
   550308637496-9tgi2g8fj3nns74l9khua18f6bisnb80@developer.gserviceaccount.com
   ```
5. Дай права "Читатель"
6. Скопируй ID папки из URL:
   ```
   https://drive.google.com/drive/folders/[ID_ПАПКИ]
   ```
7. Обнови переменную в скрипте или `.env`:
   ```bash
   export GOOGLE_DRIVE_FOLDER_ID="новый_ID"
   ```

---

## 📋 Что синхронизируется?

### Типы файлов:

| Тип в Google Drive | Формат в GitHub | Обработка |
|-------------------|-----------------|-----------|
| Google Docs | .md (Markdown) | Экспорт в текст |
| Google Sheets | .csv | Экспорт в CSV |
| Google Slides | .pdf | Экспорт в PDF |
| .docx, .xlsx | Как есть | Прямое скачивание |
| .pdf, .jpg, .png | Как есть | Прямое скачивание |
| .md, .txt | .md, .txt | Скачивание + исправление кодировки |

### Структура папок:

Google Drive сохраняет структуру папок:

```
Google Drive:
  └── База знаний ВК
      ├── БАР/
      ├── КУХНЯ/
      └── Персонал/

GitHub:
  └── knowledge-base/
      ├── БАР/
      ├── КУХНЯ/
      └── Персонал/
```

---

## 🔧 Исправление существующих файлов

### Проблема:

Старые файлы в `knowledge-base/` имеют неправильную кодировку (WINDOWS-1251 вместо UTF-8).

### Решение:

**Запустить скрипт исправления:**

```bash
cd ~/VK-offee/.github/scripts
python3 fix_encoding.py
```

**Что произойдёт:**
1. Создание резервной копии `knowledge-base-backup-YYYYMMDD-HHMMSS/`
2. Определение кодировки каждого файла
3. Конвертация в UTF-8
4. Статистика исправлений

**Время:** 5-10 минут

**Безопасно:** Создаётся резервная копия перед изменениями

---

## 📊 Отчёты синхронизации

### Где находятся:

```
knowledge-base/sync-reports/sync-YYYY-MM-DD.md
```

### Что содержат:

```markdown
# Отчёт о синхронизации

**Дата:** 19.02.2026, 09:09:48
**Длительность:** 204.26 сек
**Скачано:** 66 файлов
**Ошибок:** 3

## 📥 Скачанные файлы

- БАР/Меню/меню-холодные-напитки.csv
- КУХНЯ/Рецепты/салаты.md
- Персонал/Вакансии/бариста.md

## ⚠️ Ошибки

- Файл X: ошибка доступа
- Файл Y: неподдерживаемый формат
```

---

## 🎯 План действий

### Сейчас (30 минут):

**1. Исправить кодировку существующих файлов**

```bash
cd ~/VK-offee/.github/scripts
python3 fix_encoding.py
```

**2. Запустить новую версию синхронизации**

```bash
python3 sync_google_drive_v2.py
```

**3. Проверить результат**

```bash
# Проверить, что файлы читаются правильно
cat ~/VK-offee/knowledge-base/БАР/Меню/меню.md
```

**4. Протестировать Telegram-бота**

```bash
cd ~/VK-offee/telegram-bot
./start.sh
```

### Потом (опционально):

**1. Настроить автоматическую синхронизацию**
- Через cron (локально)
- Через GitHub Actions (в облаке)

**2. Добавить webhook**
- Google Drive уведомляет о изменениях
- Автоматический запуск синхронизации

---

## ✅ Чек-лист готовности

Перед запуском проверь:

- [ ] credentials.json существует
- [ ] token.pickle существует (авторизация выполнена)
- [ ] Python 3.8+ установлен
- [ ] Библиотеки установлены (`pip install -r requirements.txt`)
- [ ] Доступ к Google Drive папке есть
- [ ] knowledge-base/ папка существует

---

## 🚨 Troubleshooting

### Ошибка: "credentials.json не найден"

**Решение:**
1. Скачай credentials.json из Google Cloud Console
2. Положи в `.github/scripts/credentials.json`

### Ошибка: "Access denied"

**Решение:**
1. Проверь, что папка расшарена на email из credentials
2. Проверь ID папки в переменной `GOOGLE_DRIVE_FOLDER_ID`

### Ошибка: "Кракозябры в файлах"

**Решение:**
1. Запусти `fix_encoding.py`
2. Используй `sync_google_drive_v2.py` (новая версия с UTF-8)

### Ошибка: "Token expired"

**Решение:**
1. Удали `token.pickle`
2. Запусти скрипт снова — откроется браузер для авторизации

---

## 📞 Что ��альше?

**Готов запустить синхронизацию?**

Скажи:
1. "Исправь кодировку" — я запущу fix_encoding.py
2. "Запусти синхронизацию" — я запущу sync_google_drive_v2.py
3. "Настрой автоматизацию" — я настрою cron или GitHub Actions

**Или делаем всё сразу?**
