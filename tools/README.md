# 🛠️ Community Routing Tools

Python-утилиты для генерации клиентских конфигураций и QR-кодов для различных VPN-клиентов (iOS / Android / Desktop) на основе конфигураций роутинга (`HAPP/DEFAULT.JSON`, `RELOCANT/HAPP.JSON` и др.).

Утилиты по умолчанию работают автономно с локальными файлами репозитория либо загружают актуальные правила по сети.

## 📁 Структура

```
tools/
├── streisand/
│   └── generate_streisand_link.py      # Генерация ссылки streisand:// для iOS
├── v2rayNG/
│   ├── generate_v2rayng_routing_qr.py  # Генерация QR и JSON для правил v2RayNG (Android)
│   └── generate_geoasset_qr.py         # QR-коды для обновления geoip.dat и geosite.dat
├── singbox/
│   └── generate_singbox_rules.py       # Генерация rules JSON для sing-box (Throne / NekoRay v4+)
└── README.md
```

## 📋 Требования

- Python 3.8+
- Стандартная библиотека Python (для генерации QR-изображений опционально `pip install qrcode[pil]`)

## 🚀 Использование

### Streisand (iOS)

Генерация глубокой ссылки `streisand://` для мгновенного импорта профиля маршрутизации:

```bash
python tools/streisand/generate_streisand_link.py
```

Для релокант-конфигурации:
```bash
python tools/streisand/generate_streisand_link.py -c RELOCANT/HAPP.JSON
```

> **Важно:** Перед применением обновите базы `geoip.dat` и `geosite.dat` в приложении Streisand (Настройки → Маршрутизация → Ресурсы).

---

### v2RayNG (Android)

**Генерация правил маршрутизации (QR-код и JSON для буфера обмена):**

```bash
python tools/v2rayNG/generate_v2rayng_routing_qr.py
```

> **Важно:** В настройках v2RayNG установите **Стратегию доменов** (Domain Strategy) в значение `IPIfNonMatch`.

**QR-коды для загрузки гео-баз (Geoasset update):**

```bash
# Использование CDN jsdelivr (по умолчанию)
python tools/v2rayNG/generate_geoasset_qr.py

# Использование прямых ссылок GitHub Releases
python tools/v2rayNG/generate_geoasset_qr.py --source releases
```

---

### sing-box (Throne / NekoRay v4.0+)

Генерация правил маршрутизации с подключением скомпилированных `.srs` бинарных правил:

```bash
# Вывод в консоль
python tools/singbox/generate_singbox_rules.py

# Сохранение в файл
python tools/singbox/generate_singbox_rules.py -o singbox_rules.json
```

Импорт: **Настройки маршрутизации → Расширенные → Импорт JSON**.
