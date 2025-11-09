"""
Менеджер конфигурации приложения.
Загружает и сохраняет настройки в JSON файл.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class ConfigManager:
    """Управление конфигурацией приложения."""
    
    DEFAULT_CONFIG = {
        "hotkey": "f9",
        "language": "ru",
        "whisper_model": "base",
        "sample_rate": 16000,
        "channels": 1
    }
    
    def __init__(self):
        """Инициализация менеджера конфигурации."""
        self.config_dir = self._get_config_dir()
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
    
    def _get_config_dir(self) -> Path:
        """Получить директорию для хранения конфигурации."""
        if os.name == 'nt':  # Windows
            appdata = os.getenv('APPDATA')
            config_dir = Path(appdata) / "Votobu"
        else:  # Linux/Mac
            config_dir = Path.home() / ".config" / "votobu"
        
        # Создать директорию если не существует
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    def _load_config(self) -> Dict[str, Any]:
        """Загрузить конфигурацию из файла или создать новую."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Дополнить недостающие ключи из дефолтной конфигурации
                    for key, value in self.DEFAULT_CONFIG.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                print(f"Ошибка загрузки конфигурации: {e}")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Создать новый конфиг с дефолтными значениями
            self.save_config(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Получить значение настройки.
        
        Args:
            key: Ключ настройки
            default: Значение по умолчанию если ключ не найден
            
        Returns:
            Значение настройки
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Установить значение настройки.
        
        Args:
            key: Ключ настройки
            value: Новое значение
        """
        self.config[key] = value
    
    def save_config(self, config: Dict[str, Any] = None) -> bool:
        """
        Сохранить конфигурацию в файл.
        
        Args:
            config: Конфигурация для сохранения (если None, сохраняется текущая)
            
        Returns:
            True если успешно, False в случае ошибки
        """
        if config is not None:
            self.config = config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Ошибка сохранения конфигурации: {e}")
            return False
    
    def reset_to_defaults(self) -> None:
        """Сбросить настройки к дефолтным значениям."""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save_config()

