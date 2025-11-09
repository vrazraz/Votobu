' Скрипт для запуска Votobu БЕЗ консольного окна
' Использует python.exe но скрывает консольное окно

Set WshShell = CreateObject("WScript.Shell")
' Запускаем python.exe (не pythonw.exe!) но с флагом 0 = скрытое окно
WshShell.Run "python.exe src\main.py", 0, False
Set WshShell = Nothing

