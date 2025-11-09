"""
Менеджер глобальных горячих клавиш.
Использует pynput для перехвата клавиш и кнопок мыши.
"""

from pynput import keyboard, mouse
from pynput.keyboard import Key, KeyCode
from pynput.mouse import Button
import threading
from typing import Callable, Optional, Union


class HotkeyManager:
    """Класс для управления глобальными горячими клавишами."""
    
    # Маппинг строковых названий клавиш к pynput Key
    KEY_MAPPING = {
        'f1': Key.f1, 'f2': Key.f2, 'f3': Key.f3, 'f4': Key.f4,
        'f5': Key.f5, 'f6': Key.f6, 'f7': Key.f7, 'f8': Key.f8,
        'f9': Key.f9, 'f10': Key.f10, 'f11': Key.f11, 'f12': Key.f12,
        'ctrl': Key.ctrl, 'shift': Key.shift, 'alt': Key.alt,
        'space': Key.space, 'enter': Key.enter, 'tab': Key.tab,
        'esc': Key.esc, 'backspace': Key.backspace,
        'delete': Key.delete, 'insert': Key.insert,
        'home': Key.home, 'end': Key.end,
        'page_up': Key.page_up, 'page_down': Key.page_down,
        'up': Key.up, 'down': Key.down, 'left': Key.left, 'right': Key.right,
        'ctrl_l': Key.ctrl_l, 'ctrl_r': Key.ctrl_r,
        'shift_l': Key.shift_l, 'shift_r': Key.shift_r,
        'alt_l': Key.alt_l, 'alt_r': Key.alt_r,
    }
    
    # Маппинг кнопок мыши
    MOUSE_BUTTON_MAPPING = {
        'mouse_left': Button.left,
        'mouse_right': Button.right,
        'mouse_middle': Button.middle,
        'mouse_x1': Button.x1,  # Боковая кнопка назад
        'mouse_x2': Button.x2,  # Боковая кнопка вперед
    }
    
    def __init__(self, hotkey: str = "f9"):
        """
        Инициализация менеджера горячих клавиш.
        
        Args:
            hotkey: Строковое представление горячей клавиши (например, "f9")
        """
        self.hotkey_str = hotkey.lower()
        self.hotkey = self._parse_hotkey(self.hotkey_str)
        self.is_mouse_button = self._is_mouse_button(self.hotkey_str)
        self.on_press_callback: Optional[Callable[[], None]] = None
        self.on_release_callback: Optional[Callable[[], None]] = None
        self.keyboard_listener: Optional[keyboard.Listener] = None
        self.mouse_listener: Optional[mouse.Listener] = None
        self.is_pressed = False
        self.running = False
    
    def _is_mouse_button(self, hotkey_str: str) -> bool:
        """
        Проверить, является ли горячая клавиша кнопкой мыши.
        
        Args:
            hotkey_str: Строковое представление клавиши
            
        Returns:
            True если это кнопка мыши
        """
        return hotkey_str in self.MOUSE_BUTTON_MAPPING
    
    def _parse_hotkey(self, hotkey_str: str) -> Union[Key, KeyCode, Button]:
        """
        Преобразовать строковое представление клавиши в объект Key/KeyCode/Button.
        
        Args:
            hotkey_str: Строковое представление клавиши
            
        Returns:
            Key, KeyCode или Button объект
        """
        hotkey_str = hotkey_str.lower()
        
        # Проверить кнопки мыши
        if hotkey_str in self.MOUSE_BUTTON_MAPPING:
            return self.MOUSE_BUTTON_MAPPING[hotkey_str]
        
        # Проверить специальные клавиши
        if hotkey_str in self.KEY_MAPPING:
            return self.KEY_MAPPING[hotkey_str]
        
        # Если это обычная клавиша (буква, цифра)
        if len(hotkey_str) == 1:
            return KeyCode.from_char(hotkey_str)
        
        # По умолчанию F9
        return Key.f9
    
    def _on_key_press(self, key):
        """
        Обработчик нажатия клавиши.
        
        Args:
            key: Нажатая клавиша
        """
        try:
            # Сравнить нажатую клавишу с горячей клавишей
            if key == self.hotkey:
                if not self.is_pressed:
                    self.is_pressed = True
                    if self.on_press_callback:
                        self.on_press_callback()
        except Exception as e:
            print(f"Ошибка обработки нажатия клавиши: {e}")
    
    def _on_key_release(self, key):
        """
        Обработчик отпускания клавиши.
        
        Args:
            key: Отпущенная клавиша
        """
        try:
            # Сравнить отпущенную клавишу с горячей клавишей
            if key == self.hotkey:
                if self.is_pressed:
                    self.is_pressed = False
                    if self.on_release_callback:
                        self.on_release_callback()
        except Exception as e:
            print(f"Ошибка обработки отпускания клавиши: {e}")
    
    def _on_mouse_click(self, x, y, button, pressed):
        """
        Обработчик клика мыши.
        
        Args:
            x, y: Координаты клика
            button: Нажатая кнопка
            pressed: True если кнопка нажата, False если отпущена
        """
        try:
            if button == self.hotkey:
                if pressed and not self.is_pressed:
                    self.is_pressed = True
                    if self.on_press_callback:
                        self.on_press_callback()
                elif not pressed and self.is_pressed:
                    self.is_pressed = False
                    if self.on_release_callback:
                        self.on_release_callback()
        except Exception as e:
            print(f"Ошибка обработки клика мыши: {e}")
    
    def set_on_press(self, callback: Callable[[], None]) -> None:
        """
        Установить callback для нажатия клавиши.
        
        Args:
            callback: Функция, вызываемая при нажатии
        """
        self.on_press_callback = callback
    
    def set_on_release(self, callback: Callable[[], None]) -> None:
        """
        Установить callback для отпускания клавиши.
        
        Args:
            callback: Функция, вызываемая при отпускании
        """
        self.on_release_callback = callback
    
    def start(self) -> bool:
        """
        Запустить перехват клавиш/мыши.
        
        Returns:
            True если запуск успешен
        """
        if self.running:
            return False
        
        try:
            if self.is_mouse_button:
                # Запустить mouse listener для кнопок мыши
                self.mouse_listener = mouse.Listener(
                    on_click=self._on_mouse_click
                )
                self.mouse_listener.start()
                print(f"Перехват мыши запущен. Горячая кнопка: {self.hotkey_str}")
            else:
                # Запустить keyboard listener для клавиш
                self.keyboard_listener = keyboard.Listener(
                    on_press=self._on_key_press,
                    on_release=self._on_key_release
                )
                self.keyboard_listener.start()
                print(f"Перехват клавиш запущен. Горячая клавиша: {self.hotkey_str}")
            
            self.running = True
            return True
        except Exception as e:
            print(f"Ошибка запуска перехвата: {e}")
            return False
    
    def stop(self) -> None:
        """Остановить перехват клавиш/мыши."""
        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
        self.running = False
        self.is_pressed = False
        print("Перехват остановлен")
    
    def change_hotkey(self, new_hotkey: str) -> bool:
        """
        Изменить горячую клавишу.
        
        Args:
            new_hotkey: Новая горячая клавиша
            
        Returns:
            True если изменение успешно
        """
        was_running = self.running
        
        if was_running:
            self.stop()
        
        self.hotkey_str = new_hotkey.lower()
        self.hotkey = self._parse_hotkey(self.hotkey_str)
        self.is_mouse_button = self._is_mouse_button(self.hotkey_str)
        
        if was_running:
            return self.start()
        
        return True
    
    def get_hotkey_display_name(self) -> str:
        """
        Получить отображаемое имя горячей клавиши.
        
        Returns:
            Строковое представление клавиши для отображения
        """
        return self.hotkey_str.upper()

