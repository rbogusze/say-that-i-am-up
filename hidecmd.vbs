Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c script.bat"
oShell.Run strArgs, 0, false