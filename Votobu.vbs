' Скрипт для запуска Votobu БЕЗ консольного окна
' Двойной клик на этот файл для невидимого запуска

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw.exe src\main.py", 0, False
Set WshShell = Nothing

