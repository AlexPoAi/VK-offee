# VK-offee Telegram Bot

Telegram бот для работы с базой знаний сети кофеен «Вкусный Кофе».

## Возможности

- 🔍 Поиск информации в базе знаний
- 📋 Просмотр меню и рецептов
- 🎯 Навигация по ролям FPF (F1-F9)
- 📊 Доступ к документации
- ✅ Статус системы

## Боевой контур (24/7)

- Основной режим: VPS + `systemd` сервис `vk-telegram-bot`.
- Локальный запуск (`start.sh`) использовать только для отладки.
- Legacy debug-утилиты с хардкод `CHAT_ID` удалены из рабочего репозитория.

## Установка

### 1. Установка зависимостей

```bash
cd ~/VK-offee/telegram-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Настройка

Скопируйте `.env.example` в `.env` и настройте:

```bash
cp .env.example .env
nano .env
```

Укажите ваш Telegram Bot Token (получить у @BotFather).

### 3. Запуск

```bash
./start.sh
```

Или вручную:

```bash
source venv/bin/activate
python3 bot.py
```

## Команды бота

- `/start` - Начать работу
- `/help` - Помощь
- `/search <запрос>` - Поиск в базе знаний
- `/status` - Статус бота
- `/menu` - Показать меню кофейни
- `/roles` - Список ролей (F1-F9)

## Автозапуск (macOS)

Создайте файл `~/Library/LaunchAgents/com.vkoffee.bot.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vkoffee.bot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/alexander/VK-offee/telegram-bot/start.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/alexander/VK-offee/telegram-bot/bot.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/alexander/VK-offee/telegram-bot/bot.error.log</string>
</dict>
</plist>
```

Загрузите службу:

```bash
launchctl load ~/Library/LaunchAgents/com.vkoffee.bot.plist
```

## Развертывание на сервере

### Вариант 1: VPS (DigitalOcean, Hetzner, etc.)

```bash
# На сервере
git clone https://github.com/alexpoaiagent-sudo/VK-offee.git
cd VK-offee/telegram-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настройка .env
nano .env

# Запуск через systemd
sudo nano /etc/systemd/system/vkoffee-bot.service
```

Содержимое `vkoffee-bot.service`:

```ini
[Unit]
Description=VK-offee Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/home/your_user/VK-offee/telegram-bot
ExecStart=/home/your_user/VK-offee/telegram-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Запуск:

```bash
sudo systemctl enable vkoffee-bot
sudo systemctl start vkoffee-bot
sudo systemctl status vkoffee-bot
```

### Вариант 2: Railway.app (бесплатно)

1. Создайте аккаунт на [Railway.app](https://railway.app)
2. Подключите GitHub репозиторий
3. Добавьте переменные окружения из `.env`
4. Railway автоматически развернет бота

### Вариант 3: Heroku

```bash
# Создайте Procfile
echo "worker: python telegram-bot/bot.py" > Procfile

# Деплой
heroku create vkoffee-bot
heroku config:set TELEGRAM_BOT_TOKEN=your_token
git push heroku main
heroku ps:scale worker=1
```

## Логи

Логи сохраняются в `bot.log`:

```bash
tail -f bot.log
```

## Остановка бота

```bash
# Найти процесс
ps aux | grep bot.py

# Остановить
kill <PID>

# Или через launchctl (если настроен автозапуск)
launchctl unload ~/Library/LaunchAgents/com.vkoffee.bot.plist
```

## Обновление

```bash
cd ~/VK-offee
git pull
cd telegram-bot
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

## Troubleshooting

### Бот не отвечает

1. Проверьте, что бот запущен: `ps aux | grep bot.py`
2. Проверьте логи: `tail -f bot.log`
3. Проверьте токен в `.env`

### Ошибка "Token is invalid"

Получите новый токен у @BotFather в Telegram.

### Бот останавливается при закрытии терминала

Используйте `nohup` или настройте автозапуск через launchd/systemd.

---

**Версия:** 2.0
**Дата:** 2026-02-14
**Автор:** Александр + Claude Sonnet 4.5
