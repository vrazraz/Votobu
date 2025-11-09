"""
Окно настроек приложения.
Использует PyQt5 для создания GUI.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from typing import Dict, Any, Optional


class SettingsWindow(QWidget):
    """Окно настроек приложения."""
    
    # Сигнал для уведомления о сохранении настроек
    settings_saved = pyqtSignal(dict)
    
    def __init__(self, config: Dict[str, Any]):
        """
        Инициализация окна настроек.
        
        Args:
            config: Текущая конфигурация приложения
        """
        super().__init__()
        self.config = config.copy()
        self.recording_hotkey = False
        self.init_ui()
    
    def init_ui(self) -> None:
        """Инициализировать пользовательский интерфейс."""
        self.setWindowTitle("Настройки Votobu")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        # Основной layout
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Группа настроек горячей клавиши
        hotkey_group = self._create_hotkey_group()
        layout.addWidget(hotkey_group)
        
        # Группа настроек распознавания
        recognition_group = self._create_recognition_group()
        layout.addWidget(recognition_group)
        
        # Группа настроек модели
        model_group = self._create_model_group()
        layout.addWidget(model_group)
        
        # Растягивающийся элемент
        layout.addStretch()
        
        # Кнопки Сохранить/Отмена
        buttons_layout = self._create_buttons()
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def _create_hotkey_group(self) -> QGroupBox:
        """Создать группу настроек горячей клавиши."""
        group = QGroupBox("Горячая клавиша")
        layout = QVBoxLayout()
        
        # Описание
        description = QLabel("Клавиша для начала/окончания записи:")
        layout.addWidget(description)
        
        # Кнопка для записи клавиши
        hotkey_layout = QHBoxLayout()
        self.hotkey_label = QLabel(f"Текущая клавиша: {self.config.get('hotkey', 'F9').upper()}")
        self.hotkey_button = QPushButton("Изменить клавишу")
        self.hotkey_button.clicked.connect(self._on_record_hotkey)
        
        hotkey_layout.addWidget(self.hotkey_label)
        hotkey_layout.addWidget(self.hotkey_button)
        hotkey_layout.addStretch()
        
        layout.addLayout(hotkey_layout)
        
        # Информация
        info = QLabel("Зажмите клавишу для начала записи, отпустите для остановки")
        info.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(info)
        
        group.setLayout(layout)
        return group
    
    def _create_recognition_group(self) -> QGroupBox:
        """Создать группу настроек распознавания."""
        group = QGroupBox("Распознавание речи")
        layout = QVBoxLayout()
        
        # Выбор языка
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Язык:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(["Русский", "Английский", "Автоопределение"])
        
        # Установить текущий язык
        current_lang = self.config.get('language', 'ru')
        lang_index = {'ru': 0, 'en': 1, 'auto': 2}.get(current_lang, 0)
        self.language_combo.setCurrentIndex(lang_index)
        
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.language_combo)
        lang_layout.addStretch()
        
        layout.addLayout(lang_layout)
        
        group.setLayout(layout)
        return group
    
    def _create_model_group(self) -> QGroupBox:
        """Создать группу настроек модели Whisper."""
        group = QGroupBox("Модель Whisper")
        layout = QVBoxLayout()
        
        # Выбор модели
        model_layout = QHBoxLayout()
        model_label = QLabel("Модель:")
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large"])
        
        # Установить текущую модель
        current_model = self.config.get('whisper_model', 'base')
        model_index = ["tiny", "base", "small", "medium", "large"].index(current_model)
        self.model_combo.setCurrentIndex(model_index)
        
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        model_layout.addStretch()
        
        layout.addLayout(model_layout)
        
        # Описание моделей
        info = QLabel(
            "tiny - самая быстрая, низкое качество\n"
            "base - хороший баланс скорости и качества\n"
            "small - лучше качество, медленнее\n"
            "medium - высокое качество, требует больше ресурсов\n"
            "large - максимальное качество, очень медленная"
        )
        info.setStyleSheet("color: gray; font-size: 9px;")
        layout.addWidget(info)
        
        group.setLayout(layout)
        return group
    
    def _create_buttons(self) -> QHBoxLayout:
        """Создать кнопки управления."""
        layout = QHBoxLayout()
        
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self._on_save)
        
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.close)
        
        layout.addStretch()
        layout.addWidget(self.save_button)
        layout.addWidget(self.cancel_button)
        
        return layout
    
    def _on_record_hotkey(self) -> None:
        """Обработчик нажатия кнопки записи горячей клавиши."""
        self.hotkey_button.setText("Нажмите клавишу...")
        self.hotkey_button.setEnabled(False)
        self.recording_hotkey = True
    
    def keyPressEvent(self, event) -> None:
        """
        Перехват нажатия клавиши для записи горячей клавиши.
        
        Args:
            event: Событие нажатия клавиши
        """
        if self.recording_hotkey:
            key = event.key()
            
            # Преобразовать Qt key в строковое представление
            key_name = self._qt_key_to_string(key)
            
            if key_name:
                self.config['hotkey'] = key_name
                self.hotkey_label.setText(f"Текущая клавиша: {key_name.upper()}")
                self.hotkey_button.setText("Изменить клавишу")
                self.hotkey_button.setEnabled(True)
                self.recording_hotkey = False
    
    def _qt_key_to_string(self, qt_key: int) -> Optional[str]:
        """
        Преобразовать Qt key код в строковое представление.
        
        Args:
            qt_key: Qt key код
            
        Returns:
            Строковое представление клавиши
        """
        # Функциональные клавиши
        if Qt.Key_F1 <= qt_key <= Qt.Key_F12:
            f_num = qt_key - Qt.Key_F1 + 1
            return f"f{f_num}"
        
        # Буквы и цифры
        if Qt.Key_A <= qt_key <= Qt.Key_Z:
            return chr(qt_key).lower()
        
        if Qt.Key_0 <= qt_key <= Qt.Key_9:
            return chr(qt_key)
        
        # Специальные клавиши
        special_keys = {
            Qt.Key_Space: "space",
            Qt.Key_Return: "enter",
            Qt.Key_Enter: "enter",
            Qt.Key_Tab: "tab",
            Qt.Key_Escape: "esc",
            Qt.Key_Backspace: "backspace",
        }
        
        return special_keys.get(qt_key)
    
    def _on_save(self) -> None:
        """Обработчик нажатия кнопки Сохранить."""
        # Получить выбранный язык
        lang_map = {0: 'ru', 1: 'en', 2: 'auto'}
        self.config['language'] = lang_map[self.language_combo.currentIndex()]
        
        # Получить выбранную модель
        self.config['whisper_model'] = self.model_combo.currentText()
        
        # Отправить сигнал с новой конфигурацией
        self.settings_saved.emit(self.config)
        
        # Показать сообщение
        QMessageBox.information(
            self,
            "Настройки сохранены",
            "Настройки успешно сохранены!"
        )
        
        self.close()
    
    def closeEvent(self, event) -> None:
        """
        Обработчик закрытия окна.
        
        Args:
            event: Событие закрытия
        """
        if self.recording_hotkey:
            self.recording_hotkey = False
            self.hotkey_button.setText("Изменить клавишу")
            self.hotkey_button.setEnabled(True)
        event.accept()

