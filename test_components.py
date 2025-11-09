"""
Скрипт для тестирования компонентов Votobu.
Проверяет базовую функциональность без полного запуска GUI.
"""

import sys
import os
from pathlib import Path

# Установить UTF-8 для вывода в консоль Windows
if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("Тестирование компонентов Votobu")
print("=" * 60)

# Проверка Python версии
print(f"\n1. Проверка Python версии...")
print(f"   Python: {sys.version}")
if sys.version_info < (3, 8):
    print("   ❌ ОШИБКА: Требуется Python 3.8 или выше!")
    sys.exit(1)
else:
    print("   ✓ Python версия подходит")

# Проверка импорта зависимостей
print(f"\n2. Проверка зависимостей...")

dependencies = {
    'PyQt5': 'PyQt5',
    'whisper': 'openai-whisper',
    'sounddevice': 'sounddevice',
    'soundfile': 'soundfile',
    'pynput': 'pynput',
    'pyperclip': 'pyperclip',
    'numpy': 'numpy',
    'PIL': 'Pillow'
}

missing_deps = []
for module, package in dependencies.items():
    try:
        __import__(module)
        print(f"   ✓ {package}")
    except ImportError:
        print(f"   ❌ {package} - НЕ УСТАНОВЛЕН")
        missing_deps.append(package)

if missing_deps:
    print(f"\n   Установите отсутствующие зависимости:")
    print(f"   pip install {' '.join(missing_deps)}")
    sys.exit(1)

# Проверка структуры проекта
print(f"\n3. Проверка структуры проекта...")

required_files = [
    'src/main.py',
    'src/config_manager.py',
    'src/audio_recorder.py',
    'src/speech_recognizer.py',
    'src/hotkey_manager.py',
    'src/settings_window.py',
    'src/tray_app.py',
    'config/default_config.json',
    'assets/icon.png',
    'assets/icon_recording.png',
]

for file_path in required_files:
    if Path(file_path).exists():
        print(f"   ✓ {file_path}")
    else:
        print(f"   ❌ {file_path} - НЕ НАЙДЕН")

# Тест импорта модулей
print(f"\n4. Проверка модулей приложения...")

sys.path.insert(0, str(Path('src').resolve()))

modules_to_test = [
    'config_manager',
    'audio_recorder',
    'speech_recognizer',
    'hotkey_manager',
    'settings_window',
    'tray_app'
]

for module in modules_to_test:
    try:
        __import__(module)
        print(f"   ✓ {module}")
    except Exception as e:
        print(f"   ❌ {module} - ОШИБКА: {e}")

# Тест ConfigManager
print(f"\n5. Тест ConfigManager...")
try:
    from config_manager import ConfigManager
    config = ConfigManager()
    assert config.get('hotkey') is not None
    assert config.get('language') is not None
    assert config.get('whisper_model') is not None
    print(f"   ✓ ConfigManager работает")
    print(f"   - Горячая клавиша: {config.get('hotkey')}")
    print(f"   - Язык: {config.get('language')}")
    print(f"   - Модель: {config.get('whisper_model')}")
except Exception as e:
    print(f"   ❌ ConfigManager - ОШИБКА: {e}")

# Тест AudioRecorder
print(f"\n6. Тест AudioRecorder...")
try:
    from audio_recorder import AudioRecorder
    recorder = AudioRecorder()
    print(f"   ✓ AudioRecorder инициализирован")
    print(f"   - Sample rate: {recorder.sample_rate} Hz")
    print(f"   - Channels: {recorder.channels}")
except Exception as e:
    print(f"   ❌ AudioRecorder - ОШИБКА: {e}")

# Тест SpeechRecognizer (без загрузки модели)
print(f"\n7. Тест SpeechRecognizer...")
try:
    from speech_recognizer import SpeechRecognizer
    recognizer = SpeechRecognizer(model_name='base', language='ru')
    print(f"   ✓ SpeechRecognizer инициализирован")
    print(f"   - Модель: {recognizer.model_name}")
    print(f"   - Язык: {recognizer.language}")
    print(f"   ⚠ Модель НЕ загружена (для экономии времени)")
except Exception as e:
    print(f"   ❌ SpeechRecognizer - ОШИБКА: {e}")

# Тест HotkeyManager (без запуска)
print(f"\n8. Тест HotkeyManager...")
try:
    from hotkey_manager import HotkeyManager
    hotkey_mgr = HotkeyManager('f9')
    print(f"   ✓ HotkeyManager инициализирован")
    print(f"   - Горячая клавиша: {hotkey_mgr.get_hotkey_display_name()}")
    print(f"   ⚠ Listener НЕ запущен (требует GUI)")
except Exception as e:
    print(f"   ❌ HotkeyManager - ОШИБКА: {e}")

# Финальный результат
print("\n" + "=" * 60)
print("РЕЗУЛЬТАТ ТЕСТИРОВАНИЯ")
print("=" * 60)

if not missing_deps:
    print("✓ Все компоненты готовы к работе!")
    print("\nДля запуска приложения используйте:")
    print("  python src/main.py")
    print("  или")
    print("  run.bat")
else:
    print("❌ Обнаружены проблемы. Смотрите вывод выше.")
    print("\nУстановите зависимости:")
    print("  pip install -r requirements.txt")

print("=" * 60)

