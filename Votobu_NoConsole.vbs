' Альтернативный способ запуска без консоли
' Запускает через Python лаунчер

Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw.exe Votobu_silent.pyw", 0, False
Set WshShell = Nothing

