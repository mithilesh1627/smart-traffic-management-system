$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
& "$PSScriptRoot\.venv-demo\Scripts\python.exe" "$PSScriptRoot\demo\start.py"
if ($LASTEXITCODE -ne 0) { throw 'Demo startup failed. See .local-demo/logs.' }
