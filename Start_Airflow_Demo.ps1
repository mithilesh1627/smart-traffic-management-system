$ErrorActionPreference = 'Stop'
& "$PSScriptRoot\Start_Local_Demo.ps1"
wsl -d Ubuntu-22.04 -- bash /mnt/d/2026/smart-traffic-management-system/demo/start_airflow.sh
Write-Host 'Airflow: http://localhost:8080 (allow about 30 seconds to start)'
Write-Host 'Username: admin. Password: run wsl -d Ubuntu-22.04 -- cat /home/mithilesh/airflow-panel-demo/standalone_admin_password.txt'
