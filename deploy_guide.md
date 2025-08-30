
---

## ✅ 13. `deploy_guide.md`

### 🔧 Как задеплоить на Render / Fly.io / VPS

#### 1. Подготовка
- Создайте репозиторий на GitHub
- Загрузите туда этот проект
- На хостинге (Render, Fly.io) укажите:
  - **Repository**: ваш
  - **Branch**: main
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `python bot/main.py`

#### 2. Переменные окружения
В настройках хостинга добавьте:

BOT_TOKEN=ваш_токен
ADMIN_ID=ваш_telegram_id


#### 3. Webhook (опционально)
Для production лучше использовать **webhook**.  
Но для старта **polling** — проще и стабильнее.

> ⚠️ Render бесплатно "засыпает" сервисы. Используйте **cron-бота** или **UptimeRobot**, чтобы "будить" каждые 15 минут.

#### 4. Автозапуск (VPS)
Если на VPS — используйте `systemd`:

```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/bot
ExecStart=/path/to/venv/bin/python bot/main.py
Restart=always

[Install]
WantedBy=multi-user.target