# 🔄 Интеграция автороутинга с Remnawave (Remnawave-Routing-update)

Модуль для автоматического обновления диплинка роутинга в панели Remnawave через официальный API.
Используется контейнер [lifeindarkside/Remnawave-Routing-update](https://github.com/lifeindarkside/Remnawave-Routing-update).

## 🚀 Как это работает
1. Контейнер опрашивает актуальный `.DEEPLINK` файл из репозитория `mvrvntn/routing`.
2. При выходе нового релиза или обновлении правил контейнер отправляет `PATCH` запрос в Remnawave API (`/subscription-settings` или `/external-squads/{uuid}`).
3. В заголовки подписки добавляется актуальный заголовок `routing: happ://routing/onadd/...` (или `incy://...`).
4. Клиенты (Happ, INCY) при каждом обновлении подписки автоматически получают свежие правила маршрутизации без каких-либо действий пользователя.

---

## 🛠 Установка на сервере Remnawave

### 1. Добавление в `docker-compose.yml` панели Remnawave:

```yaml
services:
  remnawave-routing-update:
    image: ghcr.io/lifeindarkside/remnawave-routing-update:latest
    container_name: remnawave-routing-update
    restart: unless-stopped
    environment:
      # URL вашей панели Remnawave (локальный внутри docker-сети или внешний через https)
      - REMNA_BASE_URL=https://panel.yourdomain.com/api
      # API токен Remnawave (создается в Panel -> Settings -> API Tokens с правами Subscription Settings / External Squads)
      - REMNA_TOKEN=your_remnawave_api_token_here
      # Ссылка на актуальный диплинк Happ или INCY
      - GITHUB_RAW_URL=https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/HAPP/DEFAULT.DEEPLINK
      # Интервал проверки (в секундах, по умолчанию 300 = 5 минут)
      - CHECK_INTERVAL=300
```

> **Совет для INCY:** Если нужно раздавать роутинг для INCY, укажите:
> `GITHUB_RAW_URL=https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/INCY/DEFAULT.DEEPLINK`

### 2. Запуск:
```bash
docker compose up -d remnawave-routing-update
docker logs -f remnawave-routing-update
```
