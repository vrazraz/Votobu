"""
Модуль для распознавания речи через OpenAI Whisper.
"""

import whisper
import threading
from typing import Optional, Callable
from pathlib import Path


class SpeechRecognizer:
    """Класс для распознавания речи с использованием Whisper."""
    
    def __init__(self, model_name: str = "base", language: str = "ru"):
        """
        Инициализация распознавателя речи.
        
        Args:
            model_name: Название модели Whisper (tiny/base/small/medium/large)
            language: Код языка (ru/en/auto)
        """
        self.model_name = model_name
        self.language = language if language != "auto" else None
        self.model = None
        self.loading = False
        self.recognizing = False
        
    def load_model(self) -> bool:
        """
        Загрузить модель Whisper.
        
        Returns:
            True если модель загружена успешно
        """
        if self.model is not None:
            return True
        
        if self.loading:
            return False
        
        try:
            self.loading = True
            print(f"Загрузка модели Whisper: {self.model_name}...")
            self.model = whisper.load_model(self.model_name)
            print("Модель загружена успешно")
            return True
        except Exception as e:
            print(f"Ошибка загрузки модели: {e}")
            return False
        finally:
            self.loading = False
    
    def recognize(self, audio_file: str) -> Optional[str]:
        """
        Распознать речь из аудио файла.
        
        Args:
            audio_file: Путь к аудио файлу
            
        Returns:
            Распознанный текст или None в случае ошибки
        """
        if not Path(audio_file).exists():
            print(f"Файл не найден: {audio_file}")
            return None
        
        # Загрузить модель если еще не загружена
        if self.model is None:
            if not self.load_model():
                return None
        
        try:
            self.recognizing = True
            print(f"Распознавание аудио: {audio_file}")
            
            # Опции для транскрибации
            options = {
                "fp16": False,  # Использовать float32 для совместимости
                "language": self.language,
                "task": "transcribe"
            }
            
            # Удалить language если None (автоопределение)
            if self.language is None:
                del options["language"]
            
            # Выполнить транскрибацию
            result = self.model.transcribe(audio_file, **options)
            
            # Извлечь текст
            text = result.get("text", "").strip()
            
            if text:
                print(f"Распознанный текст: {text}")
                return text
            else:
                print("Текст не распознан")
                return None
                
        except Exception as e:
            print(f"Ошибка распознавания: {e}")
            return None
        finally:
            self.recognizing = False
    
    def recognize_async(self, audio_file: str, callback: Callable[[Optional[str]], None]) -> None:
        """
        Распознать речь асинхронно.
        
        Args:
            audio_file: Путь к аудио файлу
            callback: Функция обратного вызова с результатом
        """
        def worker():
            result = self.recognize(audio_file)
            callback(result)
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def is_recognizing(self) -> bool:
        """
        Проверить, идет ли распознавание.
        
        Returns:
            True если распознавание активно
        """
        return self.recognizing
    
    def change_model(self, model_name: str) -> bool:
        """
        Изменить модель Whisper.
        
        Args:
            model_name: Название новой модели
            
        Returns:
            True если модель изменена успешно
        """
        if self.recognizing or self.loading:
            return False
        
        self.model_name = model_name
        self.model = None
        return self.load_model()
    
    def change_language(self, language: str) -> None:
        """
        Изменить язык распознавания.
        
        Args:
            language: Код языка (ru/en/auto)
        """
        self.language = language if language != "auto" else None

