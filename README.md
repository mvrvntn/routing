<div align="center">

# 🚀 коридор роутинг

**Автономный сервис умной маршрутизации и раздельного туннелирования (Split Tunneling) для [Happ](https://happ.su), [INCY](https://incy.cc), [Remnawave](https://docs.rw), [Sing-box](https://github.com/SagerNet/sing-box) и [Mihomo](https://github.com/MetaCubeX/mihomo).**

[![Build & Update Routing](https://github.com/mvrvntn/routing/actions/workflows/update-configs.yml/badge.svg)](https://github.com/mvrvntn/routing/actions/workflows/update-configs.yml)
[![Release](https://img.shields.io/github/v/release/mvrvntn/routing?color=blue&label=Release)](https://github.com/mvrvntn/routing/releases/latest)
[![jsDelivr CDN](https://img.shields.io/badge/jsDelivr-CDN-orange.svg)](https://www.jsdelivr.com/package/gh/mvrvntn/routing)
[![Tests](https://img.shields.io/badge/Tests-15%20Passed-brightgreen.svg)](tests/test_update_geoblock.py)

**Регион:** 🇷🇺 Россия + 🇧🇾 Беларусь

</div>

---

## ⚡ Как это работает

* 🇷🇺 **Напрямую через провайдера (Direct):** Банки (Сбер, Т-Банк, ВТБ), Госуслуги, Налоговая, СБП, маркетплейсы (Ozon, WB), сервисы Яндекса, VK, Кинопоиск, игры (Steam, Epic, Riot), а также IP-чекеры для защиты от детекта VPN (MAX, антифрод). Работают на полной скорости вашего интернета без капч и блокировок.
* 🌍 **Через VPN (Proxy):** YouTube, Discord (**включая голосовые каналы**), Telegram (медиа дата-центров), Instagram, заблокированные сайты реестра, а также AI-сервисы (ChatGPT, Claude, Gemini, Perplexity).
* 🍏 **Энергоэффективно (~1.8 МБ RAM):** База сжата алгоритмом схлопывания поддоменов (`geosite.dat` ~77 КБ). Смартфон не греется, батарея не садится, исключены вылеты VPN на iOS.
* 🛡 **Аппаратный Safety Gate:** Домены зон `.ru`, `.рф`, `.su` физически не могут попасть в прокси-список.

---

## 📱 Быстрое подключение (Happ & INCY)

### 📊 Профили маршрутизации

| Профиль | Описание | Happ (iOS/Android/ПК) | INCY (iOS/Android/ПК) |
| :--- | :--- | :--- | :--- |
| **коридор роутинг**<br>*(DEFAULT)* | **Рекомендуемый.** Раздельный туннель: РФ напрямую, блок/AI/Discord/YouTube через VPN. | [⚡ В 1 клик](HAPP/DEFAULT.DEEPLINK)<br>[📄 JSON URL](HAPP/DEFAULT.JSON) | [☁️ Autorouting](INCY/DEFAULT.AUTOROUTING)<br>[⚡ В 1 клик](INCY/DEFAULT.DEEPLINK) |
| **коридор роутинг (БС)**<br>*(WHITELIST)* | **Белый список.** Спецрежим для шатдаунов мобильного интернета в РФ: напрямую только реестр ЦБ РФ, банки, Госуслуги, СБП и маркетплейсы. | [⚡ В 1 клик](HAPP/WHITELIST.DEEPLINK)<br>[📄 JSON URL](HAPP/WHITELIST.JSON) | [☁️ Autorouting](INCY/WHITELIST.AUTOROUTING)<br>[⚡ В 1 клик](INCY/WHITELIST.DEEPLINK) |
| **коридор роутинг (JSONSUB)** | Для JSON-подписок: только DoH DNS и кастомные базы, правила задаются в JSON-конфиге. | [⚡ В 1 клик](HAPP/JSONSUB.DEEPLINK)<br>[📄 JSON URL](HAPP/JSONSUB.JSON) | [☁️ Autorouting](INCY/JSONSUB.AUTOROUTING)<br>[⚡ В 1 клик](INCY/JSONSUB.DEEPLINK) |

### 🚀 Как импортировать

* **Happ:** Скопируйте строку из файла `.DEEPLINK` (начинается на `happ://...`) и откройте её на смартфоне или вставьте в Happ: **Настройки** ➔ **Маршрутизация** ➔ **+** ➔ **Импортировать из буфера**.  
  *Либо укажите прямой URL на JSON:* `https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/HAPP/DEFAULT.JSON`
* **INCY (Рекомендуется):** В приложении INCY выберите **Маршрутизация** ➔ **+** ➔ **Добавить по ссылке (Autorouting)** и вставьте URL:
  ```text
  https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/INCY/DEFAULT.JSON
  ```
  *(Профиль будет обновляться автоматически раз в сутки)*.

---

## 🔌 Для владельцев серверов (Remnawave, Sing-box, Xray)

Готовые проверенные шаблоны конфигураций находятся в каталоге [`ADDON_AUTOROUTING/Remnawave/`](ADDON_AUTOROUTING/Remnawave/):

1. **Xray Location (для узлов):** [`xray_location_template.json`](ADDON_AUTOROUTING/Remnawave/xray_location_template.json)  
   Направляет `geoip:telegram`, `geoip:discord`, `geosite:discord`, `geosite:ai` и `category-geoblock-ru` в выходной прокси/warp с защитой `routeOnly: true`.
2. **Sing-box Subscriptions:** [`singbox_subscription_template.json`](ADDON_AUTOROUTING/Remnawave/singbox_subscription_template.json)  
   Готовая структура правил с CDN-источниками бинарных `.srs` правил.
3. **Выдача Autorouting в Remnawave:**  
   В **Settings** ➔ **Subscription Settings / Response Rules** добавьте заголовок для клиентов с `User-Agent: incy`:
   ```http
   autorouting: incy://autorouting/onadd/https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/INCY/DEFAULT.JSON
   ```

---

## 💻 Ссылки на скомпилированные базы и Rule-Sets

* **Geodata бинарники (V2Ray/Xray/Happ):**
  * `geosite.dat`: `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/geosite.dat`
  * `geoip.dat`: `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/geoip.dat`
* **Sing-box (`.srs`):** `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/sing-box/<category>.srs`
* **Mihomo (`.mrs`):** `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/<category>.mrs`

---

## 🤖 Автоматизация и тесты

* **Автообновление:** Каждую ночь в 06:00 МСК GitHub Actions забирает свежие блокировки из реестра Antifilter, фильтрует их через Safety Gate, прогоняет тесты и выпускает новый релиз на CDN.
* **Локальный прогон тестов:**
  ```bash
  python -m unittest discover tests -v
  ```

---

## ❓ FAQ

<details>
<summary><b>1. Почему голосовые каналы Discord работают без «RTC Connecting»?</b></summary>

Большинство маршрутизаторов перехватывают только домен `discord.com`. Голосовой трафик Discord идёт по UDP напрямую на IP-адреса хостинга i3D.net. В наш `geoip.dat` зашиты официальные голосовые диапазоны i3D.net (`geoip:discord`), поэтому голос подключается мгновенно.
</details>

<details>
<summary><b>2. Как убедиться, что российский трафик идёт напрямую?</b></summary>

Откройте [2ip.ru](https://2ip.ru) или банковское приложение (Сбер, Т-Банк) — там отображается ваш реальный домашний IP-адрес провайдера.
</details>

<details>
<summary><b>3. Не будут ли перегружаться мои VPN-серверы?</b></summary>

Нет. Через ваши серверы проходит только заблокированный трафик (~10–15%). Весь тяжёлый контент (видео VK, RuTube, Кинопоиск, скачивание игр в Steam, торренты) идёт напрямую через провайдера пользователя.
</details>

---

<div align="center">

[⭐ Поставьте Star](https://github.com/mvrvntn/routing), если проект вам помог!

</div>
