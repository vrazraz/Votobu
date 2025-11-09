"""
Приложение системного трея.
Управляет иконкой в трее и главным меню.
"""

from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, pyqtSignal
from pathlib import Path
from typing import Optional


class TrayApp(QObject):
    """Класс приложения системного трея."""
    
    # Сигналы
    settings_requested = pyqtSignal()
    quit_requested = pyqtSignal()
    
    def __init__(self, icon_path: str = None, recording_icon_path: str = None):
        """
        Инициализация приложения трея.
        
        Args:
            icon_path: Путь к основной иконке
            recording_icon_path: Путь к иконке записи
        """
        super().__init__()
        
        # Иконки
        self.icon_path = icon_path
        self.recording_icon_path = recording_icon_path
        
        # Создать иконку трея
        self.tray_icon = None
        self.menu = None
        self.is_recording = False
        
        self._init_tray()
    
    def _init_tray(self) -> None:
        """Инициализировать системный трей."""
        # Создать иконку
        icon = self._load_icon(self.icon_path)
        self.tray_icon = QSystemTrayIcon(icon)
        
        # Создать меню
        self.menu = QMenu()
        
        # Добавить пункты меню
        self.status_action = QAction("Готов к записи", self.menu)
        self.status_action.setEnabled(False)
        self.menu.addAction(self.status_action)
        
        self.menu.addSeparator()
        
        # Настройки
        settings_action = QAction("Настройки", self.menu)
        settings_action.triggered.connect(self._on_settings)
        self.menu.addAction(settings_action)
        
        # О программе
        about_action = QAction("О программе", self.menu)
        about_action.triggered.connect(self._on_about)
        self.menu.addAction(about_action)
        
        self.menu.addSeparator()
        
        # Выход
        quit_action = QAction("Выход", self.menu)
        quit_action.triggered.connect(self._on_quit)
        self.menu.addAction(quit_action)
        
        # Установить меню
        self.tray_icon.setContextMenu(self.menu)
        
        # Показать иконку
        self.tray_icon.show()
        
        # Показать приветственное уведомление
        self.show_notification(
            "Votobu запущен",
            "Зажмите горячую клавишу для начала записи",
            QSystemTrayIcon.Information
        )
    
    def _load_icon(self, icon_path: Optional[str]) -> QIcon:
        """
        Загрузить иконку из файла.
        
        Args:
            icon_path: Путь к файлу иконки
            
        Returns:
            QIcon объект
        """
        if icon_path and Path(icon_path).exists():
            return QIcon(icon_path)
        else:
            # Вернуть пустую иконку если файл не найден
            return QIcon()
    
    def _on_settings(self) -> None:
        """Обработчик нажатия пункта Настройки."""
        self.settings_requested.emit()
    
    def _on_about(self) -> None:
        """Обработчик нажатия пункта О программе."""
        QMessageBox.about(
            None,
            "О программе Votobu",
            "<h2>Votobu</h2>"
            "<p>Приложение для преобразования голоса в текст</p>"
            "<p><b>Версия:</b> 1.0.0</p>"
            "<p><b>Технологии:</b></p>"
            "<ul>"
            "<li>PyQt5 - интерфейс</li>"
            "<li>OpenAI Whisper - распознавание речи</li>"
            "<li>sounddevice - запись аудио</li>"
            "<li>pynput - горячие клавиши</li>"
            "</ul>"
            "<p><b>Использование:</b></p>"
            "<p>Зажмите горячую клавишу (по умолчанию F9), говорите, "
            "отпустите клавишу. Текст будет скопирован в буфер обмена.</p>"
        )
    
    def _on_quit(self) -> None:
        """Обработчик нажатия пункта Выход."""
        self.quit_requested.emit()
    
    def set_recording_state(self, is_recording: bool) -> None:
        """
        Установить состояние записи.
        
        Args:
            is_recording: True если идет запись
        """
        self.is_recording = is_recording
        
        if is_recording:
            # Изменить иконку на запись
            if self.recording_icon_path:
                icon = self._load_icon(self.recording_icon_path)
                self.tray_icon.setIcon(icon)
            
            # Обновить статус
            self.status_action.setText("🔴 Запись...")
        else:
            # Вернуть обычную иконку
            if self.icon_path:
                icon = self._load_icon(self.icon_path)
                self.tray_icon.setIcon(icon)
            
            # Обновить статус
            self.status_action.setText("Готов к записи")
    
    def set_recognizing_state(self) -> None:
        """Установить состояние распознавания."""
        self.status_action.setText("🤖 Распознавание...")
    
    def show_notification(
        self, 
        title: str, 
        message: str, 
        icon_type: QSystemTrayIcon.MessageIcon = QSystemTrayIcon.Information
    ) -> None:
        """
        Показать уведомление в трее.
        
        Args:
            title: Заголовок уведомления
            message: Текст уведомления
            icon_type: Тип иконки уведомления
        """
        if self.tray_icon:
            self.tray_icon.showMessage(title, message, icon_type, 3000)
    
    def update_hotkey_display(self, hotkey: str) -> None:
        """
        Обновить отображение горячей клавиши в статусе.
        
        Args:
            hotkey: Название горячей клавиши
        """
        # Можно добавить в статус если нужно
        pass
    
    def hide(self) -> None:
        """Скрыть иконку трея."""
        if self.tray_icon:
            self.tray_icon.hide()
    
    def show(self) -> None:
        """Показать иконку трея."""
        if self.tray_icon:
            self.tray_icon.show()

