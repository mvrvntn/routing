<div align="center">

# 🚀 коридор роутинг

**Высокопроизводительный автономный репозиторий умной маршрутизации и раздельного туннелирования (Split Tunneling) для [Happ](https://happ.su), [INCY](https://incy.cc), [Remnawave](https://docs.rw), [Sing-box](https://github.com/SagerNet/sing-box) и [Mihomo](https://github.com/MetaCubeX/mihomo).**

> ⚡ **Раздельное туннелирование (Split Tunneling):** Заблокированные ресурсы, YouTube, Discord, голосовые каналы и AI направляются через удаленный узел, а российские сайты, банки, маркетплейсы и игры — напрямую через домашнего провайдера с нулевой задержкой, защитой от капч и минимальным потреблением RAM (**~1.8 МБ**).

[![Build & Update Routing](https://github.com/mvrvntn/routing/actions/workflows/update-configs.yml/badge.svg)](https://github.com/mvrvntn/routing/actions/workflows/update-configs.yml)
[![Release](https://img.shields.io/github/v/release/mvrvntn/routing?color=blue&label=Release)](https://github.com/mvrvntn/routing/releases/latest)
[![jsDelivr CDN](https://img.shields.io/badge/jsDelivr-CDN-orange.svg)](https://www.jsdelivr.com/package/gh/mvrvntn/routing)
[![Tests](https://img.shields.io/badge/Unit%20Tests-15%20Passed-brightgreen.svg)](tests/test_update_geoblock.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Целевой регион:** 🇷🇺 Россия + 🇧🇾 Беларусь

</div>

---

## 📑 Содержание

- [💡 Архитектура и ключевые особенности](#-архитектура-и-ключевые-особенности)
- [📱 Профили и быстрое подключение (Happ & INCY)](#-профили-и-быстрое-подключение-happ--incy)
- [🔌 Интеграция с Remnawave, Marzban и Xray](#-интеграция-с-remnawave-marzban-и-xray)
- [💻 Профили для Sing-box и Mihomo](#-профили-для-sing-box-и-mihomo)
- [📂 Структура репозитория](#-структура-репозитория)
- [🤖 Конвейер автообновления и Safety Gate](#-конвейер-автообновления-и-safety-gate)
- [🧪 Тестирование и контроль качества](#-тестирование-и-контроль-качества)
- [🛠 Локальная сборка и разработка](#-локальная-сборка-и-разработка)
- [❓ Частые вопросы (FAQ)](#-частые-вопросы-faq)

---

## 💡 Архитектура и ключевые особенности

* 🍏 **Ультралегкие базы (< 2 МБ RAM):**
  * `geosite.dat` весит всего **~77 КБ** благодаря Radix-схлопыванию поддоменов.
  * `geoip.dat` весит **~431 КБ**.
  * Потребление оперативной памяти на мобильных устройствах — всего **~1.8 МБ RAM** (гарантирует отсутствие крашей Network Extension на iOS и низкое энергопотребление на Android).
* 🛡 **Строгий аппаратный фильтр Safety Gate:** Ни один российский домен (`.ru`, `.рф`, `.su`, `.xn--p1ai`) или сервис из белых списков физически не может попасть в прокси. Банки, Госуслуги, налоги и СБП работают напрямую без капч и блокировок антифродом.
* 🎙 **Полноценная маршрутизация Discord (L4 + L7):**
  * Доменный уровень: шлюзы `gateway.discord.gg`, медиа и WebSockets.
  * IP-уровень (`geoip:discord`): официальные подсети провайдера i3D.net (`5.200.14.128/25`, `66.22.192.0/18`, `138.128.136.0/21`) и AS62597. **Голосовые каналы подключаются мгновенно (без вечного «RTC Connecting»).**
* ✈️ **Telegram CIDRs (`geoip:telegram`):** Диапазоны дата-центров DC1–DC5 проксируются для быстрой и бесперебойной загрузки тяжелых медиафайлов.
* 🧠 **AI & LLM Services Ready:** Оптимизированы маршруты для **ChatGPT / OpenAI**, **Claude / Anthropic**, **Gemini / Google DeepMind**, **Perplexity**, **Cursor**, **Midjourney**, **xAI (Grok)**.
* 🎮 **Игровой трафик и стриминг:**
  * **YouTube:** Видеопотоки (`googlevideo.com`, `ytimg.com`) идут через VPN.
  * **Twitch:** Прямой эфир напрямую (`geosite:twitch` ➔ direct), а реклама отсекается через прокси (`geosite:twitch-ads`).
  * **Игры и Faceit:** Steam, Epic Games, Riot Games, Faceit (московские серверы) работают напрямую без задержек.
* 🚫 **Анти-реклама и трекеры:** Блокировка рекламы (`category-ads`), телеметрии Windows (`win-spy`) и P2P/торрент-трекеров (`torrent`).

---

## 📱 Профили и быстрое подключение (Happ & INCY)

### 📊 Таблица профилей маршрутизации

| Профиль | Режим работы | RAM | Happ | INCY |
| :--- | :--- | :--- | :--- | :--- |
| **коридор роутинг**<br>*(DEFAULT)* | **Split Tunneling:** RU/банки напрямую, AI/Discord/YouTube через VPN | `~1.8 МБ` | [⚡ Deeplink](HAPP/DEFAULT.DEEPLINK)<br>[📄 JSON](HAPP/DEFAULT.JSON) | [☁️ Autorouting](INCY/DEFAULT.AUTOROUTING)<br>[⚡ Deeplink](INCY/DEFAULT.DEEPLINK)<br>[📄 JSON](INCY/DEFAULT.JSON) |
| **БС**<br>*(WHITELIST)* | **Белый список:** напрямую только реестр ЦБ РФ, Госуслуги, СБП | `~1.5 МБ` | [⚡ Deeplink](HAPP/WHITELIST.DEEPLINK)<br>[📄 JSON](HAPP/WHITELIST.JSON) | [☁️ Autorouting](INCY/WHITELIST.AUTOROUTING)<br>[⚡ Deeplink](INCY/WHITELIST.DEEPLINK)<br>[📄 JSON](INCY/WHITELIST.JSON) |
| **JSONSUB** | **Base DNS:** базовый профиль для ручной кастомизации | `~1.0 МБ` | [⚡ Deeplink](HAPP/JSONSUB.DEEPLINK)<br>[📄 JSON](HAPP/JSONSUB.JSON) | [☁️ Autorouting](INCY/JSONSUB.AUTOROUTING)<br>[⚡ Deeplink](INCY/JSONSUB.DEEPLINK)<br>[📄 JSON](INCY/JSONSUB.JSON) |

---

### 🚀 Быстрый импорт

#### 1. Для приложения Happ (iOS, Android, macOS, Windows)
* **Способ А (Deeplink в один клик):**
  Откройте [`HAPP/DEFAULT.DEEPLINK`](HAPP/DEFAULT.DEEPLINK) (или отправьте ссылку себе в Telegram Избранное) и нажмите на ссылку `happ://routing/onadd/...`. Приложение импортирует правила автоматически.
* **Способ Б (По ссылке на JSON):**
  В приложении Happ: **Настройки** ➔ **Маршрутизация** ➔ **+** ➔ **URL**:
  ```text
  https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/HAPP/DEFAULT.JSON
  ```

#### 2. Для приложения INCY (iOS, Android, Desktop)
* **Autorouting (Рекомендуется — автообновление каждые 24 часа):**
  В приложении INCY: **Маршрутизация** ➔ **+** ➔ **Добавить по ссылке (Autorouting)**:
  ```text
  https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/INCY/DEFAULT.JSON
  ```

---

## 🔌 Интеграция с Remnawave, Marzban и Xray

Готовые шаблоны интеграции находятся в каталоге [`ADDON_AUTOROUTING/Remnawave/`](ADDON_AUTOROUTING/Remnawave/):

### 1. Remnawave (Xray Location Template)
Для нод Xray используйте готовый фрагмент маршрутизации [`ADDON_AUTOROUTING/Remnawave/xray_location_template.json`](ADDON_AUTOROUTING/Remnawave/xray_location_template.json):
* Направляет `geoip:telegram`, `geoip:discord`, `geosite:discord`, `geosite:ai`, `geosite:category-geoblock-ru` во внешний прокси/warp.
* Разрешает `routeOnly: true` для предотвращения двойного проксирования.

### 2. Remnawave (Sing-box Subscription Template)
Для подписчиков Sing-box используйте шаблон [`ADDON_AUTOROUTING/Remnawave/singbox_subscription_template.json`](ADDON_AUTOROUTING/Remnawave/singbox_subscription_template.json), который автоматически подключает бинарные `.srs` правила с CDN.

### 3. Нативная выдача заголовков Autorouting
В настройках подписок Remnawave (**Subscription Settings / Response Rules**):
* Условие: `User-Agent` содержит `incy`
* Заголовок ответа:
  ```http
  autorouting: incy://autorouting/onadd/https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/INCY/DEFAULT.JSON
  ```

---

## 💻 Профили для Sing-box и Mihomo

* **Sing-box Rule-Sets (`.srs`):** `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/sing-box/<category>.srs`
* **Mihomo Rule-Sets (`.mrs`):** `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/<category>.mrs`
* **Архивы всех правил:**
  * [`sing-box.tar.gz`](https://github.com/mvrvntn/routing/releases/latest/download/sing-box.tar.gz)
  * [`mihomo.tar.gz`](https://github.com/mvrvntn/routing/releases/latest/download/mihomo.tar.gz)

---

## 📂 Структура репозитория

```text
mvrvntn/routing/
├── .github/
│   └── workflows/
│       ├── update-configs.yml       # Автономный CI/CD сборщик (cron: 03:00 UTC)
│       └── validate-pr.yml          # Линтер и проверка PR
├── data/                            # Текстовые источники Geosite
│   ├── category-geoblock-ru         # Заблокированные сайты (санитизируются скриптом)
│   ├── category-ru, whitelist       # Российские сервисы, банки, Госуслуги
│   ├── discord, youtube, telegram   # Медиа и стриминговые ресурсы
│   ├── ai, google-deepmind          # ChatGPT, Claude, Gemini, Perplexity
│   └── category-ads, win-spy        # Блокировка рекламы и телеметрии
├── geoip/                           # Конфигурация GeoIP
│   ├── discord.txt                  # Подсети i3D.net (голос Discord)
│   ├── telegram.txt                 # Диапазоны дата-центров Telegram DC1-DC5
│   └── config.json                  # Конфигурация сборщика Loyalsoldier
├── scripts/
│   └── update_geoblock.py           # Конвейер санитизации, Safety Gate и схлопывания
├── tests/
│   └── test_update_geoblock.py      # Набор 15 юнит- и регрессионных тестов
├── HAPP/                            # Профили для Happ (DEFAULT, WHITELIST, JSONSUB)
├── INCY/                            # Профили для INCY (DEFAULT, WHITELIST, JSONSUB)
├── MIHOMO/                          # Шаблоны для Mihomo / Clash Meta
├── ADDON_AUTOROUTING/               # Шаблоны для Remnawave, Marzban, Marzneshin
├── geosite.dat                      # Локальная скомпилированная база Geosite
└── geoip.dat                        # Локальная скомпилированная база GeoIP
```

---

## 🤖 Конвейер автообновления и Safety Gate

В репозиторий встроен автономный конвейер [`scripts/update_geoblock.py`](scripts/update_geoblock.py), выполняемый в GitHub Actions каждую ночь:

```
┌──────────────────────────────────────────────────────────────┐
│       Antifilter Community (domains.lst) + Baseline          │
└──────────────────────────────┬───────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────┐
│       1. Safety Gate: Блокировка попадания .ru / .рф         │
│          и доменов из category-ru / whitelist                │
└──────────────────────────────┬───────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────┐
│       2. Radix Collapsing: схлопывание избыточных            │
│          поддоменов (минус 20-30% веса базы)                 │
└──────────────────────────────┬───────────────────────────────┘
                               ▼
┌──────────────────────────────────────────────────────────────┐
│       3. Атомарная запись (.tmp ➔ replace) с защитой         │
│          от сбоев диска и санитарным порогом размера         │
└──────────────────────────────────────────────────────────────┘
```

---

## 🧪 Тестирование и контроль качества

Все модули покрыты изолированными тестами без внешних сетевых зависимостей ([`tests/test_update_geoblock.py`](tests/test_update_geoblock.py)):
* Очистка схем, портов, путей и комментариев (`clean_domain_string`).
* Валидация по RFC 1035 и отсечение IP-адресов (`is_valid_domain`).
* Проверка Safety Gate на непробиваемость Рунета (`is_protected_domain`).
* Схлопывание иерархии поддоменов (`prune_redundant_subdomains`).
* Асинхронная изоляция сетевого шва с моками (`fetch_single_url`).
* Транзакционный откат временных файлов при ошибке диска (`async_main`).

Запуск тестов локально:
```bash
python -m unittest discover tests -v
```

---

## 🛠 Локальная сборка и разработка

```bash
# 1. Запуск конвейера санитизации блокировок
python scripts/update_geoblock.py

# 2. Запуск набора тестов
python -m unittest discover tests -v

# 3. Пересчет Base64-диплинков при изменении JSON
python -c "
import json, base64
for f in ['HAPP', 'INCY']:
    for n in ['DEFAULT', 'WHITELIST', 'JSONSUB']:
        data = json.load(open(f'{f}/{n}.JSON'))
        b64 = base64.b64encode(json.dumps(data, separators=(',', ':')).encode()).decode()
        open(f'{f}/{n}.DEEPLINK', 'w').write(f'{f.lower()}://routing/onadd/{b64}\n')
"
```

---

## ❓ Частые вопросы (FAQ)

<details>
<summary><b>1. Почему на смартфонах не греется процессор и не садится батарея?</b></summary>

Лимит оперативной памяти iOS для фонового процесса Network Extension составляет 15–30 МБ.
Стандартные раздутые базы весят по 20–35 МБ и вызывают вылет (`Jetsam kill`). Наша база весит всего **~77 КБ**, а потребление оперативной памяти составляет **~1.8 МБ RAM**, обеспечивая максимальную автономность и плавность работы.
</details>

<details>
<summary><b>2. Почему Discord голосовые каналы не висят на «RTC Connecting»?</b></summary>

Большинство роутингов перехватывают только домен `discord.com`. Но голосовой трафик Discord идёт напрямую на IP-адреса хостинга i3D.net по протоколу UDP. Мы добавили официальные подсети в `geoip:discord`, поэтому голосовой трафик гарантированно проксируется.
</details>

<details>
<summary><b>3. Не будут ли перегружаться мои VPN-серверы?</b></summary>

Нет. Через серверы идёт только заблокированный трафик (~10–15% от общего объема). Весь тяжёлый контент (VK Видео, RuTube, Кинопоиск, скачивание игр Steam, торренты) идёт напрямую через провайдера без участия твоих серверов.
</details>

---

<div align="center">

[⭐ Поставьте Star репозиторию](https://github.com/mvrvntn/routing), если проект оказался полезным!

</div>
