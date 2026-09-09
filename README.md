<div align="center">

# 🚀 коридор роутинг

**Автономный сервис умной маршрутизации и раздельного туннелирования (Split Tunneling) для [коридор VPN](https://mvrvntn.github.io/koridor/), [Happ](https://happ.su), [INCY](https://incy.cc), [Remnawave](https://docs.rw), [Sing-box](https://github.com/SagerNet/sing-box) и [Mihomo](https://github.com/MetaCubeX/mihomo).**

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

## 🔌 Интеграция с серверными панелями

Готовые проверенные решения и шаблоны конфигураций:

### 1. [Remnawave](ADDON_AUTOROUTING/Remnawave/)
* **Автовыдача для INCY:** В **Subscription ➔ Response Rules** (правило `incy`):
  ```http
  autorouting: incy://autorouting/onadd/https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/INCY/DEFAULT.JSON
  ```
* **Автовыдача для Happ:** В **Subscription ➔ Response Rules** (правило `happ`):
  ```http
  routing: happ://routing/onadd/...
  ```
  *(Актуальную строку берите из [`HAPP/DEFAULT.DEEPLINK`](HAPP/DEFAULT.DEEPLINK) либо настройте автообновление через микросервис [`remnawave-routing-update`](ADDON_AUTOROUTING/Remnawave/README.md#2-автороутинг-для-happ))*.
* **Xray Location (ноды):** [`xray_location_template.json`](ADDON_AUTOROUTING/Remnawave/xray_location_template.json) с защитой `routeOnly: true`.
* **Sing-box:** [`singbox_subscription_template.json`](ADDON_AUTOROUTING/Remnawave/singbox_subscription_template.json).
* **Mihomo / Clash:** [`template_remnawave.yaml`](MIHOMO/template_remnawave.yaml).

### 2. [Marzban](ADDON_AUTOROUTING/Marzban/) и [Marzneshin](ADDON_AUTOROUTING/Marzneshin/)
* Единый модуль [`subscription.py`](ADDON_AUTOROUTING/Marzban/subscription.py) для любых типов подписок (JSON и Non-JSON) с переключением профиля через переменную `KORIDOR_ROUTING_SOURCE` (`default`, `whitelist`, `jsonsub`).

### 3. [3x-ui](ADDON_AUTOROUTING/3x-ui/)
* Поддержка кастомных заголовков маршрутизации при отдаче клиентских подписок.

---

## 💻 Ссылки на скомпилированные базы и Rule-Sets

* **Geodata бинарники (V2Ray/Xray/Happ):**
  * `geosite.dat`: `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/geosite.dat`
  * `geoip.dat`: `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/geoip.dat`
* **Sing-box (`.srs`):** `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/sing-box/<category>.srs`
* **Mihomo (`.mrs`):** `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/<category>.mrs`

---

## 📂 Структура репозитория

```text
├── data/                    # Исходные списки доменов для geosite.dat (category-ru, whitelist, discord...)
├── geoip/                   # Исходные списки CIDR IP для geoip.dat (Discord, Telegram, вайтлисты хостинга)
├── HAPP/                    # Готовые JSON-манифесты и .DEEPLINK для клиента Happ
├── INCY/                    # Готовые JSON-манифесты, .DEEPLINK и .AUTOROUTING для клиента INCY
├── MIHOMO/                  # Шаблоны конфигураций для ядра Mihomo / Clash
├── ADDON_AUTOROUTING/       # Модули интеграции для панелей Remnawave, Marzban, Marzneshin, 3x-ui
├── scripts/                 # Скрипты нормализации и санитизации гео-блокировок (update_geoblock.py)
├── tests/                   # Набор регрессионных и юнит-тестов (Safety Gate, схлопывание поддоменов)
└── .github/workflows/       # CI/CD пайплайн компиляции геобаз и публикации релизов
```

---

## 🤖 Автоматизация и тесты

* **Автообновление:** Каждую ночь в 03:00 UTC (06:00 МСК) GitHub Actions выкачивает свежие выгрузки реестров Antifilter и Re-filter, фильтрует их через Safety Gate, прогоняет тесты и выпускает релиз на CDN.
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

<details>
<summary><b>4. Чем отличаются профили DEFAULT, WHITELIST (БС) и JSONSUB?</b></summary>

* **DEFAULT:** Оптимален для 99% задач. РФ сервисы и чекеры напрямую, YouTube/Discord/AI/заблокированные ресурсы — через VPN.
* **WHITELIST (БС):** Спецрежим для периодов ограничений мобильного интернета операторами РФ (белые списки ТСПУ). Напрямую идут только госуслуги, банки, операторы связи и социально значимые ресурсы.
* **JSONSUB:** Базовый профиль для JSON-подписок. Содержит только DoH DNS и ссылки на базы данных, а правила маршрутизации считываются из самого JSON-конфига подписки.
</details>

<details>
<summary><b>5. Как работает защита от детекта VPN в MAX, банках и Госуслугах?</b></summary>

Сервисы определения IP и антифрода (более 30 чекеров, включая `browserleaks.com`, `whoer.net`, `ipinfo.io`, `ipwho.is`, `2ip.ru`) принудительно добавлены в категорию прямого соединения (`direct`). Приложения банков и мессенджер MAX видят реальный домашний IP и оператора абонента, а не сервер датацентра, что исключает блокировку аккаунтов.
</details>

<details>
<summary><b>6. Как узнать, какие IP и домены изменились после ночной сборки?</b></summary>

Вся дельта между релизами сохраняется в ветке `release`. Список добавленных и вырезанных IP-подсетей можно увидеть командой:
```bash
git diff origin/release~1 origin/release -- text/direct.txt
```
</details>

---

## 🙏 Благодарности и поддержка разработчиков оригинала

Проект базируется на наработках сообщества и выражает благодарность авторам оригинальных решений:
* **Разработка:** [ristavor](https://github.com/ristavor)
* **Благодарности:** [hydraponique](https://github.com/hydraponique) & [fatyzzz](https://github.com/fatyzzz)
* **Группа RoscomVPN в Telegram:** [t.me/vpnrouting](https://t.me/vpnrouting)

**Поддержать авторов оригинала (донат):**
* `USDT TRC20`: `TMu3N2ZjK5omJ7n3WAj5MNCSM5querBXsR`

---

<div align="center">

**[🌐 Официальный сайт «коридор VPN»](https://mvrvntn.github.io/koridor/)**  
*Быстрый, приватный и устойчивый к блокировкам VPN*

<br>

[⭐ Поставьте Star](https://github.com/mvrvntn/routing), если проект вам помог!

</div>
