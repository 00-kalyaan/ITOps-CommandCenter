Write-Host "Clearing print spool..."
net stop spooler
Start-Sleep -Seconds 2
Get-ChildItem -Path C:\\Windows\\System32\\spool\\PRINTERS -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue
net start spooler
Write-Output "Print queue cleared."
