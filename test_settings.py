"""
Тестовый скрипт для проверки окна настроек отдельно.
"""

import sys
from PyQt5.QtWidgets import QApplication

# Добавить путь к исходникам
sys.path.insert(0, 'src')

from settings_window import SettingsWindow

def main():
    app = QApplication(sys.argv)
    
    # Тестовая конфигурация
    test_config = {
        'hotkey': 'f9',
        'language': 'ru',
        'whisper_model': 'base'
    }
    
    print("Создание окна настроек...")
    window = SettingsWindow(test_config)
    
    print("Показ окна...")
    window.show()
    
    print("Окно настроек открыто!")
    print("Закройте окно чтобы выйти.")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

