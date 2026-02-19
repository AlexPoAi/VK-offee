#!/bin/bash
# Автоматическая синхронизация Google Sheets → CSV → GitHub

echo "=========================================="
echo "Google Sheets Sync: $(date)"
echo "=========================================="

# Массив таблиц: "SHEET_ID:GID:НАЗВАНИЕ:ПАПКА"
# GID=0 для первого листа (по умолчанию)
SHEETS=(
    # КУХНЯ
    "1Ai4qUIXpkc1fJ_Cd5Vh-wgPV9a-blOhtQWV_tyqhFTU:372408211:Калькуляции СЕБЕСТОИМОСТЬ КУХНЯ:КУХНЯ"
    "1iHcpofQz8WjyPnYlAZOl6RKrh4MQze1T20d3npXMdJg:0:Калькулятор подсчета приготовленных продуктов:КУХНЯ"
    "1JLmJ7KuSdj2reJlasvtFQekKrPb8-7yKZkPUEOMWFvE:0:Список продуктов учет:КУХНЯ"

    # БАР
    "1xcbVugDZoUMrrDHQb_Dycbiq6mMBFvOiFPQV-uZo1Og:0:Калькуляции напитки:БАР"
    "1J5BXZjLnAF3amAw02xH4MTYN5bPg9IwqOwnxqWBDJR4:0:Составы продукции:БАР"
    "1s3PgusaFjJftN8oKpxiDUQewqcV-NzwiRzboFyK-0GA:0:Срок продукции:БАР"
    "11BLOsP9Se5i-gNw5nrTkDPiikcRlGu3DYvsx6aqLzgo:0:Расчет смузи:БАР"

    # Чек-листы
    "1WzFPsrsXIa3BewZOo2rC3vcCsjOSfzvaV099yBahM8c:0:чек-лист Тургенева:БАР"
    "1w0xAzC20YSUPAmxYTezAIG0764uXMXOfMH1yqUPT1BA:0:чек-лист Самокиша:БАР"
    "187eTXnt3i17vnnMeSX9KQHi5_qPuL7lQqGUehyfupds:0:чек-лист Луговая:БАР"
    "1b_T5uST433dJGXnIlS4WNbIU0IDj1RymECZ8uMvITNk:0:Чек-лист Раннера Тургенева:БАР"
    "1_0EDx54ziO4mW6jSKtyspux92t7OG5v6tc1kykc98bE:0:Чек-лист Раннера Самокиша:БАР"
    "1J3kZ33YrBxXKW6WI2r6kl8kw51UHGTL3eKwJf3_Ri8s:0:Чек-лист Раннера Луговая:БАР"

    # Персонал
    "1vA2XkU229QoRQhWAbqjGTeB1Ba_fFSp0Dq_CEhKZC7Y:0:Таблица по ЗП сотрудников:Персонал"
    "1w4K9mrGmrSIua6oUI4kuMziI88YjLetJkcdjdzLADOE:0:Размер одежды сотрудников:Персонал"
    "1KiXAyzk88L0fyOWp0C9IbEcI0QGAhQL7jmPJgE__aVU:0:ДР сотрудников и рабочая почта:Персонал"
    "1pRFiKE3Ll6jTogDU-dgLgv2yKpNnMjxbJlwloBI4P-g:0:Список чатов кофейни:Персонал"
    "1edkjH38zRhWnkovDImu__v5kJy-Fnrp6CVQhjxVc5wQ:0:Обратная связь по кофейне от сотрудников:Персонал"
    "1ebAx2jvt0B7KHJhJBEJ_NUcXjgWxt3muChV7xitxhmk:0:Ответы Тестирование ДИ Официанта:Персонал"

    # ДЛЯ ШЕФА
    "1kr6Z0HyYcAZWTTp7Jp_nopsGRVuK45smtcayBaTRPMM:0:Закуп сравнение цен:ДЛЯ ШЕФА"
    "1h22FSh3F7dUGAIUDJXGbyOWQJokZ7jKVSh_aYt9pceI:0:Контакты печати строительных сеток:ДЛЯ ШЕФА"
    "1fge42tcKdx33MNxH9jrQxxdmzAaoIeS8eCTbuFF4AMM:0:Компании по дезинсекции:ДЛЯ ШЕФА"
    "1asLM0UlGNOOhQfMkoc5zDj2MKgtc4tWnwPSn5A3E9js:0:Расчет Диана МЕЛТ:ДЛЯ ШЕФА"
    "1QrL48GAzpVABqwwSO5z80PNZNk2cVKXLwDYwEGXz5sM:0:График оплаты поставщиков:ДЛЯ ШЕФА"

    # Инвентаризация
    "1-MMMX8UrxvrRhwDwkN5K94bdf95YG1bAEtGQ9kwvV6I:0:Список посуды:Инвентаризация "
    "1OhCnZGMgDEx-ghU-F-0VCP3xloGQO37mrzlJ1SnsbIU:0:Отчет по инвентаризации:Инвентаризация "
    "1sqrYyqSENH83Q-O9BWtUUAYpAWa63JHyvpp2NZuGUIg:0:Список зерна по кофейням:Инвентаризация "
)

BASE_PATH="/Users/alexander/VK-offee/knowledge-base"
CHANGED=0
SUCCESS=0
FAILED=0

for sheet in "${SHEETS[@]}"; do
    IFS=':' read -r sheet_id gid name folder <<< "$sheet"

    echo "📥 Синхронизация: $name"

    # Создать папку если не существует
    mkdir -p "$BASE_PATH/$folder"

    # Путь к файлу
    file_path="$BASE_PATH/$folder/$name.csv"

    # Скачать таблицу
    curl -s -L "https://docs.google.com/spreadsheets/d/${sheet_id}/export?format=csv&gid=${gid}" \
         -o "$file_path.tmp"

    # Проверить успешность скачивания
    if [ $? -ne 0 ] || [ ! -s "$file_path.tmp" ]; then
        echo "  ❌ Ошибка скачивания"
        rm -f "$file_path.tmp"
        FAILED=$((FAILED + 1))
        continue
    fi

    # Проверить, изменился ли файл
    if [ -f "$file_path" ]; then
        if ! cmp -s "$file_path" "$file_path.tmp"; then
            mv "$file_path.tmp" "$file_path"
            echo "  ✅ Обновлён"
            CHANGED=1
            SUCCESS=$((SUCCESS + 1))
        else
            rm "$file_path.tmp"
            echo "  ⏭️  Без изменений"
            SUCCESS=$((SUCCESS + 1))
        fi
    else
        mv "$file_path.tmp" "$file_path"
        echo "  ✅ Создан"
        CHANGED=1
        SUCCESS=$((SUCCESS + 1))
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
echo "📊 Успешно: $SUCCESS | Ошибок: $FAILED"
echo "=========================================="
