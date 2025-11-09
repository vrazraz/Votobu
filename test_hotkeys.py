"""
Тестовый скрипт для проверки горячих клавиш и кнопок мыши.
Запустите этот скрипт и попробуйте нажать разные клавиши и кнопки мыши.
"""

import sys
from pathlib import Path

# Добавить src в путь
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from hotkey_manager import HotkeyManager


def test_hotkeys():
    """Тестирование различных горячих клавиш."""
    
    print("=" * 50)
    print("  Тест горячих клавиш и кнопок мыши")
    print("=" * 50)
    print()
    
    test_keys = [
        'f9',           # Функциональная клавиша
        'a',            # Буква
        'space',        # Пробел
        'mouse_x1',     # Боковая кнопка мыши (назад)
        'mouse_x2',     # Боковая кнопка мыши (вперед)
        'mouse_middle', # Средняя кнопка мыши
    ]
    
    for key in test_keys:
        print(f"\n>>> Тестирование: {key.upper()}")
        print(f"Нажмите {key.upper()} для проверки (Ctrl+C для выхода)")
        
        manager = HotkeyManager(key)
        
        def on_press():
            print(f"  ✅ {key.upper()} нажата!")
        
        def on_release():
            print(f"  ⬆️  {key.upper()} отпущена!")
        
        manager.set_on_press(on_press)
        manager.set_on_release(on_release)
        
        try:
            manager.start()
            
            # Ждать нажатия
            import time
            time.sleep(5)
            
            manager.stop()
            print(f"  ✓ Тест {key.upper()} завершен\n")
            
        except KeyboardInterrupt:
            manager.stop()
            print("\n\nТестирование прервано.")
            break


if __name__ == "__main__":
    try:
        test_hotkeys()
    except KeyboardInterrupt:
        print("\n\nВыход...")

