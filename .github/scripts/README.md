# Автоматизация VK-offee

Скрипты для автоматизации работы с базой знаний VK-offee.

## Синхронизация с Google Drive

### Настройка

1. **Создайте проект в Google Cloud Console:**
   - Перейдите на https://console.cloud.google.com/
   - Создайте новый проект "VK-offee Sync"
   - Включите Google Drive API

2. **Создайте OAuth 2.0 Client ID:**
   - Перейдите в "APIs & Services" → "Credentials"
   - Нажмите "Create Credentials" → "OAuth client ID"
   - Выберите "Desktop app"
   - Скачайте JSON файл и сохраните как `credentials.json` в эту папку

3. **Установите зависимости:**
   ```bash
   cd ~/VK-offee/.github/scripts
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Первый запуск:**
   ```bash
   python3 sync_google_drive.py
   ```

   При первом запуске откроется браузер для авторизации. Разрешите доступ к Google Drive.

### Автоматическая синхронизация

#### macOS (через launchd)

Создайте файл `~/Library/LaunchAgents/com.vkoffee.sync.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vkoffee.sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/alexander/VK-offee/.github/scripts/venv/bin/python3</string>
        <string>/Users/alexander/VK-offee/.github/scripts/sync_google_drive.py</string>
    </array>
    <key>StartInterval</key>
    <integer>3600</integer>
    <key>StandardOutPath</key>
    <string>/Users/alexander/VK-offee/.github/scripts/sync.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/alexander/VK-offee/.github/scripts/sync.error.log</string>
</dict>
</plist>
```

Загрузите службу:

```bash
launchctl load ~/Library/LaunchAgents/com.vkoffee.sync.plist
```

Синхронизация будет запускаться каждый час (3600 секунд).

#### Linux (через cron)

```bash
crontab -e
```

Добавьте строку:

```
0 * * * * cd /home/user/VK-offee/.github/scripts && ./venv/bin/python3 sync_google_drive.py
```

### Ручной запуск

```bash
cd ~/VK-offee/.github/scripts
source venv/bin/activate
python3 sync_google_drive.py
```

### Отчеты

Отчеты о синхронизации сохраняются в `knowledge-base/Отчет синхронизации [дата].md`.

## Структура

```
.github/scripts/
├── sync_google_drive.py    # Скрипт синхронизации
├── requirements.txt         # Зависимости Python
├── credentials.json         # OAuth credentials (не коммитить!)
├── token.pickle            # Токен доступа (не коммитить!)
├── venv/                   # Виртуальное окружение
└── README.md              # Эта инструкция
```

## Troubleshooting

### Ошибка "credentials.json not found"

Скачайте credentials.json из Google Cloud Console (см. инструкцию выше).

### Ошибка "Access denied: DriveApp"

Проверьте, что:
1. Google Drive API включен в проекте
2. OAuth consent screen настроен
3. Вы авторизовались с правильным аккаунтом

### Файлы не скачиваются

Проверьте ID папки в `.env`:
```
GOOGLE_DRIVE_FOLDER_ID=120x7kqYeV0Vb4TLbdCC0esv0WkF5JROC
```

---

**Версия:** 1.0
**Дата:** 2026-02-14
