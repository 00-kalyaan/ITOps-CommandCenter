Write-Host "Flushing DNS..."
ipconfig /flushdns
if ($LASTEXITCODE -eq 0) { Write-Output "DNS cache flushed." } else { exit 1 }
