# 🔧 Решение: Доступ агентов к Google Sheets

**Проблема:** Агенты не видят Google Spreadsheets, только файлы в GitHub.

**Решение:** Автоматическая синхронизация Google Sheets → CSV → GitHub

---

## 🎯 Архитектура решения

```
Google Sheets (менеджер работает здесь)
    ↓
    ↓ sync-google-sheets.sh (автоматически)
    ↓ Экспорт в CSV
    ↓
knowledge-base/ (локально)
    ↓
    ↓ Git Hook (автоматически)
    ↓
GitHub
    ↓
Все агенты видят! ✅
```

---

## 📋 Список Google Sheets для синхронизации

### Найденные таблицы:

1. **Калькуляции СЕБЕСТОИМОСТЬ КУХНЯ**
   - ID: `1Ai4qUIXpkc1fJ_Cd5Vh-wgPV9a-blOhtQWV_tyqhFTU`
   - Лист: `372408211`
   - Папка: `knowledge-base/КУХНЯ/`

2. **Другие таблицы** (нужно найти):
   - Себестоимость напитков
   - Учёт продуктов
   - График работы
   - И т.д.

---

## 🔧 Скрипт синхронизации

### Создать: `.github/scripts/sync-google-sheets.sh`

```bash
#!/bin/bash
# Автоматическая синхронизация Google Sheets → CSV → GitHub

echo "=========================================="
echo "Google Sheets Sync: $(date)"
echo "=========================================="

# Массив таблиц: "SHEET_ID:GID:НАЗВАНИЕ:ПАПКА"
SHEETS=(
    "1Ai4qUIXpkc1fJ_Cd5Vh-wgPV9a-blOhtQWV_tyqhFTU:372408211:Калькуляции СЕБЕСТОИМОСТЬ КУХНЯ:КУХНЯ"
    # Добавить другие таблицы здесь
)

BASE_PATH="/Users/alexander/VK-offee/knowledge-base"
CHANGED=0

for sheet in "${SHEETS[@]}"; do
    IFS=':' read -r sheet_id gid name folder <<< "$sheet"

    echo "📥 Синхронизация: $name"

    # Путь к файлу
    file_path="$BASE_PATH/$folder/$name.csv"

    # Скачать таблицу
    curl -s -L "https://docs.google.com/spreadsheets/d/${sheet_id}/export?format=csv&gid=${gid}" \
         -o "$file_path.tmp"

    # Проверить, изменился ли файл
    if [ -f "$file_path" ]; then
        if ! cmp -s "$file_path" "$file_path.tmp"; then
            mv "$file_path.tmp" "$file_path"
            echo "  ✅ Обновлён"
            CHANGED=1
        else
            rm "$file_path.tmp"
            echo "  ⏭️  Без изменений"
        fi
    else
        mv "$file_path.tmp" "$file_path"
        echo "  ✅ Создан"
        CHANGED=1
    fi
done

# Если были изменения → коммит и push
if [ $CHANGED -eq 1 ]; then
    echo ""
    echo "📝 Обнаружены изменения, коммичу..."
    cd /Users/alexander/VK-offee
    git add knowledge-base/
    git commit -m "Sync: Google Sheets $(date +'%Y-%m-%d %H:%M')"
    git push origin main
    echo "✅ Изменения отправлены в GitHub"
else
    echo ""
    echo "ℹ️  Нет изменений"
fi

echo "=========================================="
echo "Завершено: $(date)"
echo "=========================================="
```

---

## 🚀 Установка

### Шаг 1: Создать скрипт

```bash
# Создать файл
nano /Users/alexander/VK-offee/.github/scripts/sync-google-sheets.sh

# Вставить содержимое выше

# Сделать исполняемым
chmod +x /Users/alexander/VK-offee/.github/scripts/sync-google-sheets.sh
```

### Шаг 2: Протестировать

```bash
cd /Users/alexander/VK-offee/.github/scripts
./sync-google-sheets.sh
```

### Шаг 3: Добавить в cron

```bash
# Редактировать crontab
crontab -e

# Добавить строку (после синхронизации Google Drive)
5 9 * * * /Users/alexander/VK-offee/.github/scripts/sync-google-sheets.sh >> /Users/alexander/VK-offee/sync-sheets.log 2>&1
```

**Результат:**
- 9:00 — синхронизация Google Drive (файлы)
- 9:05 — синхронизация Google Sheets (таблицы)

---

## 📊 Как найти все Google Sheets?

### Вариант 1: Поиск в файлах

```bash
cd /Users/alexander/VK-offee
grep -r "docs.google.com/spreadsheets" knowledge-base/ | grep -o "d/[^/]*" | sort -u
```

### Вариант 2: Из Реестра документов

```bash
cat knowledge-base/Реестр\ документов\ .csv | grep "spreadsheets"
```

### Вариант 3: Вручную

Попросить менеджера составить список всех Google Sheets, которые используются.

---

## 🔍 Доступ для агентов

### После синхронизации:

**Веб-агент Claude.ai:**
```
"Найди файл Калькуляции СЕБЕСТОИМОСТЬ КУХНЯ.csv
в репозитории https://github.com/alexpoaiagent-sudo/VK-offee
в папке knowledge-base/КУХНЯ/"
```
✅ Найдёт! (CSV в GitHub)

**Локальный агент (я):**
```
"Найди калькуляции кухни"
```
✅ Найдёт! (CSV локально)

**Telegram-бот:**
```
"Покажи калькуляции кухни"
```
✅ Найдёт и покажет данные!

---

## ⚠️ Ограничения

### Что НЕ синхронизируется автоматически:

1. **Google Forms** (формы)
   - Нужен отдельный API
   - Или экспорт ответов в Google Sheets

2. **Google Docs** (документы)
   - Синхронизируются через Google Drive sync
   - Если в папке `120x7kqYeV0Vb4TLbdCC0esv0WkF5JROC`

3. **Приватные таблицы**
   - Нужны права доступа
   - Или публичная ссылка

---

## 📝 Следующие шаги

### Сейчас:

1. **Создать скрипт `sync-google-sheets.sh`**
2. **Найти все Google Sheets** (список ID)
3. **Добавить их в скрипт**
4. **Протестировать**
5. **Добавить в cron**

### Потом:

1. **Настроить синхронизацию Google Forms**
2. **Добавить мониторинг**
3. **Создать dashboard** (какие таблицы синхронизированы)

---

## ✅ Результат

**После настройки:**

```
Менеджер обновляет Google Sheet
    ↓ (автоматически каждый день в 9:05)
CSV экспортируется
    ↓ (автоматически)
Коммитится в Git
    ↓ (автоматически)
Отправляется в GitHub
    ↓
Все агенты видят обновления! ✅
```

---

**Хочешь, чтобы я создал этот скрипт и настроил прямо сейчас?**
