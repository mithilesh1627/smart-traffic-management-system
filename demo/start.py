"""Start only project-owned, loopback-only demo services. Safe to rerun."""
import json, os, socket, subprocess, sys, time
from pathlib import Path
from local_env import configure, ROOT, STATE
configure()

def listening(port):
    with socket.socket() as s:
        s.settimeout(.5)
        return s.connect_ex(('127.0.0.1', port)) == 0

services = [
    ('mongo',27017,[str(STATE/'bin/mongod.exe'),'--dbpath',str(STATE/'data'),'--bind_ip','127.0.0.1','--port','27017','--logpath',str(STATE/'logs/mongo.log'),'--logappend']),
    ('mlflow',5000,[sys.executable,'-m','mlflow','server','--host','127.0.0.1','--port','5000','--backend-store-uri','sqlite:///'+(STATE/'panel_mlflow.db').as_posix(),'--default-artifact-root',(STATE/'mlartifacts').as_uri()]),
    ('dashboard',8501,[sys.executable,'-m','streamlit','run','streamlit_app/app.py','--server.address','127.0.0.1','--server.port','8501','--server.headless','true','--browser.gatherUsageStats','false']),
    ('video_demo',8502,[sys.executable,'-m','streamlit','run','streamlit_app/app_live.py','--server.address','127.0.0.1','--server.port','8502','--server.headless','true','--browser.gatherUsageStats','false']),
]
records = json.loads((STATE/'processes.json').read_text()) if (STATE/'processes.json').exists() else {}
for name,port,args in services:
    if listening(port):
        print(f'{name}: already listening on {port}'); continue
    if not Path(args[0]).exists():
        print(f'{name}: missing executable {args[0]}'); continue
    log=open(STATE/'logs'/f'{name}.console.log','ab')
    proc=subprocess.Popen(args,cwd=ROOT,env=os.environ.copy(),stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,creationflags=subprocess.CREATE_NO_WINDOW)
    records[name]={'pid':proc.pid,'port':port}
    print(f'{name}: started PID {proc.pid}')
(STATE/'processes.json').write_text(json.dumps(records,indent=2))
for _ in range(45):
    if all(listening(port) for _,port,_ in services):break
    time.sleep(1)
for name,port,_ in services:print(f'{name}: '+('READY' if listening(port) else 'NOT READY - check .local-demo/logs'))
print('Dashboard: http://127.0.0.1:8501 | Upload demo: http://127.0.0.1:8502 | MLflow: http://127.0.0.1:5000')
