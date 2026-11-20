"""Stop only PIDs recorded by this project's launcher, with command-line checks."""
import json
from pathlib import Path
import psutil
from local_env import STATE, ROOT
p=STATE/'processes.json'
if not p.exists():raise SystemExit('No demo services recorded.')
for name,record in json.loads(p.read_text()).items():
    try:
        proc=psutil.Process(record['pid'])
        command=' '.join(proc.cmdline())
        if str(ROOT).lower() not in command.lower() and proc.cwd().lower()!=str(ROOT).lower():
            print('Skipped unrelated PID',record['pid']);continue
        for child in proc.children(recursive=True):child.terminate()
        proc.terminate()
        print('Stopped',name)
    except psutil.NoSuchProcess:pass
