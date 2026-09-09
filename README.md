<div align="center">

# 🚀 коридор роутинг

**Автономный сервис умной маршрутизации и раздельного туннелирования (Split Tunneling) для проекта [«коридор»](https://mvrvntn.github.io/koridor/), [Happ](https://happ.su), [INCY](https://incy.cc), [Remnawave](https://docs.rw), [Sing-box](https://github.com/SagerNet/sing-box) и [Mihomo](https://github.com/MetaCubeX/mihomo).**

[![Build & Update Routing](https://github.com/mvrvntn/routing/actions/workflows/update-configs.yml/badge.svg)](https://github.com/mvrvntn/routing/actions/workflows/update-configs.yml)
[![Release](https://img.shields.io/github/v/release/mvrvntn/routing?color=blue&label=Release)](https://github.com/mvrvntn/routing/releases/latest)
[![jsDelivr CDN](https://img.shields.io/badge/jsDelivr-CDN-orange.svg)](https://www.jsdelivr.com/package/gh/mvrvntn/routing)
[![Tests](https://img.shields.io/badge/Tests-15%20Passed-brightgreen.svg)](tests/test_update_geoblock.py)

**Регион:** 🇷🇺 Россия + 🇧🇾 Беларусь

</div>

---

## ⚡ Как это работает

* 🇷🇺 **Напрямую через локального провайдера (Direct):** Государственные порталы, банки (Сбер, Т-Банк, ВТБ), Налоговая служба, СБП, маркетплейсы (Ozon, WB), сервисы Яндекса, VK, Кинопоиск, сетевые игры (Steam, Epic, Riot) и диагностические чекеры сетевых параметров. Работают с минимальным пингом (RTT) на максимальной скорости домашнего/мобильного провайдера без лишних капч и проверок.
* 🌍 **Через удалённый прокси-узел (Proxy):** Зарубежные медиаплатформы, YouTube, Discord (**включая прямые UDP голосовые серверы**), Telegram, а также исследовательские AI-инструменты (ChatGPT, Claude, Gemini, Perplexity) и внешние сервисы.
* 🍏 **Энергоэффективно (~1.8 МБ RAM):** База сжата алгоритмом агрегации поддоменов (`geosite.dat` ~77 КБ). Снижает нагрузку на CPU смартфона, предотвращает нагрев аккумулятора и системные сбросы сетевого расширения на iOS.
* 🛡 **Аппаратный Safety Gate:** Домены национальных зон `.ru`, `.рф`, `.su` аппаратно изолированы от проксирования.

---

## 📱 Быстрое подключение (Happ & INCY)

### 📊 Профили маршрутизации

| Профиль | Описание | Happ (iOS/Android/ПК) | INCY (iOS/Android/ПК) |
| :--- | :--- | :--- | :--- |
| **коридор роутинг**<br>*(DEFAULT)* | **Рекомендуемый.** Раздельная маршрутизация: локальный трафик напрямую, внешние и AI-сервисы через прокси. | [⚡ В 1 клик](HAPP/DEFAULT.DEEPLINK)<br>[📄 JSON URL](HAPP/DEFAULT.JSON) | [☁️ Autorouting](INCY/DEFAULT.AUTOROUTING)<br>[⚡ В 1 клик](INCY/DEFAULT.DEEPLINK) |
| **коридор роутинг (БС)**<br>*(WHITELIST)* | **Высокая доступность.** Прямой доступ к критической инфраструктуре: банки, Госуслуги, СБП, связь и маркетплейсы. | [⚡ В 1 клик](HAPP/WHITELIST.DEEPLINK)<br>[📄 JSON URL](HAPP/WHITELIST.JSON) | [☁️ Autorouting](INCY/WHITELIST.AUTOROUTING)<br>[⚡ В 1 клик](INCY/WHITELIST.DEEPLINK) |
| **коридор роутинг (JSONSUB)** | Базовый профиль: только DoH DNS и ссылки на базы данных; правила маршрутизации считываются из JSON-конфига. | [⚡ В 1 клик](HAPP/JSONSUB.DEEPLINK)<br>[📄 JSON URL](HAPP/JSONSUB.JSON) | [☁️ Autorouting](INCY/JSONSUB.AUTOROUTING)<br>[⚡ В 1 клик](INCY/JSONSUB.DEEPLINK) |

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

* **Автообновление:** Каждую ночь в 03:00 UTC (06:00 МСК) GitHub Actions синхронизирует сетевые списки и базы провайдеров, валидирует их через Safety Gate, прогоняет тесты и публикует обновленный релиз на CDN.
* **Локальный прогон тестов:**
  ```bash
  python -m unittest discover tests -v
  ```

---

## ❓ FAQ

<details>
<summary><b>1. Почему голосовые каналы Discord работают без задержек («RTC Connecting»)?</b></summary>

Большинство маршрутизаторов перехватывают только веб-домен `discord.com`. Голосовой трафик Discord передаётся по протоколу UDP напрямую на IP-адреса голосовой инфраструктуры i3D.net. В наш `geoip.dat` зашиты диапазоны i3D.net (`geoip:discord`), что обеспечивает стабильное соединение без зависаний.
</details>

<details>
<summary><b>2. Как убедиться, что локальный трафик идёт напрямую?</b></summary>

Откройте [2ip.ru](https://2ip.ru) или банковское приложение (Сбер, Т-Банк) — там отображается ваш реальный домашний IP-адрес интернет-провайдера.
</details>

<details>
<summary><b>3. Не будут ли перегружаться удаленные шлюзы и серверы?</b></summary>

Нет. Через удаленные узлы проходит исключительно внешний трафик (~10–15%). Весь локальный тяжелый контент (видеосервисы, CDN, скачивание игр в Steam, P2P/торренты) направляется напрямую через домашнего провайдера на максимальной скорости тарифа.
</details>

<details>
<summary><b>4. Чем отличаются профили DEFAULT, WHITELIST (БС) и JSONSUB?</b></summary>

* **DEFAULT:** Оптимален для повседневного использования. Локальные сервисы и диагностические чекеры идут напрямую, внешние платформы и AI-инструменты — через прокси-узел.
* **WHITELIST (БС):** Профиль высокой доступности: прямой приоритетный доступ к критической инфраструктуре (банки, Госуслуги, связь, транспорт и социально значимые ресурсы).
* **JSONSUB:** Базовый профиль для интеграции: содержит только DoH DNS и ссылки на скомпилированные базы данных; правила маршрутизации считываются из внешнего JSON-конфига.
</details>

<details>
<summary><b>5. Как устроена корректная работа банковских приложений, мессенджеров и Госуслуг?</b></summary>

Сервисы определения параметров соединения (более 30 чекеров, включая `browserleaks.com`, `whoer.net`, `ipinfo.io`, `ipwho.is`, `2ip.ru`) принудительно направляются в прямое соединение (`direct`). Приложения банков и сервисы аутентификации обращаются напрямую к оператору связи, что обеспечивает мгновенный вход без задержек и капч.
</details>

<details>
<summary><b>6. Как узнать, какие IP и домены изменились после ночной сборки?</b></summary>

Вся дельта между релизами сохраняется в ветке `release`. Список добавленных и скорректированных подсетей можно увидеть командой:
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

## ⚖️ Дисклеймер (Legal Disclaimer)

> [!NOTE]
> Настоящий репозиторий представляет собой независимый исследовательский open-source проект для системного администрирования, анализа сетевых протоколов и оптимизации маршрутизации трафика (Traffic Engineering & Split Tunneling).
>
> 1. Проект **не является средством для обхода блокировок или ограничения доступа к информации**, не содержит встроенных серверов или средств обхода, не предоставляет телематических услуг связи и не популяризирует доступ к запрещенным ресурсам.
> 2. Файлы конфигураций содержат технические списки маршрутизации доменных имен и IP-адресов, предназначенные исключительно для снижения сетевых задержек (RTT), распределения нагрузки на каналы связи и обеспечения стабильного прямого доступа к локальным информационным системам (включая государственные порталы, финансовые сервисы и национальную цифровую инфраструктуру).
> 3. Использование представленных материалов регулируется законодательством страны пользователя. Пользователь самостоятельно несет ответственность за соблюдение применимых законов и правил связи.

---

<div align="center">

**[🌐 Официальный сайт «коридор»](https://mvrvntn.github.io/koridor/)**  
*Надежная оптимизация сетевых маршрутов и раздельного туннелирования*

<br>

[⭐ Поставьте Star](https://github.com/mvrvntn/routing), если проект вам помог!

</div>
