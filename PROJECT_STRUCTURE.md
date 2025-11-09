# Структура проекта Votobu

## Обзор архитектуры

Votobu - модульное приложение на Python с четким разделением ответственности между компонентами.

## Структура файлов

```
Votobu/
│
├── src/                          # Исходный код приложения
│   ├── __init__.py              # Инициализация пакета
│   ├── main.py                  # Точка входа, координация компонентов
│   ├── config_manager.py        # Управление конфигурацией (JSON)
│   ├── audio_recorder.py        # Запись аудио (sounddevice)
│   ├── speech_recognizer.py     # Распознавание речи (Whisper)
│   ├── hotkey_manager.py        # Глобальные горячие клавиши (pynput)
│   ├── settings_window.py       # Окно настроек (PyQt5)
│   └── tray_app.py              # Системный трей (PyQt5)
│
├── assets/                       # Ресурсы приложения
│   ├── icon.png                 # Основная иконка (синий микрофон)
│   └── icon_recording.png       # Иконка записи (красный микрофон)
│
├── config/                       # Конфигурационные файлы
│   └── default_config.json      # Конфигурация по умолчанию
│
├── requirements.txt              # Python зависимости
├── .gitignore                   # Git исключения
│
├── create_icons.py              # Скрипт создания иконок
├── install.bat                  # Автоматическая установка (Windows)
├── run.bat                      # Запуск приложения (Windows)
│
├── README.md                    # Основная документация
├── INSTALL.md                   # Инструкция по установке
├── USAGE.md                     # Руководство пользователя
└── PROJECT_STRUCTURE.md         # Этот файл
```

## Компоненты приложения

### 1. main.py - Главный координатор

**Класс:** `VotobuApp`

**Ответственность:**
- Инициализация всех компонентов
- Связывание событий между модулями
- Управление жизненным циклом приложения

**Поток данных:**
```
HotkeyManager → AudioRecorder → SpeechRecognizer → Clipboard → User
                     ↓                  ↓
                TrayApp (UI feedback)
```

### 2. config_manager.py - Управление настройками

**Класс:** `ConfigManager`

**Возможности:**
- Загрузка/сохранение настроек в JSON
- Хранение в %APPDATA%/Votobu/config.json
- Значения по умолчанию
- Валидация конфигурации

**Настройки:**
- `hotkey`: горячая клавиша (по умолчанию: "f9")
- `language`: язык распознавания (по умолчанию: "ru")
- `whisper_model`: модель Whisper (по умолчанию: "base")
- `sample_rate`: частота дискретизации (16000 Hz)
- `channels`: каналы аудио (1 - моно)

### 3. audio_recorder.py - Запись аудио

**Класс:** `AudioRecorder`

**Технологии:**
- `sounddevice`: захват аудио с микрофона
- `soundfile`: сохранение в WAV формат
- `numpy`: обработка аудио массивов

**Процесс:**
1. `start()` - начало записи, создание потока
2. Накопление аудио данных в буфере
3. `stop()` - остановка, объединение чанков
4. Сохранение во временный WAV файл (16kHz mono)
5. `cleanup()` - удаление временных файлов

### 4. speech_recognizer.py - Распознавание речи

**Класс:** `SpeechRecognizer`

**Технологии:**
- `openai-whisper`: модель распознавания речи

**Возможности:**
- Загрузка моделей: tiny, base, small, medium, large
- Поддержка языков: ru, en, auto
- Синхронное и асинхронное распознавание
- Автоматическое определение языка

**Процесс:**
1. Загрузка модели (первый раз требует интернет)
2. Транскрибация аудио файла
3. Возврат текста

### 5. hotkey_manager.py - Горячие клавиши

**Класс:** `HotkeyManager`

**Технологии:**
- `pynput`: глобальный перехват клавиатуры

**Возможности:**
- Глобальные горячие клавиши (работают во всех приложениях)
- Поддержка F1-F12, букв, цифр, специальных клавиш
- События: on_press, on_release
- Динамическое изменение клавиши

