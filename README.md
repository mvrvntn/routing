<div align="center">

# 🚀 koridor Routing

**Высокопроизводительный, оптимизированный по памяти репозиторий умной маршрутизации и раздельного туннелирования (Split Tunneling) для [Happ](https://happ.su), [INCY](https://incy.cc), [Mihomo](https://github.com/MetaCubeX/mihomo), [Sing-box](https://github.com/SagerNet/sing-box) и [Remnawave](https://docs.rw).**

> ⚡ **Раздельное туннелирование (Split Tunneling):** Зарубежные сервисы и глобальные веб-ресурсы направляются через удаленный шлюз (`GlobalProxy: true`), а российские сервисы, банки и локальные ресурсы — напрямую через домашнего провайдера (`direct`) с нулевой задержкой, защитой от капч и минимальным потреблением RAM (**3–5 МБ**).

[![Build & Update Routing](https://github.com/mvrvntn/routing/actions/workflows/update-configs.yml/badge.svg)](https://github.com/mvrvntn/routing/actions/workflows/update-configs.yml)
[![Validate Configs](https://github.com/mvrvntn/routing/actions/workflows/validate-pr.yml/badge.svg)](https://github.com/mvrvntn/routing/actions/workflows/validate-pr.yml)
[![Release](https://img.shields.io/github/v/release/mvrvntn/routing?color=blue&label=Release)](https://github.com/mvrvntn/routing/releases/latest)
[![jsDelivr CDN](https://img.shields.io/badge/jsDelivr-CDN-orange.svg)](https://www.jsdelivr.com/package/gh/mvrvntn/routing)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Целевой регион:** 🇷🇺 Россия + 🇧🇾 Беларусь

</div>

---

## 📑 Содержание

- [💡 Ключевые возможности](#-ключевые-возможности)
- [🧠 Архитектура и принципы работы](#-архитектура-и-принципы-работы)
- [📱 Профили для Happ и INCY](#-профили-для-happ-и-incy)
- [💻 Профили для Mihomo и Sing-box](#-профили-для-mihomo-и-sing-box)
- [🔌 Интеграция с панелями управления](#-интеграция-с-панелями-управления)
- [📂 Структура репозитория](#-структура-репозитория)
- [🛠 Локальная сборка и разработка](#-локальная-сборка-и-разработка)
- [⚙️ Автоматизация CI/CD (GitHub Actions)](#️-автоматизация-cicd-github-actions)
- [❓ Частые вопросы и Troubleshooting](#-частые-вопросы-и-troubleshooting)

---

## 💡 Ключевые возможности

* 🍏 **iOS Memory Safe (< 5 МБ RAM):** Защита от аварийного завершения фонового процесса сетевого расширения на iPhone и iPad. В отличие от стандартных баз на 700 000 доменов (потребляющих 80+ МБ RAM и вызывающих системный `Jetsam kill` по лимиту 15 МБ), размер `geosite.dat` составляет всего **~350 КБ**, а `geoip.dat` — **~750 КБ**.
* 🧠 **AI & LLM Services (2026 Ready):** Оптимизированная маршрутизация для API искусственного интеллекта и сервисов: **Gemini (Google DeepMind)**, **ChatGPT (OpenAI)**, **Claude (Anthropic)**, **Perplexity**, **Cursor**, **Midjourney**, **xAI / Grok**, **Microsoft Copilot**, **Antigravity**.
* 🎮 **Discord, Видеостриминг и Игровые сервисы:**
  * **Discord:** Стабильная маршрутизация голосовых шлюзов (`gateway.discord.gg`), медиа-серверов и WebSockets.
  * **YouTube & Видеоплатформы:** Прямое распределение видеопотоков (`googlevideo.com`, `ytimg.com`) через оптимизированный зарубежный канал.
  * **Twitch:** Стримы в 1080p (Source) без задержек за счет прямого видеопотока (`geosite:twitch` ➔ direct) с фильтрацией рекламы (`geosite:twitch-ads` ➔ proxy).
  * **Faceit:** Прямой маршрут к московским серверам для минимального сетевого пинга.
  * **Игровые платформы (Steam, Epic Games, Riot Games, Escape from Tarkov, EA Origin):** Загрузка и обновления игр идут напрямую на максимальной скорости домашнего интернет-соединения.
* 🏛 **Прямой доступ к Госуслугам и Банкам РФ:** Госуслуги, СБП, Налоговая, реестр ЦБ РФ, ВТБ, Сбер, Т-Банк, Альфа, Яндекс, VK работают напрямую по локальному IP без капч и ограничений.
* 🤖 **Оптимизация Google Play / Android:** Корректное разделение сессий Google Play Services и Firebase для стабильной работы мобильных приложений.
* 🔄 **100% Автономный Monorepo CI/CD:** Автоматический pull баз данных, компиляция бинарных `.dat`, `.mrs`, `.srs` и публикация релизов в GitHub Actions.

---

## 🧠 Архитектура и принципы работы

Репозиторий использует архитектуру **«Раздельного туннелирования» (Split Tunneling & Targeted Routing)** на базе принципа `GlobalProxy: true`:

```
                           ┌───────────────────────────┐
                           │   Входящий сетевой запрос │
                           └─────────────┬─────────────┘
                                         │
                        ┌────────────────┴────────────────┐
                        ▼                                 ▼
              [ Доменное имя (FQDN) ]            [ IP-адрес назначения ]
                        │                                 │
         ┌──────────────┴──────────────┐                  │
         │                             │                  │
   Совпадение с                  Совпадение с             │
   DirectSites?                  ProxySites?              │
   (RU, Банки, Игры)             (AI, Discord, YT)        │
         │                             │                  │
         ▼                             ▼                  │
    [ DIRECT ]                    [ PROXY ]               │
 (Напрямую через РФ)           (Через сетевой узел)       │
                                       ▲                  │
                                       │                  │
             Нет совпадения ───────────┴──────────────────┘
             (GlobalProxy = true)
```

1. **Порядок обработки (`RouteOrder: "block-proxy-direct"`):**
   * **`BlockSites`:** Телеметрия Windows (`geosite:win-spy`), публичные DHT-ноды BitTorrent (`geosite:torrent`), реклама (`geosite:category-ads`).
   * **`ProxySites`:** Сервисы, направляемые через удаленный защищенный узел (YouTube, Discord, AI/Gemini, Telegram, GitHub).
   * **`DirectSites`:** Ресурсы, направляемые напрямую провайдером в РФ (банки, Госуслуги, Apple/Microsoft, Faceit, Steam, RU/BY домены).
   * **`Fallback`:** Все остальные неизвестные или зарубежные домены автоматически направляются в `proxy`.

---

## 📱 Профили для Happ и INCY

### Сравнение профилей

| Профиль | Назначение | Режим | Размер в RAM |
| :--- | :--- | :--- | :--- |
| **DEFAULT** (Рекомендуемый) | Оптимальный профиль: RU/банки/игры напрямую, AI/Discord/YouTube через удаленный шлюз, реклама заблокирована | `GlobalProxy: true` + `DirectSites` | ~3–5 МБ |
| **WHITELIST** | Строгий режим: напрямую идут только проверенные ресурсы из белых списков РФ; весь остальной трафик — через удаленный узел | `Whitelist Direct` | ~2 МБ |
| **JSONSUB** | Базовый профиль: только DNS и ссылки на кастомные базы без предустановленных правил | `Base DNS only` | ~1 МБ |

### 1. Happ (iOS, Android, macOS, Windows)

| Профиль | Установка через Deeplink | Исходный JSON |
| :--- | :--- | :--- |
| **DEFAULT** | [⚡ Установить koridor](happ://routing/onadd/eyJOYW1lIjoia29yaWRvciIsIkdsb2JhbFByb3h5IjoidHJ1ZSIsIlVzZUNodW5rRmlsZXMiOiJ0cnVlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU1RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJHZW9pcHVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9tdnJ2bnRuL3JvdXRpbmdAcmVsZWFzZS9nZW9pcC5kYXQiLCJHZW9zaXRldXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL212cnZudG4vcm91dGluZ0ByZWxlYXNlL2dlb3NpdGUuZGF0IiwiTGFzdFVwZGF0ZWQiOiIxNzg3MjUyNTQ0IiwiRG5zSG9zdHMiOnsibGtmbDIubmFsb2cucnUiOiIyMTMuMjQuNjQuMTc1IiwibGtucGQubmFsb2cucnUiOiIyMTMuMjQuNjQuMTgxIn0sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTp3aGl0ZWxpc3QiLCJnZW9zaXRlOm1pY3Jvc29mdCIsImdlb3NpdGU6YXBwbGUiLCJnZW9zaXRlOmVwaWNnYW1lcyIsImdlb3NpdGU6cmlvdCIsImdlb3NpdGU6ZXNjYXBlZnJvbXRhcmtvdiIsImdlb3NpdGU6c3RlYW0iLCJnZW9zaXRlOm9yaWdpbiIsImdlb3NpdGU6dHdpdGNoIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOmZhY2VpdCJdLCJEaXJlY3RJcCI6WyJnZW9pcDpwcml2YXRlIiwiZ2VvaXA6ZGlyZWN0Il0sIlByb3h5U2l0ZXMiOlsiZ2Vvc2l0ZTpnb29nbGUtcGxheSIsImdlb3NpdGU6Z29vZ2xlLWRlZXBtaW5kIiwiZ2Vvc2l0ZTphaSIsImdlb3NpdGU6Z2l0aHViIiwiZ2Vvc2l0ZTp0d2l0Y2gtYWRzIiwiZ2Vvc2l0ZTp5b3V0dWJlIiwiZ2Vvc2l0ZTpkaXNjb3JkIiwiZ2Vvc2l0ZTp0ZWxlZ3JhbSIsImdlb3NpdGU6Y2F0ZWdvcnktZ2VvYmxvY2stcnUiXSwiUHJveHlJcCI6W10sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp0b3JyZW50IiwiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIn0=) | [HAPP/DEFAULT.JSON](HAPP/DEFAULT.JSON) |
| **WHITELIST** | [⚡ Установить koridor (Whitelist)](happ://routing/onadd/eyJOYW1lIjoia29yaWRvciAoV2hpdGVsaXN0KSIsIkdsb2JhbFByb3h5IjoidHJ1ZSIsIlVzZUNodW5rRmlsZXMiOiJ0cnVlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU1RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJHZW9pcHVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9tdnJ2bnRuL3JvdXRpbmdAcmVsZWFzZS9nZW9pcC5kYXQiLCJHZW9zaXRldXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL212cnZudG4vcm91dGluZ0ByZWxlYXNlL2dlb3NpdGUuZGF0IiwiTGFzdFVwZGF0ZWQiOiIxNzg3MjUyNTQ0IiwiRG5zSG9zdHMiOnsibGtmbDIubmFsb2cucnUiOiIyMTMuMjQuNjQuMTc1IiwibGtucGQubmFsb2cucnUiOiIyMTMuMjQuNjQuMTgxIn0sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOndoaXRlbGlzdCJdLCJEaXJlY3RJcCI6WyJnZW9pcDpwcml2YXRlIiwiZ2VvaXA6d2hpdGVsaXN0Il0sIlByb3h5U2l0ZXMiOltdLCJQcm94eUlwIjpbXSwiQmxvY2tTaXRlcyI6WyJnZW9zaXRlOndpbi1zcHkiLCJnZW9zaXRlOnRvcnJlbnQiLCJnZW9zaXRlOmNhdGVnb3J5LWFkcyJdLCJCbG9ja0lwIjpbXSwiRG9tYWluU3RyYXRlZ3kiOiJJUElmTm9uTWF0Y2giLCJGYWtlRE5TIjoiZmFsc2UifQ==) | [HAPP/WHITELIST.JSON](HAPP/WHITELIST.JSON) |
| **JSONSUB** | [⚡ Установить koridor (JSON)](happ://routing/onadd/eyJOYW1lIjoia29yaWRvciAoSlNPTikiLCJHbG9iYWxQcm94eSI6InRydWUiLCJVc2VDaHVua0ZpbGVzIjoiZmFsc2UiLCJSZW1vdGVEbnMiOiI4LjguOC44IiwiRG9tZXN0aWNEbnMiOiI3Ny44OC44LjgiLCJSZW1vdGVETlNUeXBlIjoiRG9IIiwiUmVtb3RlRE5TRG9tYWluIjoiaHR0cHM6Ly84LjguOC44L2Rucy1xdWVyeSIsIlJlbW90ZUROU0lQIjoiOC44LjguOCIsIkRvbWVzdGljRE5TVHlwZSI6IkRvSCIsIkRvbWVzdGljRE5TRG9tYWluIjoiaHR0cHM6Ly83Ny44OC44LjgvZG5zLXF1ZXJ5IiwiRG9tZXN0aWNETlNJUCI6Ijc3Ljg4LjguOCIsIkdlb2lwdXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL212cnZudG4vcm91dGluZ0ByZWxlYXNlL2dlb2lwLmRhdCIsIkdlb3NpdGV1cmwiOiiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL212cnZudG4vcm91dGluZ0ByZWxlYXNlL2dlb3NpdGUuZGF0IiwiTGFzdFVwZGF0ZWQiOiIxNzg3MjUyNTQ0IiwiRG5zSG9zdHMiOnsibGtmbDIubmFsb2cucnUiOiIyMTMuMjQuNjQuMTc1IiwibGtucGQubmFsb2cucnUiOiIyMTMuMjQuNjQuMTgxIn0sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6W10sIkRpcmVjdElwIjpbXSwiUHJveHlTaXRlcyI6WyJnZW9zaXRlOmNhdGVnb3J5LWdlb2Jsb2NrLXJ1Il0sIlByb3h5SXAiOltdLCJCbG9ja1NpdGVzIjpbXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIn0=) | [HAPP/JSONSUB.JSON](HAPP/JSONSUB.JSON) |

### 2. INCY (iOS, Android, Desktop)

> 💡 **Рекомендуется использовать Autorouting (incy://autorouting/):** Профиль привязывается к удаленному источнику (иконка облака ☁️ в приложении) и обновляется автоматически каждые 24 часа в фоновом режиме без необходимости повторного импорта!

| Профиль | 🔄 Автообновляемый (Autorouting) | ⚡ Одноразовый импорт (Routing) | Исходный JSON |
| :--- | :--- | :--- | :--- |
| **DEFAULT** (Рекомендуемый) | [☁️ Подключить Autorouting](incy://autorouting/onadd/https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/INCY/DEFAULT.JSON) | [⚡ Импортировать](incy://routing/onadd/eyJOYW1lIjoia29yaWRvciIsIkdsb2JhbFByb3h5IjoidHJ1ZSIsIlVzZUNodW5rRmlsZXMiOiJ0cnVlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJHZW9pcHVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9tdnJ2bnRuL3JvdXRpbmdAcmVsZWFzZS9nZW9pcC5kYXQiLCJHZW9zaXRldXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL212cnZudG4vcm91dGluZ0ByZWxlYXNlL2dlb3NpdGUuZGF0IiwiTGFzdFVwZGF0ZWQiOiIxNzg3MjU1MjU3IiwiRG5zSG9zdHMiOnsibGtmbDIubmFsb2cucnUiOiIyMTMuMjQuNjQuMTc1IiwibGtucGQubmFsb2cucnUiOiIyMTMuMjQuNjQuMTgxIn0sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTp3aGl0ZWxpc3QiLCJnZW9zaXRlOm1pY3Jvc29mdCIsImdlb3NpdGU6YXBwbGUiLCJnZW9zaXRlOmVwaWNnYW1lcyIsImdlb3NpdGU6cmlvdCIsImdlb3NpdGU6ZXNjYXBlZnJvbXRhcmtvdiIsImdlb3NpdGU6c3RlYW0iLCJnZW9zaXRlOm9yaWdpbiIsImdlb3NpdGU6dHdpdGNoIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOmZhY2VpdCJdLCJEaXJlY3RJcCI6WyJnZW9pcDpwcml2YXRlIiwiZ2VvaXA6ZGlyZWN0Il0sIlByb3h5U2l0ZXMiOlsiZ2Vvc2l0ZTpnb29nbGUtcGxheSIsImdlb3NpdGU6Z29vZ2xlLWRlZXBtaW5kIiwiZ2Vvc2l0ZTphaSIsImdlb3NpdGU6Z2l0aHViIiwiZ2Vvc2l0ZTp0d2l0Y2gtYWRzIiwiZ2Vvc2l0ZTp5b3V0dWJlIiwiZ2Vvc2l0ZTpkaXNjb3JkIiwiZ2Vvc2l0ZTp0ZWxlZ3JhbSIsImdlb3NpdGU6Y2F0ZWdvcnktZ2VvYmxvY2stcnUiXSwiUHJveHlJcCI6W10sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp0b3JyZW50IiwiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIn0=) | [INCY/DEFAULT.JSON](INCY/DEFAULT.JSON) |
| **WHITELIST** | [☁️ Подключить Autorouting](incy://autorouting/onadd/https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/INCY/WHITELIST.JSON) | [⚡ Импортировать](incy://routing/onadd/eyJOYW1lIjoia29yaWRvciAoV2hpdGVsaXN0KSIsIkdsb2JhbFByb3h5IjoidHJ1ZSIsIlVzZUNodW5rRmlsZXMiOiJ0cnVlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJHZW9pcHVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9tdnJ2bnRuL3JvdXRpbmdAcmVsZWFzZS9nZW9pcC5kYXQiLCJHZW9zaXRldXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL212cnZudG4vcm91dGluZ0ByZWxlYXNlL2dlb3NpdGUuZGF0IiwiTGFzdFVwZGF0ZWQiOiIxNzg3MjU1MjU3IiwiRG5zSG9zdHMiOnsibGtmbDIubmFsb2cucnUiOiIyMTMuMjQuNjQuMTc1IiwibGtucGQubmFsb2cucnUiOiIyMTMuMjQuNjQuMTgxIn0sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOndoaXRlbGlzdCJdLCJEaXJlY3RJcCI6WyJnZW9pcDpwcml2YXRlIiwiZ2VvaXA6d2hpdGVsaXN0Il0sIlByb3h5U2l0ZXMiOltdLCJQcm94eUlwIjpbXSwiQmxvY2tTaXRlcyI6WyJnZW9zaXRlOndpbi1zcHkiLCJnZW9zaXRlOnRvcnJlbnQiLCJnZW9zaXRlOmNhdGVnb3J5LWFkcyJdLCJCbG9ja0lwIjpbXSwiRG9tYWluU3RyYXRlZ3kiOiJJUElmTm9uTWF0Y2giLCJGYWtlRE5TIjoiZmFsc2UifQ==) | [INCY/WHITELIST.JSON](INCY/WHITELIST.JSON) |
| **JSONSUB** | [☁️ Подключить Autorouting](incy://autorouting/onadd/https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/INCY/JSONSUB.JSON) | [⚡ Импортировать](incy://routing/onadd/eyJOYW1lIjoia29yaWRvciAoSlNPTikiLCJHbG9iYWxQcm94eSI6InRydWUiLCJVc2VDaHVua0ZpbGVzIjoiZmFsc2UiLCJSZW1vdGVEbnMiOiI4LjguOC44IiwiRG9tZXN0aWNEbnMiOiI3Ny44OC44LjgiLCJSZW1vdGVETlNUeXBlIjoiRG9IIiwiUmVtb3RlRE5TRG9tYWluIjoiaHR0cHM6Ly84LjguOC44L2Rucy1xdWVyeSIsIlJlbW90ZUROU0lQIjoiOC44LjguOCIsIkRvbWVzdGljRE5TVHlwZSI6IkRvSCIsIkRvbWVzdGljRE5TRG9tYWluIjoiaHR0cHM6Ly83Ny44OC44LjgvZG5zLXF1ZXJ5IiwiRG9tZXN0aWNETlNJUCI6Ijc3Ljg4LjguOCIsIkdlb2lwdXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL212cnZudG4vcm91dGluZ0ByZWxlYXNlL2dlb2lwLmRhdCIsIkdlb3NpdGV1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvbXZydm50bi9yb3V0aW5nQHJlbGVhc2UvZ2Vvc2l0ZS5kYXQiLCJMYXN0VXBkYXRlZCI6IjE3ODcyNTUyNTciLCJEbnNIb3N0cyI6eyJsa2ZsMi5uYWxvZy5ydSI6IjIxMy4yNC42NC4xNzUiLCJsa25wZC5uYWxvZy5ydSI6IjIxMy4yNC42NC4xODEifSwiUm91dGVPcmRlciI6ImJsb2NrLXByb3h5LWRpcmVjdCIsIkRpcmVjdFNpdGVzIjpbXSwiRGlyZWN0SXAiOltdLCJQcm94eVNpdGVzIjpbImdlb3NpdGU6Y2F0ZWdvcnktZ2VvYmxvY2stcnUiXSwiUHJveHlJcCI6W10sIkJsb2NrU2l0ZXMiOltdLCJCbG9ja0lwIjpbXSwiRG9tYWluU3RyYXRlZ3kiOiJJUElmTm9uTWF0Y2giLCJGYWtlRE5TIjoiZmFsc2UifQ==) | [INCY/JSONSUB.JSON](INCY/JSONSUB.JSON) |

---

## 💻 Профили для Mihomo и Sing-box

Готовые конфигурации находятся в каталоге [`MIHOMO/`](MIHOMO/):

* [`MIHOMO/default.yaml`](MIHOMO/default.yaml) — полный автономный конфиг с набором из 20+ бинарных rule-provider (`.mrs`).
* [`MIHOMO/template_remnawave.yaml`](MIHOMO/template_remnawave.yaml) — шаблон для панели Remnawave.

### Прямые ссылки на скомпилированные Rule-Sets:
* **Mihomo Rule-Sets (`.mrs`):** `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/<category>.mrs`
* **Sing-box Rule-Sets (`.srs`):** `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/sing-box/<category>.srs`
* **Архивы всех правил:**
  * `https://github.com/mvrvntn/routing/releases/latest/download/mihomo.tar.gz`
  * `https://github.com/mvrvntn/routing/releases/latest/download/sing-box.tar.gz`

---

## 🔌 Интеграция с панелями управления

### 1. Remnawave

#### А. Нативный Autorouting для INCY (Рекомендуемый)
В панели Remnawave перейдите в **Settings** ➔ **Subscription Settings / Response Rules**:
1. Создайте правило ответа для INCY (`User-Agent` содержит `incy`).
2. Укажите заголовок ответа:
   ```http
   autorouting: https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/INCY/DEFAULT.JSON
   ```
> 🚀 Клиенты INCY автоматически подключат автообновляемый профиль `koridor` с иконкой облака ☁️ и будут обновлять его раз в 24 часа.

#### Б. Автообновление диплинков Happ через `remnawave-routing-update`
Добавьте сервис в `docker-compose.yml` панели:

```yaml
services:
  remnawave-routing-update:
    image: ghcr.io/lifeindarkside/remnawave-routing-update:latest
    container_name: remnawave-routing-update
    restart: unless-stopped
    environment:
      # URL API панели Remnawave
      - REMNA_BASE_URL=https://panel.yourdomain.com/api
      # API токен (Panel -> Settings -> API Tokens)
      - REMNA_TOKEN=your_remnawave_api_token
      # Ссылка на актуальный диплинк koridor
      - GITHUB_RAW_URL=https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/HAPP/DEFAULT.DEEPLINK
      # Интервал проверки обновлений (в секундах)
      - CHECK_INTERVAL=300
```

Запустите контейнер:
```bash
docker compose up -d remnawave-routing-update
```

---

### 2. Marzban & Marzneshin

Подробные инструкции и шаблоны модификации скриптов подписки для Marzban и Marzneshin находятся в директории [`ADDON_AUTOROUTING/`](ADDON_AUTOROUTING/):
* [`ADDON_AUTOROUTING/Marzban/`](ADDON_AUTOROUTING/Marzban/) — инъекция заголовков `routing` / `autorouting` через кастомный `subscription.py`.
* [`ADDON_AUTOROUTING/Marzneshin/`](ADDON_AUTOROUTING/Marzneshin/) — передача правил в подписки Marzneshin.

---

## 📂 Структура репозитория

```
mvrvntn/routing/
├── .github/
│   ├── ISSUE_TEMPLATE/              # Интерактивные формы Issue (домены, багрепорты)
│   ├── PULL_REQUEST_TEMPLATE.md     # Чек-лист для Pull Request
│   └── workflows/
│       ├── update-configs.yml       # Единый автономный CI/CD пайплайн сборщика
│       └── validate-pr.yml          # Автоматический линтер и валидатор PR
├── data/                            # Исходные списки доменов (25 категорий)
│   ├── ai                           # OpenAI, Claude, Perplexity, Cursor, Grok, Copilot
│   ├── google-deepmind              # Gemini, AI Studio, Generative Language API, Antigravity
│   ├── google-play                  # Google Play Services, Firebase, OTA updates
│   ├── discord                      # Voice Gateways, Media CDN, Discord WebSockets
│   ├── youtube                      # YouTube, Googlevideo CDN, ytimg
│   ├── telegram                     # Telegram Web, CDN, t.me
│   ├── category-geoblock-ru         # Зарубежные сервисы, блокирующие пользователей из РФ
│   ├── category-ru                  # Зона .RU/.РФ, VK, Яндекс, Mail.ru, сервисы РФ
│   ├── whitelist                    # Банки РФ (реестр ЦБ), Госуслуги, СБП, Налоговая
│   ├── twitch                       # Twitch Video Stream (direct)
│   ├── twitch-ads                   # Twitch Ads Blocker (proxy)
│   ├── steam, epicgames, riot...    # Игровые платформы и Faceit
│   └── win-spy, torrent, category-ads # Блокируемые трекеры и реклама
├── geoip/                           # Конфигурация и списки исключений для GeoIP
│   ├── config.json                  # Правила генерации geoip:direct
│   └── CUSTOM-LIST-ADD.txt          # Подсети Apple Push, казенные CDN
├── HAPP/                            # Конфигурации и диплинки для Happ
│   ├── DEFAULT.JSON & .DEEPLINK
│   ├── WHITELIST.JSON & .DEEPLINK
│   └── JSONSUB.JSON & .DEEPLINK
├── INCY/                            # Конфигурации и диплинки для INCY
│   ├── DEFAULT.JSON & .AUTOROUTING & .DEEPLINK
│   ├── WHITELIST.JSON & .AUTOROUTING & .DEEPLINK
│   └── JSONSUB.JSON & .AUTOROUTING & .DEEPLINK
├── MIHOMO/                          # Шаблоны для Mihomo / Clash Meta
└── ADDON_AUTOROUTING/               # Документация интеграций с панелями (Remnawave, Marzban, etc.)
```

---

## 🛠 Локальная сборка и разработка

### Требования:
- **Go** 1.22+
- **Python** 3.10+
- **Git**, `jq`

### 1. Сборка `geosite.dat` локально:
```bash
git clone https://github.com/v2fly/domain-list-community.git /tmp/community
cp -r ./data/* /tmp/community/data/
cd /tmp/community && go run ./ -outputdir=./out
cp ./out/dlc.dat ./geosite.dat
```

### 2. Пересчет Base64 диплинков:
```bash
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

## ⚙️ Автоматизация CI/CD (GitHub Actions)

Пайплайн [`.github/workflows/update-configs.yml`](.github/workflows/update-configs.yml) выполняет:
1. Загрузку свежих баз IP (Antifilter, Re:filter, GeoLite2, IPinfo, DB-IP).
2. Сборку `geosite.dat` и `geoip.dat` через официальные компиляторы Go.
3. Генерацию бинарных правил `.mrs` (Mihomo) и `.srs` (Sing-box).
4. Создание релиза с тегом даты `YYYYMMDDHHMM` и выгрузку в ветку `release`.
5. Пересчет таймстемпов, ссылок и генерацию `.DEEPLINK`.
6. Очистку кэша CDN jsDelivr.

---

## ❓ Частые вопросы и Troubleshooting

### 1. Почему на локации «АВТО» (балансировщик) сбоит Gemini?
* **Причина:** Балансировщик Xray со стратегией `leastLoad` распределяет запросы сессии на разные ноды (Финляндия ➔ Нидерланды ➔ Турция). Защита Google расценивает частую смену IP одного сессионного токена как попытку взлома (Session Hijacking) и блокирует генерацию.
* **Решение:** В шаблоне балансировщика Xray закрепить домены AI за одной быстрой и чистой нодой:
  ```json
  {
    "type": "field",
    "domain": [
      "geosite:google-deepmind",
      "geosite:ai"
    ],
    "outboundTag": "<ВАШ_ВЫДЕЛЕННЫЙ_УЗЕЛ>"
  }
  ```

### 2. Почему на iPhone процесс туннелирования работает стабильно и не вылетает?
* Системный лимит iOS для фонового процесса Network Extension составляет **15–30 МБ RAM**.
* Базы `koridor` занимают всего **~350 КБ**, а потребление оперативной памяти процессом держится в пределах **3–5 МБ**, что полностью исключает принудительное завершение процесса операционной системой.

### 3. Как убедиться, что банковские приложения идут напрямую через домашнего провайдера?
* Откройте сайт [ipinfo.io](https://ipinfo.io) или проверьте геолокацию в приложении банка (Сбербанк, Т-Банк). Сервис покажет ваш реальный IP-адрес домашнего интернет-провайдера.

---

<div align="center">

**[⭐ Поставьте Star репозиторию](https://github.com/mvrvntn/routing)**, чтобы поддержать развитие проекта!

Сделано с ❤️ для качественного, стабильного и быстрого интернета.

</div>
