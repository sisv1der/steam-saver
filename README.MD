# Steam Saver

Steam Saver is a script that automatically backs up Steam Proton save files to a git repository.

## Features
- Extracts save data from Proton prefixes
- Supports Flatpak and native Steam installations
- Uses `rsync` for efficient copying
- Automatically commits and pushes changes to a Git repository

## Installation

```bash
git clone https://github.com/yourname/steam-saver.git
cd steam-saver
chmod +x steam-saver.py
```

## Usage

```bash
./steam-saver.py /path/to/target/directory
```

### Help
```bash
./steam-saver.py -h
```

## Systemd Integration (Example Timer and Service)

### `steam-saver.timer`
```ini
[Unit]
Description=Run steam-saver.service every 2 hours

[Timer]
OnUnitActiveSec=2h
Unit=steam-saver.service
Persistent=true

[Install]
WantedBy=multi-user.target
```

### `steam-saver.service`
```ini
[Unit]
Description=Steam saves exporter to git
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/steam-saver.py /path/to/target/directory
Restart=on-failure
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=timers.target
```

---

# Steam Saver (на русском)

Steam Saver — это скрипт для автоматического бэкапа Proton-сейвов Steam в git-репозиторий.

## Возможности
- Извлечение сейвов из Proton-префиксов
- Поддержка Flatpak и обычной установки Steam
- Эффективное копирование с помощью `rsync`
- Коммит и пуш изменений в репозиторий

## Установка
```bash
git clone https://github.com/yourname/steam-saver.git
cd steam-saver
chmod +x steam-saver.py
```

## Использование

```bash
./steam-saver.py /путь/до/директории/для/сейвов
```

### Помощь
```bash
./steam-saver.py -h
```

## Интеграция с systemd (Пример таймера и сервиса)

### `steam-saver.timer`
```ini
[Unit]
Description=Run steam-saver.service every 2 hours

[Timer]
OnUnitActiveSec=2h
Unit=steam-saver.service
Persistent=true

[Install]
WantedBy=multi-user.target
```

### `steam-saver.service`
```ini
[Unit]
Description=Экспорт сейвов Steam в git
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /путь/до/steam-saver.py /путь/до/папки/сейвов
Restart=on-failure
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=timers.target
```
