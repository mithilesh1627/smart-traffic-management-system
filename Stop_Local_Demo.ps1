$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
& "$PSScriptRoot\.venv-demo\Scripts\python.exe" "$PSScriptRoot\demo\stop.py"
