#!/bin/bash
# Скрипт автоматической синхронизации Google Drive
# Запускается через cron каждый день в 9:00

cd /Users/alexander/Github/VK-offee/.github/scripts

echo "=========================================="
echo "Google Drive Sync: $(date)"
echo "=========================================="

# Запуск синхронизации
python3 sync_google_drive_v2.py

# Проверка результата
if [ $? -eq 0 ]; then
    echo "✅ Синхронизация завершена успешно"

    # Автоматический коммит изменений
    cd /Users/alexander/Github/VK-offee

    # Проверка наличия изменений
    if [ -n "$(git status --porcelain)" ]; then
        echo "📝 Обнаружены изменения, коммичу..."
        git add knowledge-base/
        git commit -m "Sync: Google Drive $(date +'%Y-%m-%d %H:%M')"
        git push origin main
        echo "✅ Изменения отправлены в GitHub"
    else
        echo "ℹ️  Нет изменений для коммита"
    fi
else
    echo "❌ Ошибка синхронизации"
    exit 1
fi

echo "=========================================="
echo "Завершено: $(date)"
echo "=========================================="
