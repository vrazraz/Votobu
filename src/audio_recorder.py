"""
Модуль для записи аудио с микрофона.
Использует sounddevice для захвата аудио.
"""

import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import threading
from pathlib import Path
from typing import Optional, Callable


class AudioRecorder:
    """Класс для записи аудио с микрофона."""
    
    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        """
        Инициализация рекордера.
        
        Args:
            sample_rate: Частота дискретизации (16kHz для Whisper)
            channels: Количество каналов (1 для моно)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_data = []
        self.stream = None
        self.temp_file = None
        
    def _audio_callback(self, indata, frames, time, status):
        """
        Callback функция для обработки аудио данных.
        
        Args:
            indata: Входящие аудио данные
            frames: Количество фреймов
            time: Временная информация
            status: Статус записи
        """
        if status:
            print(f"Статус записи: {status}")
        if self.recording:
            self.audio_data.append(indata.copy())
    
    def start(self) -> bool:
        """
        Начать запись аудио.
        
        Returns:
            True если запись началась успешно
        """
        if self.recording:
            return False
        
        try:
            self.audio_data = []
            self.recording = True
            
            # Создать поток для записи
            self.stream = sd.InputStream(
                callback=self._audio_callback,
                channels=self.channels,
                samplerate=self.sample_rate,
                dtype=np.float32
            )
            self.stream.start()
            print("Запись началась...")
            return True
        except Exception as e:
            print(f"Ошибка начала записи: {e}")
            self.recording = False
            return False
    
    def stop(self) -> Optional[str]:
        """
        Остановить запись и сохранить в временный файл.
        
        Returns:
            Путь к сохраненному аудио файлу или None в случае ошибки
        """
        if not self.recording:
            return None
        
        try:
            self.recording = False
            
            if self.stream:
                self.stream.stop()
                self.stream.close()
                self.stream = None
            
            if not self.audio_data:
                print("Нет данных для сохранения")
                return None
            
            # Объединить все чанки аудио
            audio_array = np.concatenate(self.audio_data, axis=0)
            
            # Создать временный файл
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix='.wav',
                prefix='votobu_'
            )
            temp_file.close()
            
            # Сохранить в WAV формат
            sf.write(
                temp_file.name,
                audio_array,
                self.sample_rate,
                format='WAV',
                subtype='PCM_16'
            )
            
            self.temp_file = temp_file.name
            print(f"Запись сохранена: {self.temp_file}")
            return self.temp_file
            
        except Exception as e:
            print(f"Ошибка остановки записи: {e}")
            return None
    
    def is_recording(self) -> bool:
        """
        Проверить, идет ли запись.
        
        Returns:
            True если запись активна
        """
        return self.recording
    
    def cleanup(self) -> None:
        """Очистить временные файлы."""
        if self.temp_file and Path(self.temp_file).exists():
            try:
                Path(self.temp_file).unlink()
                print(f"Временный файл удален: {self.temp_file}")
            except Exception as e:
                print(f"Ошибка удаления временного файла: {e}")
            finally:
                self.temp_file = None

