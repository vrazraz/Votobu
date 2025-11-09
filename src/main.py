"""
Главный модуль приложения Votobu.
Точка входа и координация всех компонентов.
"""

import sys
import os
from pathlib import Path

# Исправление проблемы с Qt platform plugin на Windows
if sys.platform == 'win32':
    # Найти путь к PyQt5
    import site
    for site_dir in site.getsitepackages():
        qt_plugin_path = Path(site_dir) / 'PyQt5' / 'Qt5' / 'plugins'
        if qt_plugin_path.exists():
            os.environ['QT_PLUGIN_PATH'] = str(qt_plugin_path)
            break
    
    # Альтернативный путь
    if 'QT_PLUGIN_PATH' not in os.environ:
        pyqt5_path = Path(sys.executable).parent / 'Lib' / 'site-packages' / 'PyQt5' / 'Qt5' / 'plugins'
        if pyqt5_path.exists():
            os.environ['QT_PLUGIN_PATH'] = str(pyqt5_path)

import pyperclip
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal

# Добавить ffmpeg в PATH для Whisper
try:
    import imageio_ffmpeg
    import shutil
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = Path(ffmpeg_exe).parent
    
    # Создать копию с правильным именем если нужно
    ffmpeg_standard = ffmpeg_dir / "ffmpeg.exe"
    if not ffmpeg_standard.exists() and Path(ffmpeg_exe).exists():
        try:
            shutil.copy2(ffmpeg_exe, ffmpeg_standard)
            print(f"ffmpeg скопирован: {ffmpeg_standard}")
        except Exception as copy_error:
            print(f"Не удалось скопировать ffmpeg: {copy_error}")
    
    # Добавить в PATH
    os.environ['PATH'] = str(ffmpeg_dir) + os.pathsep + os.environ.get('PATH', '')
    print(f"ffmpeg добавлен в PATH: {ffmpeg_dir}")
    
except Exception as e:
    print(f"Предупреждение: не удалось настроить ffmpeg: {e}")

# Импорт модулей приложения
from config_manager import ConfigManager
from audio_recorder import AudioRecorder
from speech_recognizer import SpeechRecognizer
from hotkey_manager import HotkeyManager
from settings_window import SettingsWindow
from tray_app import TrayApp