**Маппинг клавиш:**
```python
KEY_MAPPING = {
    'f1'-'f12': Function keys,
    'ctrl', 'shift', 'alt': Modifiers,
    'space', 'enter', 'tab', 'esc': Special keys,
    'a'-'z', '0'-'9': Alphanumeric
}
```

### 6. settings_window.py - Окно настроек

**Класс:** `SettingsWindow`

**Технологии:**
- `PyQt5`: GUI фреймворк

**Компоненты:**
- Выбор горячей клавиши (перехват нажатия)
- Выбор языка (русский/английский/авто)
- Выбор модели Whisper (dropdown)
- Кнопки Сохранить/Отмена

**Сигналы:**
- `settings_saved`: emit при сохранении настроек

### 7. tray_app.py - Системный трей

**Класс:** `TrayApp`

**Технологии:**
- `PyQt5.QtWidgets.QSystemTrayIcon`

**Функционал:**
- Иконка в системном трее
- Контекстное меню:
  - Статус (текущее состояние)
  - Настройки
  - О программе
  - Выход
- Динамическое изменение иконки (обычная/запись)
- Уведомления (notifications)

**Состояния:**
- Готов к записи (синяя иконка)
- Запись (красная иконка)
- Распознавание (статус текст)

## Поток работы приложения

### Инициализация (startup)

```
1. QApplication создается
2. ConfigManager загружает настройки
3. AudioRecorder инициализируется
4. SpeechRecognizer загружает модель Whisper
5. HotkeyManager начинает перехват клавиш
6. TrayApp показывает иконку в трее
7. Уведомление "Votobu запущен"
```

### Цикл записи/распознавания

```
[Пользователь зажимает F9]
    ↓
HotkeyManager.on_press()
    ↓
AudioRecorder.start()
    ↓
TrayApp.set_recording_state(True) → Красная иконка
    ↓
[Пользователь говорит в микрофон]
    ↓
AudioRecorder накапливает аудио в буфере
    ↓
[Пользователь отпускает F9]
    ↓
HotkeyManager.on_release()
    ↓
AudioRecorder.stop() → возвращает путь к WAV файлу
    ↓
TrayApp.set_recognizing_state() → "Распознавание..."
    ↓
SpeechRecognizer.recognize_async(wav_file)
    ↓
Whisper транскрибирует аудио
    ↓
Текст возвращается через callback
    ↓
pyperclip.copy(text) → Буфер обмена
    ↓
AudioRecorder.cleanup() → Удаление временного файла
    ↓
TrayApp.show_notification("Текст распознан")
    ↓
TrayApp.set_recording_state(False) → Синяя иконка
```

### Изменение настроек

```
[ПКМ на иконке → Настройки]
    ↓
SettingsWindow.show()
    ↓
[Пользователь изменяет настройки]
    ↓
[Нажимает "Сохранить"]
    ↓
SettingsWindow.settings_saved.emit(new_config)
    ↓
VotobuApp._on_settings_saved(new_config)
    ↓
ConfigManager.save_config(new_config)
    ↓
Обновление компонентов:
    - HotkeyManager.change_hotkey()
    - SpeechRecognizer.change_language()
    - SpeechRecognizer.change_model()
```

## Зависимости

### Основные библиотеки

```python
PyQt5           # GUI и системный трей
openai-whisper  # AI распознавание речи
sounddevice     # Захват аудио с микрофона
soundfile       # Сохранение аудио файлов
pynput          # Глобальные горячие клавиши
pyperclip       # Буфер обмена
numpy           # Обработка аудио данных
Pillow          # Создание иконок
```

### Граф зависимостей

```
main.py
├── config_manager.py
├── audio_recorder.py
│   ├── sounddevice
│   ├── soundfile
│   └── numpy
├── speech_recognizer.py
│   └── whisper
├── hotkey_manager.py
│   └── pynput
├── settings_window.py
│   └── PyQt5
└── tray_app.py
    └── PyQt5
```

