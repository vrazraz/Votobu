"""
Скрипт для создания иконок приложения.
Создает простые иконки микрофона для трея.
"""

from PIL import Image, ImageDraw
from pathlib import Path


def create_microphone_icon(size=64, color=(100, 100, 255), output_path="icon.png"):
    """
    Создать иконку микрофона.
    
    Args:
        size: Размер иконки
        color: Цвет микрофона (RGB)
        output_path: Путь для сохранения
    """
    # Создать изображение с прозрачным фоном
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Параметры микрофона
    padding = size // 8
    mic_width = size // 3
    mic_height = size // 2
    
    # Координаты микрофона
    mic_left = (size - mic_width) // 2
    mic_top = padding
    mic_right = mic_left + mic_width
    mic_bottom = mic_top + mic_height
    
    # Нарисовать капсулу микрофона (эллипс сверху + прямоугольник)
    # Верхняя часть - эллипс
    draw.ellipse(
        [mic_left, mic_top, mic_right, mic_top + mic_width],
        fill=color
    )
    
    # Средняя часть - прямоугольник
    draw.rectangle(
        [mic_left, mic_top + mic_width // 2, mic_right, mic_bottom],
        fill=color
    )
    
    # Нарисовать ручку микрофона
    handle_top = mic_bottom
    handle_bottom = size - padding - size // 8
    handle_left = size // 2 - size // 20
    handle_right = size // 2 + size // 20
    
    draw.rectangle(
        [handle_left, handle_top, handle_right, handle_bottom],
        fill=color
    )
    
    # Нарисовать основание микрофона
    base_y = size - padding - size // 16
    base_width = size // 3
    draw.line(
        [(size // 2 - base_width // 2, base_y), (size // 2 + base_width // 2, base_y)],
        fill=color,
        width=size // 16
    )
    
    # Сохранить
    img.save(output_path)
    print(f"Создана иконка: {output_path}")


def create_recording_icon(size=64, color=(255, 50, 50), output_path="icon_recording.png"):
    """
    Создать иконку микрофона для записи (красный цвет).
    
    Args:
        size: Размер иконки
        color: Цвет микрофона (RGB) - красный
        output_path: Путь для сохранения
    """
    # Создать базовую иконку микрофона
    create_microphone_icon(size, color, output_path)
    
    # Добавить красный круг индикатора записи
    img = Image.open(output_path)
    draw = ImageDraw.Draw(img)
    
    # Нарисовать маленький красный круг в углу
    circle_size = size // 5
    circle_x = size - circle_size - size // 10
    circle_y = size // 10
    
    draw.ellipse(
        [circle_x, circle_y, circle_x + circle_size, circle_y + circle_size],
        fill=(255, 0, 0)
    )
    
    img.save(output_path)
    print(f"Создана иконка записи: {output_path}")


def main():
    """Создать все необходимые иконки."""
    # Создать директорию assets если не существует
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    # Создать иконки
    create_microphone_icon(
        size=64,
        color=(70, 130, 255),
        output_path=str(assets_dir / "icon.png")
    )
    
    create_recording_icon(
        size=64,
        color=(255, 80, 80),
        output_path=str(assets_dir / "icon_recording.png")
    )
    
    print("\nВсе иконки созданы успешно!")


if __name__ == "__main__":
    main()