class VotobuApp(QObject):
    """Главный класс приложения Votobu."""
    
    def __init__(self):
        """Инициализация приложения."""
        super().__init__()
        
        print("Запуск Votobu...")
        
        # Инициализация компонентов
        self.config_manager = ConfigManager()
        self.audio_recorder = None
        self.speech_recognizer = None
        self.hotkey_manager = None
        self.settings_window = None
        self.tray_app = None
        
        # Инициализация
        self._init_components()
        self._connect_signals()
        
        print("Votobu успешно запущен!")
    
    def _init_components(self) -> None:
        """Инициализировать все компоненты."""
        # Загрузить конфигурацию
        config = self.config_manager.config
        
        # Создать аудио рекордер
        self.audio_recorder = AudioRecorder(
            sample_rate=config.get('sample_rate', 16000),
            channels=config.get('channels', 1)
        )
        
        # Создать распознаватель речи
        self.speech_recognizer = SpeechRecognizer(
            model_name=config.get('whisper_model', 'base'),
            language=config.get('language', 'ru')
        )
        
        # Загрузить модель Whisper в фоне
        print("Загрузка модели Whisper...")
        self.speech_recognizer.load_model()
        
        # Создать менеджер горячих клавиш
        self.hotkey_manager = HotkeyManager(
            hotkey=config.get('hotkey', 'f9')
        )
        
        # Создать приложение трея
        icon_path = self._get_asset_path('icon.png')
        recording_icon_path = self._get_asset_path('icon_recording.png')
        
        self.tray_app = TrayApp(
            icon_path=icon_path,
            recording_icon_path=recording_icon_path
        )
    
    def _get_asset_path(self, filename: str) -> str:
        """
        Получить путь к файлу ресурса.
        
        Args:
            filename: Имя файла
            
        Returns:
            Полный путь к файлу
        """
        # Получить директорию проекта
        project_dir = Path(__file__).parent.parent
        assets_dir = project_dir / "assets"
        asset_path = assets_dir / filename
        
        return str(asset_path) if asset_path.exists() else None
    
    def _connect_signals(self) -> None:
        """Связать сигналы и слоты компонентов."""
        # Hotkey manager callbacks
        self.hotkey_manager.set_on_press(self._on_hotkey_press)
        self.hotkey_manager.set_on_release(self._on_hotkey_release)
        
        # Tray app signals
        self.tray_app.settings_requested.connect(self._on_settings_requested)
        self.tray_app.quit_requested.connect(self._on_quit_requested)
        
        # Запустить менеджер горячих клавиш
        self.hotkey_manager.start()
    
    def _on_hotkey_press(self) -> None:
        """Обработчик нажатия горячей клавиши."""
        print("\n=== Горячая клавиша нажата ===")
        
        # Начать запись
        if self.audio_recorder.start():
            self.tray_app.set_recording_state(True)
            print("Запись началась")
    
    def _on_hotkey_release(self) -> None:
        """Обработчик отпускания горячей клавиши."""
        print("=== Горячая клавиша отпущена ===")
        
        # Остановить запись
        audio_file = self.audio_recorder.stop()
        
        if audio_file:
            self.tray_app.set_recording_state(False)
            self.tray_app.set_recognizing_state()
            print(f"Запись остановлена: {audio_file}")
            
            # Распознать речь асинхронно
            self.speech_recognizer.recognize_async(
                audio_file,
                self._on_recognition_complete
            )
    
    def _on_recognition_complete(self, text: str) -> None:
        """
        Обработчик завершения распознавания.
        
        Args:
            text: Распознанный текст
        """
        print("=== Распознавание завершено ===")
        
        # Очистить временные файлы
        self.audio_recorder.cleanup()
        
        # Вернуть статус в готовность
        self.tray_app.set_recording_state(False)
        
        if text:
            # Скопировать в буфер обмена
            pyperclip.copy(text)
            print(f"Текст скопирован в буфер обмена: {text}")
            
            # Показать уведомление
            self.tray_app.show_notification(
                "Текст распознан",
                f"Скопировано в буфер обмена:\n{text[:100]}{'...' if len(text) > 100 else ''}"
            )
        else:
            print("Текст не распознан")
            self.tray_app.show_notification(
                "Ошибка",
                "Не удалось распознать речь. Попробуйте еще раз."
            )
    
    def _on_settings_requested(self) -> None:
        """Обработчик запроса открытия настроек."""
        if self.settings_window is None or not self.settings_window.isVisible():
            self.settings_window = SettingsWindow(self.config_manager.config)
            self.settings_window.settings_saved.connect(self._on_settings_saved)
        
        self.settings_window.show()
        self.settings_window.activateWindow()
    
    def _on_settings_saved(self, new_config: dict) -> None:
        """
        Обработчик сохранения настроек.
        
        Args:
            new_config: Новая конфигурация
        """
        print("Сохранение новых настроек...")
        
        # Сохранить конфигурацию
        self.config_manager.save_config(new_config)
        
        # Обновить компоненты
        # Горячая клавиша
        if new_config.get('hotkey') != self.config_manager.config.get('hotkey'):
            self.hotkey_manager.change_hotkey(new_config['hotkey'])
        
        # Язык распознавания
        if new_config.get('language') != self.config_manager.config.get('language'):
            self.speech_recognizer.change_language(new_config['language'])
        
        # Модель Whisper
        if new_config.get('whisper_model') != self.config_manager.config.get('whisper_model'):
            self.speech_recognizer.change_model(new_config['whisper_model'])
        
        print("Настройки применены")
    
    def _on_quit_requested(self) -> None:
        """Обработчик запроса выхода из приложения."""
        print("Выход из приложения...")
        
        # Остановить компоненты
        if self.hotkey_manager:
            self.hotkey_manager.stop()
        
        if self.audio_recorder and self.audio_recorder.is_recording():
            self.audio_recorder.stop()
            self.audio_recorder.cleanup()
        
        # Скрыть трей
        if self.tray_app:
            self.tray_app.hide()
        
        # Выйти из приложения
        QApplication.quit()


def main():
    """Точка входа приложения."""
    # Создать Qt приложение
    app = QApplication(sys.argv)
    
    # Установить название приложения
    app.setApplicationName("Votobu")
    app.setQuitOnLastWindowClosed(False)  # Не закрывать при закрытии окна
    
    # Создать главное приложение
    votobu = VotobuApp()
    
    # Запустить event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

