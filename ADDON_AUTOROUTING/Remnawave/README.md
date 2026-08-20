# 🔄 Интеграция автороутинга с Remnawave

В панели Remnawave поддерживаются два способа доставки правил маршрутизации клиентам **Happ** и **INCY**:

---

## Вариант 1. Нативный Autorouting для INCY (Рекомендуемый)

Приложение [INCY](https://incy.cc) поддерживает встроенный механизм **Autorouting** — профиль привязывается к удаленному JSON-файлу репозитория, получает иконку облака ☁️ в приложении и самостоятельно обновляется каждые 24 часа.

### Настройка в панели Remnawave:
1. Перейдите в **Settings** ➔ **Subscription Templates / Response Rules** (Правила ответов).
2. Создайте или отредактируйте правило для INCY (условие: заголовок `User-Agent` содержит `incy`).
3. Добавьте HTTP-заголовок ответа:
   ```http
   autorouting: https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/INCY/DEFAULT.JSON
   ```
4. Сохраните правило.

> 🚀 **Результат:** Клиенты INCY при первой загрузке подписки автоматически подключат автообновляемый профиль `koridor` и будут обновлять его в фоновом режиме.

---

## Вариант 2. Автообновление через сервис `Remnawave-Routing-update` (для Happ и INCY)

Для клиентов [Happ](https://happ.su) и статических диплинков используется официальный микросервис [lifeindarkside/Remnawave-Routing-update](https://github.com/lifeindarkside/Remnawave-Routing-update).

### Как это работает:
1. Сервис опрашивает файл `.DEEPLINK` из репозитория `mvrvntn/routing`.
2. При выходе нового релиза отправляет `PATCH` в Remnawave API (`/subscription-settings`).
3. Панель начинает отдавать клиентам заголовок `routing: happ://routing/onadd/<base64>`.

### Установка на сервере:

Добавьте в `docker-compose.yml` панели Remnawave:

```yaml
services:
  remnawave-routing-update:
    image: ghcr.io/lifeindarkside/remnawave-routing-update:latest
    container_name: remnawave-routing-update
    restart: unless-stopped
    environment:
      # URL вашей панели Remnawave
      - REMNA_BASE_URL=https://panel.yourdomain.com/api
      # API токен (Panel -> Settings -> API Tokens с правами Subscription Settings / External Squads)
      - REMNA_TOKEN=your_remnawave_api_token_here
      # Ссылка на актуальный диплинк koridor
      - GITHUB_RAW_URL=https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/HAPP/DEFAULT.DEEPLINK
      # Интервал проверки (в секундах)
      - CHECK_INTERVAL=300
```

> **Совет:** Для INCY укажите:
> `GITHUB_RAW_URL=https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/INCY/DEFAULT.DEEPLINK`

Запуск:
```bash
docker compose up -d remnawave-routing-update
docker logs -f remnawave-routing-update
```
