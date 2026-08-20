<div align="center">

# 🚀 koridor Routing

**Высокопроизводительный, оптимизированный по памяти репозиторий маршрутизации для [Happ](https://happ.su), [INCY](https://incy.cc), [Mihomo](https://github.com/MetaCubeX/mihomo), [Sing-box](https://github.com/SagerNet/sing-box) и [Remnawave](https://remnawave.com).**

> ⚡ **Хирургическая фильтрация:** Весь зарубежный интернет по умолчанию идет через VPN (`GlobalProxy: true`), российские сервисы и банки — напрямую (`direct`), а мобильные клиенты на iOS не вылетают по лимиту памяти (потребление RAM всего **3–5 МБ**).

[![Build & Update Routing](https://github.com/mvrvntn/routing/actions/workflows/update-configs.yml/badge.svg)](https://github.com/mvrvntn/routing/actions/workflows/update-configs.yml)
[![Validate Configs](https://github.com/mvrvntn/routing/actions/workflows/validate-pr.yml/badge.svg)](https://github.com/mvrvntn/routing/actions/workflows/validate-pr.yml)
[![Release](https://img.shields.io/github/v/release/mvrvntn/routing?color=blue&label=Release)](https://github.com/mvrvntn/routing/releases/latest)
[![jsDelivr CDN](https://data.jsdelivr.com/v1/package/gh/mvrvntn/routing@release/badge)](https://www.jsdelivr.com/package/gh/mvrvntn/routing)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Целевой регион:** 🇷🇺 Россия + 🇧🇾 Беларусь

</div>

---

## 📑 Содержание

- [💡 Ключевые возможности](#-ключевые-возможности)
- [🧠 Архитектура и принципы работы](#-архитектура-и-принципы-работы)
- [📱 Профили для Happ и INCY](#-профили-для-happ-и-incy)
- [💻 Профили для Mihomo и Sing-box](#-профили-для-mihomo-и-sing-box)
- [🔌 Интеграция с панелью Remnawave](#-интеграция-с-панелью-remnawave)
- [📂 Структура репозитория](#-структура-репозитория)
- [🛠 Локальная сборка и разработка](#-локальная-сборка-и-разработка)
- [⚙️ Автоматизация CI/CD (GitHub Actions)](#️-автоматизация-cicd-github-actions)
- [❓ Частые вопросы и Troubleshooting](#-частые-вопросы-и-troubleshooting)

---

## 💡 Ключевые возможности

* 🍏 **iOS Memory Safe (< 5 МБ RAM):** Гарантированная защита от аварийного завершения VPN на iPhone и iPad. В отличие от стандартных баз на 700 000 доменов (потребляющих 80+ МБ RAM и вызывающих системный `Jetsam kill` по лимиту 15 МБ), размер `geosite.dat` составляет всего **~350 КБ**, а `geoip.dat` — **~750 КБ**.
* 🧠 **AI & LLM Services (2026 Ready):** Гарантированное проксирование нейросетей — **Gemini (Google DeepMind)**, **ChatGPT (OpenAI)**, **Claude (Anthropic)**, **Perplexity**, **Cursor**, **Midjourney**, **xAI / Grok**, **Microsoft Copilot**, **Antigravity**.
* 🎮 **Discord & YouTube & Игры:**
  * **Discord:** Полная разблокировка голосовых каналов (`gateway.discord.gg`), медиа-серверов и CDN.
  * **YouTube:** Проксирование видеопотоков (`googlevideo.com`, `ytimg.com`) в обход замедления ТСПУ.
  * **Twitch:** Стримы в 1080p (Source) без лагов за счет прямого видеопотока (`geosite:twitch` ➔ direct) с вырезанием рекламы (`geosite:twitch-ads` ➔ proxy).
  * **Faceit:** Прямой маршрут к московским серверам для минимального пинга.
  * **Игровые платформы (Steam, Epic Games, Riot Games, Escape from Tarkov, EA Origin):** Обновления игр идут напрямую на максимальной скорости домашнего провайдера.
* 🏛 **Бесшовная работа Госуслуг и Банков РФ:** Госуслуги, СБП, Налоговая, реестр ЦБ РФ, ВТБ, Сбер, Т-Банк, Альфа, Яндекс, VK работают напрямую. Банки не блокируют вход и не ругаются на включенный VPN.
* 🤖 **Фикс Google Play / Android:** Устранено расщепление сессий сервисов Google Play Services и Firebase, вызывавшее сбои мобильного приложения Gemini.
* 🔄 **100% Автономный Monorepo CI/CD:** Автоматический pull баз Antifilter, Re:filter, MaxMind, IPinfo, DB-IP, компиляция бинарных `.dat`, `.mrs`, `.srs` и релизов в GitHub Actions.

---

## 🧠 Архитектура и принципы работы

Репозиторий использует архитектуру **«Хирургической фильтрации» (Targeted Routing)** на базе принципа `GlobalProxy: true`:

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
 (Мимо VPN в РФ)              (Через ноду VPN)            │
                                       ▲                  │
                                       │                  │
             Нет совпадения ───────────┴──────────────────┘
             (GlobalProxy = true)
```

1. **Порядок обработки (`RouteOrder: "block-proxy-direct"`):**
   * **`BlockSites`:** Телеметрия Windows (`geosite:win-spy`), публичные DHT-ноды BitTorrent (`geosite:torrent`), реклама (`geosite:category-ads`).
   * **`ProxySites`:** Сервисы, требующие гарантированного VPN-туннеля (YouTube, Discord, AI/Gemini, Telegram, GitHub).
   * **`DirectSites`:** Ресурсы, направляемые напрямую в РФ (банки, Госуслуги, Apple/Microsoft, Faceit, Steam, RU/BY домены).
   * **`Fallback`:** Все остальные неизвестные или зарубежные домены автоматически направляются в `proxy`.

---

## 📱 Профили для Happ и INCY

### Сравнение профилей

| Профиль | Назначение | Режим | Размер в RAM |
| :--- | :--- | :--- | :--- |
| **DEFAULT** (Рекомендуемый) | Оптимальный профиль для повседневного использования: RU/банки/игры напрямую, AI/Discord/YouTube через VPN, реклама заблокирована | `GlobalProxy: true` + `DirectSites` | ~3–5 МБ |
| **WHITELIST** | Строгий режим: напрямую идут только ресурсы из белых списков РФ; весь остальной интернет — через VPN | `Whitelist Direct` | ~2 МБ |
| **JSONSUB** | Базовый профиль: только DNS и ссылки на кастомные базы без предустановленных правил | `Base DNS only` | ~1 МБ |

### 1. Happ (iOS, Android, macOS, Windows)

| Профиль | Установка через Deeplink | Исходный JSON |
| :--- | :--- | :--- |
| **DEFAULT** | [⚡ Установить koridor DEFAULT](happ://routing/onadd/eyJOYW1lIjoia29yaWRvciIsIkdsb2JhbFByb3h5IjoidHJ1ZSIsIlVzZUNodW5rRmlsZXMiOiJ0cnVlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJHZW9pcHVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9tdnJ2bnRuL3JvdXRpbmdAcmVsZWFzZS9nZW9pcC5kYXQiLCJHZW9zaXRldXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL212cnZudG4vcm91dGluZ0ByZWxlYXNlL2dlb3NpdGUuZGF0IiwiTGFzdFVwZGF0ZWQiOiIxNzg3MjUyNTQ0IiwiRG5zSG9zdHMiOnsibGtmbDIubmFsb2cucnUiOiIyMTMuMjQuNjQuMTc1IiwibGtucGQubmFsb2cucnUiOiIyMTMuMjQuNjQuMTgxIn0sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTp3aGl0ZWxpc3QiLCJnZW9zaXRlOm1pY3Jvc29mdCIsImdlb3NpdGU6YXBwbGUiLCJnZW9zaXRlOmVwaWNnYW1lcyIsImdlb3NpdGU6cmlvdCIsImdlb3NpdGU6ZXNjYXBlZnJvbXRhcmtvdiIsImdlb3NpdGU6c3RlYW0iLCJnZW9zaXRlOm9yaWdpbiIsImdlb3NpdGU6dHdpdGNoIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOmZhY2VpdCJdLCJEaXJlY3RJcCI6WyJnZW9pcDpwcml2YXRlIiwiZ2VvaXA6ZGlyZWN0Il0sIlByb3h5U2l0ZXMiOlsiZ2Vvc2l0ZTpnb29nbGUtcGxheSIsImdlb3NpdGU6Z29vZ2xlLWRlZXBtaW5kIiwiZ2Vvc2l0ZTphaSIsImdlb3NpdGU6Z2l0aHViIiwiZ2Vvc2l0ZTp0d2l0Y2gtYWRzIiwiZ2Vvc2l0ZTp5b3V0dWJlIiwiZ2Vvc2l0ZTpkaXNjb3JkIiwiZ2Vvc2l0ZTp0ZWxlZ3JhbSIsImdlb3NpdGU6Y2F0ZWdvcnktZ2VvYmxvY2stcnUiXSwiUHJveHlJcCI6W10sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp0b3JyZW50IiwiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIn0=) | [HAPP/DEFAULT.JSON](HAPP/DEFAULT.JSON) |
| **WHITELIST** | [⚡ Установить koridor WHITELIST](happ://routing/onadd/eyJOYW1lIjoia29yaWRvciBXaGl0ZWxpc3QiLCJHbG9iYWxQcm94eSI6InRydWUiLCJVc2VDaHVua0ZpbGVzIjoidHJ1ZSIsIlJlbW90ZURucyI6IjguOC44LjgiLCJEb21lc3RpY0RucyI6Ijc3Ljg4LjguOCIsIlJlbW90ZUROU1R5cGUiOiJEb0giLCJSZW1vdGVETlNEb21haW4iOiJodHRwczovLzguOC44LjgvZG5zLXF1ZXJ5IiwiUmVtb3RlRE5TSVAiOiI4LjguOC44IiwiRG9tZXN0aWNETlNUeXBlIjoiRG9IIiwiRG9tZXN0aWNETlNEb21haW4iOiJodHRwczovLzc3Ljg4LjguOC9kbnMtcXVlcnkiLCJEb21lc3RpY0ROU0lQIjoiNzcuODguOC44IiwiR2VvaXB1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvbXZydm50bi9yb3V0aW5nQHJlbGVhc2UvZ2VvaXAuZGF0IiwiR2Vvc2l0ZXVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9tdnJ2bnRuL3JvdXRpbmdAcmVsZWFzZS9nZW9zaXRlLmRhdCIsIkxhc3RVcGRhdGVkIjoiMTc4NzI1MjU0NCIsIkRuc0hvc3RzIjp7ImxrZmwyLm5hbG9nLnJ1IjoiMjEzLjI0LjY0LjE3NSIsImxrbnBkLm5hbG9nLnJ1IjoiMjEzLjI0LjY0LjE4MSJ9LCJSb3V0ZU9yZGVyIjoiYmxvY2stcHJveHktZGlyZWN0IiwiRGlyZWN0U2l0ZXMiOlsiZ2Vvc2l0ZTpwcml2YXRlIiwiZ2Vvc2l0ZTp3aGl0ZWxpc3QiXSwiRGlyZWN0SXAiOlsiZ2VvaXA6cHJpdmF0ZSIsImdlb2lwOndoaXRlbGlzdCJdLCJQcm94eVNpdGVzIjpbXSwiUHJveHlJcCI6W10sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp0b3JyZW50IiwiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIn0=) | [HAPP/WHITELIST.JSON](HAPP/WHITELIST.JSON) |
| **JSONSUB** | [⚡ Установить koridor JSON](happ://routing/onadd/eyJOYW1lIjoia29yaWRvciBKU09OIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6ImZhbHNlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJHZW9pcHVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9tdnJ2bnRuL3JvdXRpbmdAcmVsZWFzZS9nZW9pcC5kYXQiLCJHZW9zaXRldXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL212cnZudG4vcm91dGluZ0ByZWxlYXNlL2dlb3NpdGUuZGF0IiwiTGFzdFVwZGF0ZWQiOiIxNzg3MjUyNTQ0IiwiRG5zSG9zdHMiOnsibGtmbDIubmFsb2cucnUiOiIyMTMuMjQuNjQuMTc1IiwibGtucGQubmFsb2cucnUiOiIyMTMuMjQuNjQuMTgxIn0sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6W10sIkRpcmVjdElwIjpbXSwiUHJveHlTaXRlcyI6WyJnZW9zaXRlOmNhdGVnb3J5LWdlb2Jsb2NrLXJ1Il0sIlByb3h5SXAiOltdLCJCbG9ja1NpdGVzIjpbXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIn0=) | [HAPP/JSONSUB.JSON](HAPP/JSONSUB.JSON) |

---

### 2. INCY (iOS, Android, Desktop)

> 💡 **Рекомендуется использовать Autorouting (incy://autorouting/):** Профиль привязывается к удаленному источнику (иконка облака ☁️ в приложении) и обновляется автоматически каждые 24 часа в фоновом режиме без необходимости повторного импорта!

| Профиль | 🔄 Автообновляемый (Autorouting) | ⚡ Одноразовый импорт (Routing) | Исходный JSON |
| :--- | :--- | :--- | :--- |
| **DEFAULT** (Рекомендуемый) | [☁️ Подключить Autorouting](incy://autorouting/onadd/https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/INCY/DEFAULT.JSON) | [⚡ Импортировать](incy://routing/onadd/eyJOYW1lIjoia29yaWRvciIsIkdsb2JhbFByb3h5IjoidHJ1ZSIsIlVzZUNodW5rRmlsZXMiOiJ0cnVlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJHZW9pcHVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9tdnJ2bnRuL3JvdXRpbmdAcmVsZWFzZS9nZW9pcC5kYXQiLCJHZW9zaXRldXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL212cnZudG4vcm91dGluZ0ByZWxlYXNlL2dlb3NpdGUuZGF0IiwiTGFzdFVwZGF0ZWQiOiIxNzg3MjUyNTQ0IiwiRG5zSG9zdHMiOnsibGtmbDIubmFsb2cucnUiOiIyMTMuMjQuNjQuMTc1IiwibGtucGQubmFsb2cucnUiOiIyMTMuMjQuNjQuMTgxIn0sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6WyJnZW9zaXRlOnByaXZhdGUiLCJnZW9zaXRlOmNhdGVnb3J5LXJ1IiwiZ2Vvc2l0ZTp3aGl0ZWxpc3QiLCJnZW9zaXRlOm1pY3Jvc29mdCIsImdlb3NpdGU6YXBwbGUiLCJnZW9zaXRlOmVwaWNnYW1lcyIsImdlb3NpdGU6cmlvdCIsImdlb3NpdGU6ZXNjYXBlZnJvbXRhcmtvdiIsImdlb3NpdGU6c3RlYW0iLCJnZW9zaXRlOm9yaWdpbiIsImdlb3NpdGU6dHdpdGNoIiwiZ2Vvc2l0ZTpwaW50ZXJlc3QiLCJnZW9zaXRlOmZhY2VpdCJdLCJEaXJlY3RJcCI6WyJnZW9pcDpwcml2YXRlIiwiZ2VvaXA6ZGlyZWN0Il0sIlByb3h5U2l0ZXMiOlsiZ2Vvc2l0ZTpnb29nbGUtcGxheSIsImdlb3NpdGU6Z29vZ2xlLWRlZXBtaW5kIiwiZ2Vvc2l0ZTphaSIsImdlb3NpdGU6Z2l0aHViIiwiZ2Vvc2l0ZTp0d2l0Y2gtYWRzIiwiZ2Vvc2l0ZTp5b3V0dWJlIiwiZ2Vvc2l0ZTpkaXNjb3JkIiwiZ2Vvc2l0ZTp0ZWxlZ3JhbSIsImdlb3NpdGU6Y2F0ZWdvcnktZ2VvYmxvY2stcnUiXSwiUHJveHlJcCI6W10sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp0b3JyZW50IiwiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIn0=) | [INCY/DEFAULT.JSON](INCY/DEFAULT.JSON) |
| **WHITELIST** | [☁️ Подключить Autorouting](incy://autorouting/onadd/https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/INCY/WHITELIST.JSON) | [⚡ Импортировать](incy://routing/onadd/eyJOYW1lIjoia29yaWRvciBXaGl0ZWxpc3QiLCJHbG9iYWxQcm94eSI6InRydWUiLCJVc2VDaHVua0ZpbGVzIjoidHJ1ZSIsIlJlbW90ZURucyI6IjguOC44LjgiLCJEb21lc3RpY0RucyI6Ijc3Ljg4LjguOCIsIlJlbW90ZUROU1R5cGUiOiJEb0giLCJSZW1vdGVETlNEb21haW4iOiJodHRwczovLzguOC44LjgvZG5zLXF1ZXJ5IiwiUmVtb3RlRE5TSVAiOiI4LjguOC44IiwiRG9tZXN0aWNETlNUeXBlIjoiRG9IIiwiRG9tZXN0aWNETlNEb21haW4iOiJodHRwczovLzc3Ljg4LjguOC9kbnMtcXVlcnkiLCJEb21lc3RpY0ROU0lQIjoiNzcuODguOC44IiwiR2VvaXB1cmwiOiJodHRwczovL2Nkbi5qc2RlbGl2ci5uZXQvZ2gvbXZydm50bi9yb3V0aW5nQHJlbGVhc2UvZ2VvaXAuZGF0IiwiR2Vvc2l0ZXVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9tdnJ2bnRuL3JvdXRpbmdAcmVsZWFzZS9nZW9zaXRlLmRhdCIsIkxhc3RVcGRhdGVkIjoiMTc4NzI1MjU0NCIsIkRuc0hvc3RzIjp7ImxrZmwyLm5hbG9nLnJ1IjoiMjEzLjI0LjY0LjE3NSIsImxrbnBkLm5hbG9nLnJ1IjoiMjEzLjI0LjY0LjE4MSJ9LCJSb3V0ZU9yZGVyIjoiYmxvY2stcHJveHktZGlyZWN0IiwiRGlyZWN0U2l0ZXMiOlsiZ2Vvc2l0ZTpwcml2YXRlIiwiZ2Vvc2l0ZTp3aGl0ZWxpc3QiXSwiRGlyZWN0SXAiOlsiZ2VvaXA6cHJpdmF0ZSIsImdlb2lwOndoaXRlbGlzdCJdLCJQcm94eVNpdGVzIjpbXSwiUHJveHlJcCI6W10sIkJsb2NrU2l0ZXMiOlsiZ2Vvc2l0ZTp3aW4tc3B5IiwiZ2Vvc2l0ZTp0b3JyZW50IiwiZ2Vvc2l0ZTpjYXRlZ29yeS1hZHMiXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIn0=) | [INCY/WHITELIST.JSON](INCY/WHITELIST.JSON) |
| **JSONSUB** | [☁️ Подключить Autorouting](incy://autorouting/onadd/https://raw.githubusercontent.com/mvrvntn/routing/refs/heads/main/INCY/JSONSUB.JSON) | [⚡ Импортировать](incy://routing/onadd/eyJOYW1lIjoia29yaWRvciBKU09OIiwiR2xvYmFsUHJveHkiOiJ0cnVlIiwiVXNlQ2h1bmtGaWxlcyI6ImZhbHNlIiwiUmVtb3RlRG5zIjoiOC44LjguOCIsIkRvbWVzdGljRG5zIjoiNzcuODguOC44IiwiUmVtb3RlRE5TVHlwZSI6IkRvSCIsIlJlbW90ZUROU0RvbWFpbiI6Imh0dHBzOi8vOC44LjguOC9kbnMtcXVlcnkiLCJSZW1vdGVETlNJUCI6IjguOC44LjgiLCJEb21lc3RpY0ROU1R5cGUiOiJEb0giLCJEb21lc3RpY0ROU0RvbWFpbiI6Imh0dHBzOi8vNzcuODguOC44L2Rucy1xdWVyeSIsIkRvbWVzdGljRE5TSVAiOiI3Ny44OC44LjgiLCJHZW9pcHVybCI6Imh0dHBzOi8vY2RuLmpzZGVsaXZyLm5ldC9naC9tdnJ2bnRuL3JvdXRpbmdAcmVsZWFzZS9nZW9pcC5kYXQiLCJHZW9zaXRldXJsIjoiaHR0cHM6Ly9jZG4uanNkZWxpdnIubmV0L2doL212cnZudG4vcm91dGluZ0ByZWxlYXNlL2dlb3NpdGUuZGF0IiwiTGFzdFVwZGF0ZWQiOiIxNzg3MjUyNTQ0IiwiRG5zSG9zdHMiOnsibGtmbDIubmFsb2cucnUiOiIyMTMuMjQuNjQuMTc1IiwibGtucGQubmFsb2cucnUiOiIyMTMuMjQuNjQuMTgxIn0sIlJvdXRlT3JkZXIiOiJibG9jay1wcm94eS1kaXJlY3QiLCJEaXJlY3RTaXRlcyI6W10sIkRpcmVjdElwIjpbXSwiUHJveHlTaXRlcyI6WyJnZW9zaXRlOmNhdGVnb3J5LWdlb2Jsb2NrLXJ1Il0sIlByb3h5SXAiOltdLCJCbG9ja1NpdGVzIjpbXSwiQmxvY2tJcCI6W10sIkRvbWFpblN0cmF0ZWd5IjoiSVBJZk5vbk1hdGNoIiwiRmFrZUROUyI6ImZhbHNlIn0=) | [INCY/JSONSUB.JSON](INCY/JSONSUB.JSON) |

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

## 🔌 Интеграция с панелью Remnawave

Для автоматической передачи правил маршрутизации в клиентские подписки используется сервис [Remnawave-Routing-update](https://github.com/lifeindarkside/Remnawave-Routing-update).

### Настройка на сервере Remnawave:

Добавьте сервис в `docker-compose.yml` панели управления:

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

> **Для пользователей INCY:** Замените `HAPP/DEFAULT.DEEPLINK` на `INCY/DEFAULT.DEEPLINK`.

Запустите контейнер:
```bash
docker compose up -d remnawave-routing-update
docker logs -f remnawave-routing-update
```

При каждом обновлении подписки клиентское приложение получит HTTP-заголовок `routing: happ://routing/onadd/...` и автоматически применит свежий роутинг.

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

### 2. Почему на iPhone VPN работает стабильно и не отваливается?
* Системный лимит iOS для фонового Network Extension составляет **15–30 МБ RAM**.
* Базы `koridor` занимают всего **~350 КБ**, а потребление оперативной памяти процессом VPN держится в пределах **3–5 МБ**, что полностью исключает завершение процесса операционной системой.

### 3. Как убедиться, что банковские приложения идут мимо VPN?
* Откройте сайт [2ip.ru](https://2ip.ru) или проверьте геолокацию в приложении банка (Сбербанк, Т-Банк). Банк покажет ваш реальный домашний IP и город подключения.

---

<div align="center">

**[⭐ Поставьте Star репозиторию](https://github.com/mvrvntn/routing)**, чтобы поддержать развитие проекта!

Сделано с ❤️ к свободному и быстрому интернету.

</div>