## Хранение данных

### Конфигурация

**Путь:** `%APPDATA%\Votobu\config.json` (Windows)

**Формат:**
```json
{
  "hotkey": "f9",
  "language": "ru",
  "whisper_model": "base",
  "sample_rate": 16000,
  "channels": 1
}
```

### Временные файлы

**Аудио записи:**
- Путь: системная временная папка
- Формат: `votobu_XXXXXX.wav`
- Очистка: автоматическая после распознавания

### Модели Whisper

**Путь:** `~/.cache/whisper/` (по умолчанию)

**Размеры:**
- tiny: ~75 MB
- base: ~150 MB
- small: ~500 MB
- medium: ~1.5 GB
- large: ~3 GB

## Потоки и асинхронность

### Потоки выполнения

1. **Main Thread (PyQt)**
   - GUI события
   - Системный трей
   - Окно настроек

2. **Hotkey Listener Thread (pynput)**
   - Глобальный перехват клавиш
   - Запускается автоматически pynput

3. **Audio Recording Thread (sounddevice)**
   - Захват аудио с микрофона
   - Callback функция для данных

4. **Recognition Thread**
   - Асинхронное распознавание
   - Создается для каждой транскрибации

### Синхронизация

- **Callbacks** используются для связи между потоками
- **pyqtSignal** для GUI обновлений
- **Threading-safe** операции с файлами

## Расширяемость

### Добавление новых языков

```python
# В settings_window.py
self.language_combo.addItems(["Русский", "Английский", "Немецкий", ...])

# Маппинг
lang_map = {0: 'ru', 1: 'en', 2: 'de', ...}
```

### Добавление новых форматов аудио

```python
# В audio_recorder.py
sf.write(temp_file.name, audio_array, self.sample_rate, 
         format='FLAC',  # Вместо WAV
         subtype='PCM_16')
```

### Добавление кнопок мыши как hotkey

```python
# В hotkey_manager.py
from pynput.mouse import Listener as MouseListener

# Добавить mouse listener параллельно keyboard listener
```

## Тестирование

### Ручное тестирование

1. **Запись аудио:**
   - Зажать клавишу → проверить красную иконку
   - Говорить → проверить захват звука
   - Отпустить → проверить остановку

2. **Распознавание:**
   - Короткие фразы (5 сек)
   - Длинные фразы (30 сек)
   - Разные языки

3. **Настройки:**
   - Изменить клавишу → проверить работу
   - Изменить язык → проверить качество
   - Изменить модель → проверить скорость

### Автоматическое тестирование

```python
# Пример unit теста для ConfigManager
def test_config_manager():
    cm = ConfigManager()
    assert cm.get('hotkey') == 'f9'
    cm.set('hotkey', 'f8')
    assert cm.get('hotkey') == 'f8'
```

## Производительность

### Узкие места

1. **Загрузка модели Whisper** (~5-30 сек при первом запуске)
2. **Транскрибация** (~0.5-2x реального времени аудио)
3. **Инициализация audio stream** (~1-2 сек)

### Оптимизации

- Модель загружается асинхронно при старте
- Аудио стрим остается открытым
- Временные файлы минимальны (только WAV)

## Известные ограничения

1. **Pynput:** может требовать права администратора на некоторых системах
2. **Whisper:** требует CPU/GPU ресурсов для распознавания
3. **PyQt5:** окно настроек может мигать при открытии
4. **Cross-platform:** полная поддержка только Windows

## Будущие улучшения

- [ ] GPU ускорение для Whisper
- [ ] Streaming распознавание (реальное время)
- [ ] История распознанных текстов
- [ ] Кастомные словари для специальных терминов
- [ ] Поддержка комбинаций клавиш (Ctrl+Shift+F9)
- [ ] Экспорт в разные форматы (TXT, DOCX, PDF)
- [ ] Интеграция с облачными сервисами
- [ ] Поддержка macOS и Linux

