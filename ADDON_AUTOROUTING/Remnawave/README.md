# 🔄 Интеграция автороутинга «коридор роутинг» с Remnawave

Полное руководство по интеграции «коридор роутинг» с панелью **Remnawave** для всех типов клиентов (INCY, Happ, Sing-Box, Mihomo / Clash, Xray).

---

## 1. Автороутинг для INCY (Нативный, рекомендуется)

Приложение [INCY](https://incy.cc) поддерживает нативное автообновление профиля:
1. В панели Remnawave перейдите в **Settings** ➔ **Subscription Templates / Response Rules** (Правила ответов).
2. Отредактируйте правило для INCY (`User-Agent` содержит `incy`).
3. Добавьте HTTP-заголовок ответа:
   ```http
   autorouting: https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/INCY/DEFAULT.JSON
   ```
   *(Для профиля Белых Списков используйте: `https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/INCY/WHITELIST.JSON`)*.

---

## 2. Автороутинг для Happ

Для [Happ](https://happ.su) передайте диплинк в заголовке `routing`:
1. В **Правилах ответов** Remnawave для правила `Happ` (`User-Agent` содержит `happ`) добавьте заголовок:
   ```http
   routing: happ://routing/onadd/eyJOYW1lIjoi0LrQvtGA0LjQtNC+0YAg0YDQvtGD0YLQuNC90LMiLCJHbG9iYWxQcm94eSI6InRydWUiLCJVc2VDaHVua0ZpbGVzIjoidHJ1ZSIsIlJlbW90ZURucyI6IjguOC44LjgiLCJEb21lc3RpY0RucyI6Ijc3Ljg4LjguOCIsIlJlbW90ZUROU1R5cGUiOiJEb0giLCJSZW1vdGVETlNEb21haW4iOiJodHRwczovLzguOC44LjgvZG5zLXF1ZXJ5IiwiUmVtb3RlRE5TSVAiOiI4LjguOC44IiwiRG9tZXN0aWNETlNUeXBlIjoiRG9IIiwiRG9tZXN0aWNETlNEb21haW4iOiJodHRwczovLzc3Ljg4LjguOC9kbnMtcXVlcnkiLCJEb21lc3RpY0ROU0lQIjoiNzcuODguOC44IiwiR2VvaXB1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvbXZydm50bi9yb3V0aW5nQHJlbGVhc2UvZ2VvaXAuZGF0IiwiR2Vvc2l0ZXVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9tdnJ2bnRuL3JvdXRpbmdAcmVsZWFzZS9nZW9zaXRlLmRhdCIsIkxhc3RVcGRhdGVkIjoiMTc4ODU5MzY0MCIsIkRuc0hvc3RzIjp7ImxrZmwyLm5hbG9nLnJ1IjoiMjEzLjI0LjY0LjE3NSIsImxrbnBkLm5hbG9nLnJ1IjoiMjEzLjI0LjY0LjE4MSIsImRucy5nb29nbGUiOiI4LjguOC44IiwiY2xvdWRmbGFyZS1kbnMuY29tIjoiMS4xLjEuMSJ9LCJSb3V0ZU9yZGVyIjoiYmxvY2stcHJveHktZGlyZWN0IiwiRGlyZWN0U2l0ZXMiOlsiZ2Vvc2l0ZTpwcml2YXRlIiwiZ2Vvc2l0ZTpjYXRlZ29yeS1ydSIsImdlb3NpdGU6d2hpdGVsaXN0IiwiZ2Vvc2l0ZTptaWNyb3NvZnQiLCJnZW9zaXRlOmFwcGxlIiwiZ2Vvc2l0ZTplcGljZ2FtZXMiLCJnZW9zaXRlOnJpb3QiLCJnZW9zaXRlOmVzY2FwZWZyb210YXJrb3YiLCJnZW9zaXRlOnN0ZWFtIiwiZ2Vvc2l0ZTpvcmlnaW4iLCJnZW9zaXRlOnR3aXRjaCIsImdlb3NpdGU6cGludGVyZXN0IiwiZ2Vvc2l0ZTpmYWNlaXQiXSwiRGlyZWN0SXAiOlsiZ2VvaXA6cHJpdmF0ZSIsImdlb2lwOmRpcmVjdCJdLCJQcm94eVNpdGVzIjpbImdlb3NpdGU6Z29vZ2xlLXBsYXkiLCJnZW9zaXRlOmdvb2dsZS1kZWVwbWluZCIsImdlb3NpdGU6Z2l0aHViIiwiZ2Vvc2l0ZTp0d2l0Y2gtYWRzIiwiZ2Vvc2l0ZTp5b3V0dWJlIiwiZ2Vvc2l0ZTp0ZWxlZ3JhbSIsImdlb3NpdGU6ZGlzY29yZCIsImdlb3NpdGU6YWkiLCJnZW9zaXRlOmNhdGVnb3J5LWdlb2Jsb2NrLXJ1Il0sIlByb3h5SXAiOlsiZ2VvaXA6dGVsZWdyYW0iLCJnZW9pcDpkaXNjb3JkIl0sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp0b3JyZW50IiwiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIn0=
   ```
2. Либо используйте микросервис `remnawave-routing-update`:
   ```yaml
   services:
     remnawave-routing-update:
       image: ghcr.io/lifeindarkside/remnawave-routing-update:latest
       container_name: remnawave-routing-update
       restart: unless-stopped
       environment:
         - REMNA_BASE_URL=https://panel.yourdomain.com/api
         - REMNA_TOKEN=your_remnawave_api_token_here
         - GITHUB_RAW_URL=https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/HAPP/DEFAULT.DEEPLINK
         - CHECK_INTERVAL=300
   ```

---

## 3. Шаблон подписки Sing-Box
В панели Remnawave ➔ **Settings** ➔ **Subscription Templates** ➔ **Sing-Box**:
* Рекомендуется использовать скомпилированные бинарные `.srs` правила нашего репозитория через jsDelivr CDN (`discord-ip`, `telegram-ip`, `category-ru`, `whitelist`, `direct-ip`, `category-ads`, `win-spy`).

---

## 4. Шаблон подписки Mihomo / Clash
В панели Remnawave ➔ **Settings** ➔ **Subscription Templates** ➔ **Clash / Mihomo**:
* Скопируйте содержимое файла [MIHOMO/template_remnawave.yaml](../../MIHOMO/template_remnawave.yaml).
* Шаблон полностью совместим с синтаксисом Remnawave (`# LEAVE THIS LINE!`, `remnawave: include-proxies: false`).

---

## 5. Основной шаблон XRAY для каждой локации
В Remnawave при настройке шаблона Xray для входящих локаций рекомендуется включить:
* Маршрутизацию доменов `geosite:discord`, `geosite:ai`, `geosite:category-geoblock-ru` через тег прокси.
* Прямое проксирование IP-подсетей `geoip:telegram` и `geoip:discord`.
* Опцию `"routeOnly": true` в секции `sniffing` для предотвращения утечек на iOS.

---

## 6. Рекомендация для профиля ноды Remnawave
В конфигурации ноды (`Профиль remnawave ноды.txt`) в секцию чекеров `warp-out` рекомендуется добавить:
```json
"ipwho.is"
```
Это гарантирует, что российские приложения (Мос.ру, Ozon, WB), снайпящие реальный IP через сервис `ipwho.is`, будут работать без ложных срабатываний и плашек «Отключите VPN».
