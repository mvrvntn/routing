<div align="center">

# 🚀 VPN Custom Routing (Happ & INCY & Mihomo)

**Высокопроизводительный, оптимизированный по памяти роутинг для [Happ](https://happ.su), [INCY](https://incy.cc), [Mihomo](https://github.com/MetaCubeX/mihomo) и [Remnawave](https://remnawave.com).**

> ⚡ **Хирургическая маршрутизация:** Все зарубежные ресурсы по умолчанию идут через VPN (`GlobalProxy: true`), российские сервисы и банки — напрямую (`direct`), а тяжелые базы РКН не забивают память iPhone (потребление RAM всего **3–5 МБ**).

**Таргет:** 🇷🇺 Россия + 🇧🇾 Беларусь

</div>

---

## 💡 Особенности и преимущества

- 🍏 **iOS Memory Safe (< 5 MB RAM):** Предотвращает аварийное завершение VPN по лимиту Network Extension (15 МБ) на iPhone и iPad.
- 🧠 **AI & LLM Services Out-of-the-box:** Гарантированное проксирование **Gemini, ChatGPT / OpenAI, Claude / Anthropic, Perplexity, Cursor, Midjourney, Grok**.
- 🎮 **Google Play & Discord & YouTube:** Полное исправление сессий Google Play Services на Android, разблокировка голосовых каналов Discord и видеопотоков YouTube.
- 🏛 **Direct для банков и Госуслуг:** Госуслуги, СБП, Налоговая, реестр ЦБ РФ, ВТБ, Сбер, Т-Банк, Альфа, Яндекс, VK работают на максимальной скорости домашнего провайдера.
- 🔄 **Полная автономия (GitHub Actions):** Автосборка `geosite.dat`, `geoip.dat`, `.mrs`, `.srs` и релизов в репозитории `mvrvntn/routing`.
- 🔌 **Интеграция с Remnawave:** Поддержка автоподстановки правил в подписки через `Remnawave-Routing-update`.

---

## 📱 Профили маршрутизации

### 1. Happ (iOS / Android / Desktop)
| Профиль | Описание | Deeplink | JSON |
| :--- | :--- | :--- | :--- |
| **DEFAULT** | 🌟 Рекомендуемый: RU direct, AI/YouTube/Discord proxy, реклама block | [DEFAULT.DEEPLINK](HAPP/DEFAULT.DEEPLINK) | [DEFAULT.JSON](HAPP/DEFAULT.JSON) |
| **WHITELIST** | Только сервисы и IP из белых списков РФ direct, всё остальное proxy | [WHITELIST.DEEPLINK](HAPP/WHITELIST.DEEPLINK) | [WHITELIST.JSON](HAPP/WHITELIST.JSON) |
| **JSONSUB** | Минимальный профиль: DNS + кастомные базы без встроенных правил | [JSONSUB.DEEPLINK](HAPP/JSONSUB.DEEPLINK) | [JSONSUB.JSON](HAPP/JSONSUB.JSON) |

### 2. INCY (iOS / Android)
| Профиль | Описание | Deeplink | JSON |
| :--- | :--- | :--- | :--- |
| **DEFAULT** | 🌟 Рекомендуемый: RU direct, AI/YouTube/Discord proxy, реклама block | [DEFAULT.DEEPLINK](INCY/DEFAULT.DEEPLINK) | [DEFAULT.JSON](INCY/DEFAULT.JSON) |
| **WHITELIST** | Только сервисы и IP из белых списков РФ direct, всё остальное proxy | [WHITELIST.DEEPLINK](INCY/WHITELIST.DEEPLINK) | [WHITELIST.JSON](INCY/WHITELIST.JSON) |
| **JSONSUB** | Минимальный профиль: DNS + кастомные базы без встроенных правил | [JSONSUB.DEEPLINK](INCY/JSONSUB.DEEPLINK) | [JSONSUB.JSON](INCY/JSONSUB.JSON) |

---

## 🛠 Автоматизация подписок в Remnawave

Инструкция по подключению автоматического обновления подписок через `Remnawave-Routing-update` доступна в [ADDON_AUTOROUTING/Remnawave](ADDON_AUTOROUTING/Remnawave/README.md).

---

## 📦 Прямые ссылки на базы данных (CDN & Releases)

* **GeoSite:** `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/geosite.dat`
* **GeoIP:** `https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/geoip.dat`
* **GitHub Releases:** `https://github.com/mvrvntn/routing/releases/latest`
