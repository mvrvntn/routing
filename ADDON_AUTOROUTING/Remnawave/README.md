# 🔄 Интеграция автороутинга «коридор роутинг» с Remnawave

Полное руководство по интеграции «коридор роутинг» с панелью **Remnawave** для всех типов клиентов (INCY, Happ, Sing-Box, Mihomo / Clash, Xray).

---

## 1. Автороутинг для INCY (Нативный, рекомендуется)

Приложение [INCY](https://incy.cc) поддерживает нативное автообновление профиля:
1. В панели Remnawave перейдите в **Settings** ➔ **Subscription Templates / Response Rules** (Правила ответов).
2. Отредактируйте правило для INCY (`User-Agent` содержит `incy`).
3. Добавьте HTTP-заголовок ответа:
   ```http
   autorouting: incy://autorouting/onadd/https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/INCY/DEFAULT.JSON
   ```
   *(Для профиля Белых Списков: `incy://autorouting/onadd/https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/INCY/WHITELIST.JSON`, для JSONSUB: `incy://autorouting/onadd/https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/INCY/JSONSUB.JSON`)*.

---

## 2. Автороутинг для Happ

Для [Happ](https://happ.su) передайте диплинк в заголовке `routing`:
1. В **Правилах ответов** Remnawave для правила `Happ` (`User-Agent` содержит `happ`) добавьте заголовок (скопируйте готовую актуальную строку из файла [`HAPP/DEFAULT.DEEPLINK`](../../HAPP/DEFAULT.DEEPLINK)):
   ```http
   routing: happ://routing/onadd/...
   ```
2. Либо настройте автоматическое обновление через микросервис [`remnawave-routing-update`](https://github.com/lifeindarkside/Remnawave-Routing-update):
   ```yaml
   services:
     remnawave-routing-update:
       image: ghcr.io/lifeindarkside/remnawave-routing-update:latest
       container_name: remnawave-routing-update
       restart: unless-stopped
       environment:
         - REMNA_BASE_URL=https://panel.yourdomain.com/api
         - REMNA_TOKEN=your_remnawave_api_token_here
         - GITHUB_RAW_URL=https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/HAPP/DEFAULT.DEEPLINK
         - CHECK_INTERVAL=43200
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
Это гарантирует, что российские приложения (Мос.ру, Ozon, WB), проверяющие реальный IP через сервис `ipwho.is`, будут работать без ложных срабатываний и сетевых предупреждений.

---

## 🙏 Благодарности
* Оригинальная разработка: **ristavor**
* Исследования и списки: **hydraponique** & **fatyzzz**
* Группа RoscomVPN в Telegram: [t.me/vpnrouting](https://t.me/vpnrouting)
* Донаты авторам оригинала (`USDT TRC20`): `TMu3N2ZjK5omJ7n3WAj5MNCSM5querBXsR`

Проект «коридор»: [https://mvrvntn.github.io/koridor/](https://mvrvntn.github.io/koridor/)
