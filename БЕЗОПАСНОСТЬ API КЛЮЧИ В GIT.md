# 🔴 КРИТИЧЕСКАЯ ПРОБЛЕМА: API ключи были в GitHub!

**Дата обнаружения:** 2026-02-19, 22:45
**Статус:** 🔴 ТРЕБУЕТСЯ НЕМЕДЛЕННОЕ ДЕЙСТВИЕ

---

## ⚠️ ЧТО ПРОИЗОШЛО

В коммите `87260c30` (6 февраля 2026) файл `.env` был закоммичен с реальными API ключами:

1. **Telegram Bot Token:** `7978142264:AAFr3oSP_ZNz18X_Z9ADCNAs3_lhwIZrfmU`
2. **Anthropic API Key:** `sk-ant-api03-ShVN...` (частично)

**Это значит:** Любой, кто имеет доступ к репозиторию, может увидеть эти ключи в истории Git!

---

## 🚨 НЕМЕДЛЕННЫЕ ДЕЙСТВИЯ

### ✅ Что уже сделано:

1. ✅ `.env` добавлен в `.gitignore`
2. ✅ История Git очищена от `.env` (filter-branch)

### ⚠️ ЧТО НУЖНО СДЕЛАТЬ СРОЧНО:

#### 1. Сменить Telegram Bot Token

**Где:** https://t.me/BotFather

**Как:**
```
1. Открыть @BotFather в Telegram
2. Отправить: /mybots
3. Выбрать бота
4. API Token → Revoke current token
5. Скопировать новый токен
6. Обновить в .env:
   TELEGRAM_BOT_TOKEN=новый_токен
```

#### 2. Сменить Anthropic API Key (если использовался)

**Где:** https://console.anthropic.com/settings/keys

**Как:**
```
1. Открыть Anthropic Console
2. Перейти в Settings → API Keys
3. Удалить старый ключ
4. Создать новый ключ
5. Обновить в .env (если используется):
   ANTHROPIC_API_KEY=новый_ключ
```

#### 3. Force Push очищенной истории

**⚠️ ВНИМАНИЕ:** Это перезапишет историю в GitHub!

```bash
cd /Users/alexander/VK-offee

# Проверить, что .env удалён из истории
git log --all --full-history -- telegram-bot/.env

# Если пусто → хорошо, можно продолжать

# Force push (ОПАСНО!)
git push origin --force --all
git push origin --force --tags
```

#### 4. Проверить другие репозитории

```bash
# creativ-convector
cd /Users/alexander/Documents/creativ-convector.nocloud
git log --all --full-history -- .env
git log --all --full-history -- token.pickle
git log --all --full-history -- credentials.json
```

---

## 🔒 КАК ПРЕДОТВРАТИТЬ В БУДУЩЕМ

### 1. Проверить .gitignore

**Файл:** `/Users/alexander/VK-offee/.gitignore`

**Должно быть:**
```
# Секретные данные
.env
*.env
.env.*
!.env.example

# API ключи и токены
token.pickle
credentials.json
*.key
*.pem
*_key
*_token
*_secret

# Логи с возможными секретами
*.log
```

### 2. Использовать pre-commit hook

**Создать:** `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Проверка на случайный коммит секретов

if git diff --cached --name-only | grep -E "\.env$|token|credentials|\.key$"; then
    echo "🔴 ОШИБКА: Попытка закоммитить секретные файлы!"
    echo "Файлы:"
    git diff --cached --name-only | grep -E "\.env$|token|credentials|\.key$"
    exit 1
fi

# Проверка на API ключи в коде
if git diff --cached | grep -E "sk-[a-zA-Z0-9]{20,}|AKIA[A-Z0-9]{16}"; then
    echo "🔴 ОШИБКА: Обнаружен API ключ в коде!"
    exit 1
fi

exit 0
```

```bash
chmod +x .git/hooks/pre-commit
```

### 3. Использовать git-secrets

```bash
# Установить
brew install git-secrets

# Настроить для репозитория
cd /Users/alexander/VK-offee
git secrets --install
git secrets --register-aws
git secrets --add 'sk-[a-zA-Z0-9]{20,}'
git secrets --add '[0-9]{10}:[A-Za-z0-9_-]{35}'
```

---

## 📋 ЧЕКЛИСТ БЕЗОПАСНОСТИ

### Немедленно:
- [ ] Сменить Telegram Bot Token
- [ ] Сменить Anthropic API Key (если был)
- [ ] Force push очищенной истории
- [ ] Проверить другие репозитории

### В течение дня:
- [ ] Установить pre-commit hook
- [ ] Установить git-secrets
- [ ] Проверить все .env файлы
- [ ] Обновить .gitignore во всех репозиториях

### Постоянно:
- [ ] Никогда не коммитить .env
- [ ] Использовать .env.example для примеров
- [ ] Проверять `git status` перед commit
- [ ] Использовать переменные окружения в продакшене

---

## 🔍 КАК ПРОВЕРИТЬ, ЧТО КЛЮЧИ УДАЛЕНЫ

### Проверка 1: Локальная история

```bash
cd /Users/alexander/VK-offee
git log --all --full-history --source -- telegram-bot/.env
# Должно быть пусто
```

### Проверка 2: GitHub

```bash
# После force push
# Открыть: https://github.com/alexpoaiagent-sudo/VK-offee/commits/main
# Найти коммит 87260c30
# Проверить, что .env не показывается
```

### Проверка 3: Поиск в коде

```bash
cd /Users/alexander/VK-offee
git grep "7978142264" $(git rev-list --all)
# Должно быть пусто после force push
```

---

## 💡 ЛУЧШИЕ ПРАКТИКИ

### 1. Использовать переменные окружения

**Вместо .env в Git:**
```bash
# В ~/.zshrc или ~/.bashrc
export TELEGRAM_BOT_TOKEN="..."
export OPENAI_API_KEY="..."
```

### 2. Использовать секретные менеджеры

**Для продакшена:**
- Railway: Variables
- Heroku: Config Vars
- AWS: Secrets Manager
- 1Password: Developer Secrets

### 3. Разделять окружения

```
.env.local       # Локальная разработка (не в Git)
.env.development # Разработка (не в Git)
.env.production  # Продакшен (не в Git)
.env.example     # Пример (в Git) ✅
```

---

## 📞 ЕСЛИ КЛЮЧИ УЖЕ ИСПОЛЬЗОВАЛИСЬ ЗЛОУМЫШЛЕННИКАМИ

### Признаки:

1. Неожиданные расходы на OpenAI/Anthropic
2. Странные сообщения от бота
3. Необычная активность в логах

### Действия:

1. **Немедленно** отозвать все ключи
2. Проверить billing на всех сервисах
3. Изменить пароли
4. Включить 2FA везде
5. Связаться с поддержкой сервисов

---

## ✅ ПОСЛЕ ИСПРАВЛЕНИЯ

**Проверить:**
- [ ] Новые токены работают
- [ ] Старые токены не работают
- [ ] История Git чиста
- [ ] .gitignore настроен
- [ ] Pre-commit hook установлен
- [ ] Нет неожиданных расходов

---

**ВАЖНО:** Это серьёзная проблема безопасности. Действуй быстро!

**Дата создания:** 2026-02-19, 22:45
**Статус:** 🔴 ТРЕБУЕТСЯ ДЕЙСТВИЕ
