<div align="center">

# 🚀 koridor Routing

**Высокопроизводительный репозиторий умной маршрутизации и раздельного туннелирования (Split Tunneling) для [Happ](https://happ.su), [INCY](https://incy.cc), [Mihomo](https://github.com/MetaCubeX/mihomo), [Sing-box](https://github.com/SagerNet/sing-box) и [Remnawave](https://docs.rw).**

> ⚡ **Раздельное туннелирование (Split Tunneling):** Зарубежные сервисы, YouTube, Discord и AI направляются через удаленный узел, а российские сайты, банки и игры — напрямую через домашнего провайдера с нулевой задержкой, защитой от капч и минимальным потреблением RAM (**3–5 МБ**).

[![Build & Update Routing](https://github.com/mvrvntn/routing/actions/workflows/update-configs.yml/badge.svg)](https://github.com/mvrvntn/routing/actions/workflows/update-configs.yml)
[![Validate Configs](https://github.com/mvrvntn/routing/actions/workflows/validate-pr.yml/badge.svg)](https://github.com/mvrvntn/routing/actions/workflows/validate-pr.yml)
[![Release](https://img.shields.io/github/v/release/mvrvntn/routing?color=blue&label=Release)](https://github.com/mvrvntn/routing/releases/latest)
[![jsDelivr CDN](https://img.shields.io/badge/jsDelivr-CDN-orange.svg)](https://www.jsdelivr.com/package/gh/mvrvntn/routing)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Целевой регион:** 🇷🇺 Россия + 🇧🇾 Беларусь

</div>

---

## 📑 Содержание

- [💡 Возможности и оптимизации](#-возможности-и-оптимизации)
- [📱 Профили и быстрое подключение (Happ & INCY)](#-профили-и-быстрое-подключение-happ--incy)
- [💻 Профили для Mihomo и Sing-box](#-профили-для-mihomo-и-sing-box)
- [🔌 Интеграция с панелями управления (Remnawave / Marzban)](#-интеграция-с-панелями-управления)
- [📂 Структура репозитория](#-структура-репозитория)
- [🛠 Локальная сборка и разработка](#-локальная-сборка-и-разработка)
- [⚙️ Автоматизация CI/CD](#️-автоматизация-cicd)
- [❓ Частые вопросы (FAQ)](#-частые-вопросы-faq)

---

## 💡 Возможности и оптимизации

* 🍏 **Безопасно для памяти iOS (< 5 МБ RAM):** Размер `geosite.dat` составляет всего **~350 КБ**, а `geoip.dat` — **~750 КБ**. Никаких вылетов на iPhone и iPad (лимит iOS Network Extension — 15 МБ).
* 🧠 **AI & LLM Services (2026 Ready):** Оптимизированы маршруты для **Gemini (Google DeepMind)**, **ChatGPT**, **Claude**, **Perplexity**, **Cursor**, **Midjourney**, **xAI / Grok**, **Microsoft Copilot**, **Antigravity**.
* 🎮 **Стриминг и Игровые сервисы:**
  * **YouTube:** Видеопотоки (`googlevideo.com`, `ytimg.com`) идут через выделенный зарубежный канал.
  * **Discord:** Стабильные голосовые шлюзы (`gateway.discord.gg`), медиа и WebSockets.
  * **Twitch:** Стримы в 1080p напрямую (`geosite:twitch` ➔ direct), реклама блокируется через прокси (`geosite:twitch-ads`).
  * **Игры и Faceit:** Steam, Epic Games, Riot Games, EFT, Faceit (московские серверы) работают напрямую на максимальной скорости.
* 🏛 **Прямой доступ к Банкам и Госуслугам:** Сбер, Т-Банк, ВТБ, Альфа, Госуслуги, СБП, Налоговая, VK и Яндекс работают напрямую без капч.
* 🛡 **Блокировка рекламы:** Встроенная фильтрация рекламы (`category-ads`), телеметрии Windows (`win-spy`) и торрент-трекеров (`torrent`).

---

## 📱 Профили и быстрое подключение (Happ & INCY)

### 📊 Таблица профилей маршрутизации

| Профиль | Режим работы | RAM | Happ | INCY |
| :--- | :--- | :--- | :--- | :--- |
| **DEFAULT**<br>*(Рекомендуемый)* | **Split Tunneling:** RU/банки напрямую, AI/Discord/YouTube через VPN | `~3–5 МБ` | [⚡ Deeplink](HAPP/DEFAULT.DEEPLINK)<br>[📄 JSON](HAPP/DEFAULT.JSON) | [☁️ Autorouting](INCY/DEFAULT.AUTOROUTING)<br>[⚡ Deeplink](INCY/DEFAULT.DEEPLINK)<br>[📄 JSON](INCY/DEFAULT.JSON) |
| **WHITELIST** | **Строгий режим:** напрямую только реестр ЦБ РФ, Госуслуги, СБП | `~2 МБ` | [⚡ Deeplink](HAPP/WHITELIST.DEEPLINK)<br>[📄 JSON](HAPP/WHITELIST.JSON) | [☁️ Autorouting](INCY/WHITELIST.AUTOROUTING)<br>[⚡ Deeplink](INCY/WHITELIST.DEEPLINK)<br>[📄 JSON](INCY/WHITELIST.JSON) |
| **JSONSUB** | **Base DNS:** базовый профиль для ручной настройки правил | `~1 МБ` | [⚡ Deeplink](HAPP/JSONSUB.DEEPLINK)<br>[📄 JSON](HAPP/JSONSUB.JSON) | [☁️ Autorouting](INCY/JSONSUB.AUTOROUTING)<br>[⚡ Deeplink](INCY/JSONSUB.DEEPLINK)<br>[📄 JSON](INCY/JSONSUB.JSON) |

---

### 🚀 Инструкция по установке

#### 1. Для приложения Happ (iOS, Android, macOS, Windows)
1. Откройте файл нужного профиля (например, [`HAPP/DEFAULT.DEEPLINK`](HAPP/DEFAULT.DEEPLINK)) и скопируйте строку `happ://...`.
2. В приложении **Happ** откройте: **Настройки** ➔ **Правила маршрутизации** ➔ **Импортировать из буфера обмена**.

#### 2. Для приложения INCY (iOS, Android, Desktop)
* **Вариант А (Autorouting с автообновлением раз в 24ч — Рекомендуется):**
  1. Откройте [`INCY/DEFAULT.AUTOROUTING`](INCY/DEFAULT.AUTOROUTING) и скопируйте ссылку `incy://autorouting/...` (или чистый URL JSON-манифеста).
  2. В приложении **INCY** откройте: **Маршрутизация** ➔ **+** ➔ **Добавить по ссылке (Autorouting)** ➔ вставьте скопированную ссылку.
* **Вариант Б (Одноразовый импорт):**
  1. Откройте [`INCY/DEFAULT.DEEPLINK`](INCY/DEFAULT.DEEPLINK) и скопируйте строку `incy://routing/...`.
  2. В приложении **INCY** откройте: **Маршрутизация** ➔ **Импортировать из буфера обмена**.

---

## 💻 Профили для Mihomo и Sing-box

Готовые конфигурации находятся в каталоге [`MIHOMO/`](MIHOMO/):

* [`MIHOMO/default.yaml`](MIHOMO/default.yaml) — полный автономный конфиг с набором из 20+ бинарных rule-provider (`.mrs`).
* [`MIHOMO/template_remnawave.yaml`](MIHOMO/template_remnawave.yaml) — шаблон для панели Remnawave.

### Прямые ссылки на скомпилированные Rule-Sets:
* **Mihomo Rule-Sets (`.mrs`):** `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/<category>.mrs`
* **Sing-box Rule-Sets (`.srs`):** `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/sing-box/<category>.srs`
* **Архивы всех правил:**
  * [`mihomo.tar.gz`](https://github.com/mvrvntn/routing/releases/latest/download/mihomo.tar.gz)
  * [`sing-box.tar.gz`](https://github.com/mvrvntn/routing/releases/latest/download/sing-box.tar.gz)

---

## 🔌 Интеграция с панелями управления

### 1. Remnawave

#### А. Нативный Autorouting для INCY (Рекомендуемый)
В панели Remnawave перейдите в **Settings** ➔ **Subscription Settings / Response Rules**:
1. Создайте правило ответа для INCY (`User-Agent` содержит `incy`).
2. Укажите заголовок ответа:
   ```http
   autorouting: https://cdn.jsdelivr.net/gh/mvrvntn/routing@main/INCY/DEFAULT.JSON
   ```

#### Б. Автообновление диплинков Happ через `remnawave-routing-update`
Добавьте сервис в `docker-compose.yml` панели:

```yaml
services:
  remnawave-routing-update:
    image: ghcr.io/lifeindarkside/remnawave-routing-update:latest
    container_name: remnawave-routing-update
    restart: unless-stopped
    environment:
      - REMNA_BASE_URL=https://admin.mavrtun.ru/api
      - REMNA_TOKEN=your_api_token
      - GITHUB_RAW_URL=https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/HAPP/DEFAULT.DEEPLINK
      - CHECK_INTERVAL=43200
```

### 2. Marzban & Marzneshin

Инструкции по интеграции заголовков подписки находятся в папке [`ADDON_AUTOROUTING/`](ADDON_AUTOROUTING/):
* [`ADDON_AUTOROUTING/Marzban/`](ADDON_AUTOROUTING/Marzban) — передача заголовков `routing` / `autorouting` через кастомный `subscription.py`.
* [`ADDON_AUTOROUTING/Marzneshin/`](ADDON_AUTOROUTING/Marzneshin) — интеграция правил в подписки Marzneshin.

---

## 📂 Структура репозитория

```text
mvrvntn/routing/
├── .github/
│   └── workflows/
│       ├── update-configs.yml       # Автономный CI/CD пайплайн сборки
│       └── validate-pr.yml          # Автоматический линтер и валидатор
├── data/                            # Исходные списки доменов (25 категорий)
│   ├── ai, google-deepmind          # Искусственный интеллект (Gemini, ChatGPT, Claude)
│   ├── discord, youtube, telegram   # Медиа и стриминг
│   ├── category-ru, whitelist       # Банки РФ, Госуслуги, СБП
│   ├── steam, epicgames, faceit     # Игры и Faceit
│   └── category-ads, win-spy        # Блокируемая реклама и трекеры
├── geoip/                           # Конфигурация диапазонов IP
│   ├── config.json                  # Генерация geoip:direct
│   └── CUSTOM-LIST-ADD.txt          # Подсети исключений
├── HAPP/                            # Профили для Happ (DEFAULT, WHITELIST, JSONSUB)
├── INCY/                            # Профили для INCY (DEFAULT, WHITELIST, JSONSUB)
├── MIHOMO/                          # Шаблоны для Mihomo / Clash Meta
└── ADDON_AUTOROUTING/               # Скрипты интеграции с панелями
```

---

## 🛠 Локальная сборка и разработка

```bash
# 1. Сборка geosite.dat
git clone https://github.com/v2fly/domain-list-community.git /tmp/community
cp -r ./data/* /tmp/community/data/
cd /tmp/community && go run ./ -outputdir=./out
cp ./out/dlc.dat ./geosite.dat

# 2. Пересчет Base64 диплинков
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

## ⚙️ Автоматизация CI/CD

Пайплайн [`.github/workflows/update-configs.yml`](.github/workflows/update-configs.yml) автоматически:
1. Загружает актуальные базы IP (Antifilter, Re:filter, GeoLite2, IPinfo).
2. Собирает бинарные `geosite.dat` и `geoip.dat`.
3. Компилирует rule-set файлы `.mrs` (Mihomo) и `.srs` (Sing-box).
4. Публикует релиз и выгружает артефакты в ветку `release`.
5. Пересчитывает контрольные суммы и обновляет Deeplink-файлы.
6. Очищает кэш CDN jsDelivr.

---

## ❓ Частые вопросы (FAQ)

<details>
<summary><b>1. Почему на iPhone процесс не вылетает?</b></summary>

Лимит оперативной памяти iOS для фонового сетевого расширения составляет 15–30 МБ.
Стандартные базы на 750 000 доменов весят 35 МБ и в RAM занимают более 80 МБ, вызывая системный краш (`Jetsam kill`). Базы koridor занимают всего ~350 КБ, а процесс в RAM держится в пределах **3–5 МБ**, гарантируя 100% стабильность на iOS.
</details>

<details>
<summary><b>2. Почему сбоит Gemini на локации «АВТО» (балансировщик)?</b></summary>

Балансировщик Xray распределяет запросы одной сессии на разные серверы. Защита Google расценивает постоянную смену IP одного токена как взлом сессии и блокирует генерацию.
**Решение:** В шаблоне Xray закрепить теги `geosite:google-deepmind` и `geosite:ai` за одним конкретным узлом.
</details>

<details>
<summary><b>3. Как проверить, что банковские приложения идут напрямую?</b></summary>

Откройте сервис [ipinfo.io](https://ipinfo.io/) или проверьте геолокацию в приложении банка (Сбер, Т-Банк) — сервис покажет ваш реальный IP-адрес домашнего провайдера.
</details>

---

<div align="center">

[⭐ Поставьте Star репозиторию](https://github.com/mvrvntn/routing), чтобы поддержать проект!

</div>
