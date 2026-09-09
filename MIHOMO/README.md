# 🚀 Mihomo (Clash Meta) — Маршрутизация и Rule-Sets

Набор правил и готовых конфигураций для ядра [Mihomo](https://github.com/MetaCubeX/mihomo) (Clash.Meta), оптимизированный для пользователей из РФ и Беларуси.

Все списки скомпилированы в бинарный формат **MRS** (*Mihomo Rule-Set*, бинарное дерево radix-tree/protobuf), загружаются ядром за миллисекунды и практически не потребляют оперативную память.

---

## 📂 Файлы в этой директории

| Файл | Назначение |
| :--- | :--- |
| [`default.yaml`](default.yaml) | Полный рабочий конфиг с DNS, сниффером, группами прокси и правилами. Подходит для ПК и клиентов (Mihomo Party, Clash Verge Rev, Flclash). |
| [`template_remnawave.yaml`](template_remnawave.yaml) | Шаблон для панели [Remnawave](https://docs.rw) (**Subscription ➔ Templates**). |
| [`games.yaml`](games.yaml) | Список процессов популярных сетевых игр и лаунчеров (Steam, Epic, Riot, EFT, CS2, GTA RP, античиты). |
| [`ru-apps.yaml`](ru-apps.yaml) | Пакеты российских Android-приложений для прямого доступа. |
| [`torrent-clients.yaml`](torrent-clients.yaml) | Список процессов торрент-клиентов для исключения из проксирования. |

---

## ⚡ Модульная вставка (в существующий конфиг)

Если у вас уже настроен Mihomo (есть рабочие ноды или подписка) и вы хотите просто подключить умную маршрутизацию без раздувания конфига:

### 1. Добавьте `rule-providers`

```yaml
rule-providers:
  # Системные и RU-исключения
  private-domains:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/private.mrs
    path: ./ruleset/geosite-private.mrs
    interval: 2592000

  category-ru:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/category-ru.mrs
    path: ./ruleset/category-ru.mrs
    interval: 86400

  whitelist:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/whitelist.mrs
    path: ./ruleset/whitelist.mrs
    interval: 86400

  direct-ips:
    type: http
    behavior: ipcidr
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/direct.mrs
    path: ./ruleset/direct-ips.mrs
    interval: 86400

  # Блокировка рекламы и телеметрии
  category-ads:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/category-ads.mrs
    path: ./ruleset/category-ads.mrs
    interval: 86400

  win-spy:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/win-spy.mrs
    path: ./ruleset/win-spy.mrs
    interval: 86400

  # Торренты (домены и клиенты)
  torrent-domains:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/torrent.mrs
    path: ./ruleset/torrent-domains.mrs
    interval: 86400

  torrent-clients:
    type: http
    behavior: classical
    format: yaml
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/torrent-clients.yaml
    path: ./ruleset/torrent-clients.yaml
    interval: 86400

  # Сервисы через Прокси
  youtube:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/youtube.mrs
    path: ./ruleset/youtube.mrs
    interval: 86400

  discord:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/discord.mrs
    path: ./ruleset/discord.mrs
    interval: 86400

  discord-ip:
    type: http
    behavior: ipcidr
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/discord-ip.mrs
    path: ./ruleset/discord-ip.mrs
    interval: 86400

  telegram:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/telegram.mrs
    path: ./ruleset/telegram.mrs
    interval: 86400

  telegram-ip:
    type: http
    behavior: ipcidr
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/telegram-ip.mrs
    path: ./ruleset/telegram-ip.mrs
    interval: 86400

  ai:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/ai.mrs
    path: ./ruleset/ai.mrs
    interval: 86400

  category-geoblock-ru:
    type: http
    behavior: domain
    format: mrs
    url: https://cdn.jsdelivr.net/gh/mvrvntn/routing@release/mihomo/category-geoblock-ru.mrs
    path: ./ruleset/category-geoblock-ru.mrs
    interval: 86400
```

### 2. Замените секцию `rules`

*(Замените `PROXY` на название вашей прокси-группы)*:

```yaml
rules:
  # Приватные адреса и локальные сети — напрямую
  - RULE-SET,private-domains,DIRECT
  - IP-CIDR,10.0.0.0/8,DIRECT,no-resolve
  - IP-CIDR,172.16.0.0/12,DIRECT,no-resolve
  - IP-CIDR,192.168.0.0/16,DIRECT,no-resolve
  - IP-CIDR,127.0.0.0/8,DIRECT,no-resolve
  - IP-CIDR,::/0,REJECT-DROP,no-resolve

  # Дроп QUIC (UDP 443) — ускорение YouTube и устранение буферизации
  - AND,((NETWORK,UDP),(DST-PORT,443)),REJECT-DROP

  # Блокировка рекламы и телеметрии
  - RULE-SET,category-ads,REJECT-DROP
  - RULE-SET,win-spy,REJECT-DROP

  # Торренты — напрямую
  - RULE-SET,torrent-domains,DIRECT
  - RULE-SET,torrent-clients,DIRECT

  # Проксируемые сервисы
  - RULE-SET,youtube,PROXY
  - RULE-SET,discord,PROXY
  - RULE-SET,discord-ip,PROXY,no-resolve
  - RULE-SET,telegram,PROXY
  - RULE-SET,telegram-ip,PROXY,no-resolve
  - RULE-SET,ai,PROXY
  - RULE-SET,category-geoblock-ru,PROXY

  # Прямой доступ (РФ домены, Белый список и чистые RU IP без Антифильтра)
  - RULE-SET,category-ru,DIRECT
  - RULE-SET,whitelist,DIRECT
  - RULE-SET,direct-ips,DIRECT

  # Всё остальное зарубежное — в прокси
  - MATCH,PROXY
```

---

## 🛠 Особенности работы с базами

* **Антифильтр без зависаний:** База `direct.mrs` формируется каждую ночь. Из пула российских провайдеров автоматически исключаются все заблокированные IP-адреса из списков Антифильтра и Re-filter. В результате нет необходимости загружать 200 000+ сырых IP в память роутера.
* **DNS Bootstrap:** В параметрах `default-nameserver` и `proxy-server-nameserver` используются прямые IP (`77.88.8.8`, `8.8.8.8`), что предотвращает цикл резолва (дедлок) до установки защищенного соединения.
* **Nameserver Policy:** Домены `.ru`, `.рф` и сервисы Белого списка резолвятся напрямую через Яндекс.DNS (`77.88.8.8`) без лишних капч и проверок.

---

## 🤝 Благодарности и поддержка

# Разработка: ristavor
# Благодарности: hydraponique & fatyzzz
# Группа RoscomVPN в Telegram: https://t.me/vpnrouting
#
# Будем благодарны любой поддержке:
# USDT TRC20 — TMu3N2ZjK5omJ7n3WAj5MNCSM5querBXsR

*Проект «коридор»: [https://mvrvntn.github.io/koridor/](https://mvrvntn.github.io/koridor/)*
