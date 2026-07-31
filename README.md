# Automatically Restores Microphone Volume


Держит громкость микрофона на 100% (Windows). Скрипт запускается в фоне (pythonw), проверяет уровень каждые 10 секунд и поднимает его до максимума, если он снизился.

## Возможности

- Автоматически возвращает громкость микрофона на 100%
- Фоновый запуск без окна (pythonw)
- Логирование в `logs/mic_volume.log`
- Watchdog (`watchdog.bat`) следит за процессом и перезапускает его при падении

## Требования

- Windows 10/11
- Python 3.8+ (с `pythonw.exe`, доступным через PATH)

## Установка

1) Перейдите на страницу релизов и скачайте последнюю версию или по ссылке и скачайте [последнюю версию](https://github.com/IvanChaev/automatically-restores-microphone-volume/archive/refs/tags/v1.0.0.zip)
2) Распакуйте в удобную папку
3) Запустите батник watchdog.bat



## Запуск

1. `watchdog.bat` — основной запуск (watchdog + скрипт микрофона). Окно можно свернуть, оно останется работать.
2. `mic_100.bat` — запуск только скрипта микрофона (без watchdog).
3. `stop_all.bat` — остановить и скрипт, и watchdog.

## Структура

```
main.py          — основной скрипт
mic_100.bat      — запуск скрипта
watchdog.bat     — watchdog с автоперезапуском
stop_all.bat     — остановка всего
requirements.txt — зависимости
```

## Логи и файлы состояния

Создаются в папке `logs/`:

- `mic_volume.log` — события изменения громкости
- `watchdog.log` — события watchdog
- `pid.pid` — pid запущенного скрипта
- `raised.flag` / `restart.flag` — служебные флаги

## Лицензия

MIT
