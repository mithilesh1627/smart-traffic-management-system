"""Read-only service checks for presentation day."""
from urllib.request import urlopen
import sys
from local_env import configure
configure()
failed=False
for name,url in [('Main dashboard','http://127.0.0.1:8501/_stcore/health'),('Upload demo','http://127.0.0.1:8502/_stcore/health'),('MLflow','http://127.0.0.1:5000/health')]:
    try:
        with urlopen(url,timeout=5) as response:print(name,response.status)
    except Exception as e:print(name,'FAILED',type(e).__name__);failed=True
try:
    from pymongo import MongoClient
    c=MongoClient('mongodb://127.0.0.1:27017',serverSelectionTimeoutMS=3000)
    c.admin.command('ping')
    print('MongoDB OK; raw records:',c.traffic_system.metrics.count_documents({}),'; hourly records:',c.traffic_system.panel_hourly.count_documents({}))
except Exception as e:print('MongoDB FAILED',type(e).__name__);failed=True
sys.exit(1 if failed else 0)
