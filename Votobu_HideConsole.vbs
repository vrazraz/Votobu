' Запуск через hide_console.py который прячет консоль после старта
' Этот способ использует python.exe но прячет консоль программно

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "python.exe hide_console.py", 0, False
Set WshShell = Nothing

