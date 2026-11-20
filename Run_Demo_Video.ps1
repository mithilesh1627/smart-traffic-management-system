param([string]$Video = '')
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if ($Video) {
    & "$PSScriptRoot\.venv-demo\Scripts\python.exe" "$PSScriptRoot\demo\run_video.py" --video $Video
} else {
    & "$PSScriptRoot\.venv-demo\Scripts\python.exe" "$PSScriptRoot\demo\run_video.py"
}
if ($LASTEXITCODE -ne 0) { throw 'Video processing failed. Review the error above.' }
