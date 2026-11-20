"""Run the repository pipeline, then store an actual aggregation and MLflow run."""
import argparse, subprocess, sys, time
from local_env import configure, ROOT, STATE
configure()
sys.path.insert(0,str(ROOT))
parser=argparse.ArgumentParser()
parser.add_argument('--video',default=str(STATE/'panel_sample.mp4'))
parser.add_argument('--execution-source', default='Manual local demo; Airflow not running')
args=parser.parse_args()
from pathlib import Path
if not Path(args.video).is_file():raise SystemExit('Video not found: '+args.video)
import mlflow
from pymongo import MongoClient
client=MongoClient('mongodb://127.0.0.1:27017',serverSelectionTimeoutMS=3000)
client.admin.command('ping')
mlflow.set_tracking_uri('http://127.0.0.1:5000')
mlflow.set_experiment('Local_Panel_Demo')
before=client.traffic_system.metrics.count_documents({})
started=time.time()
with mlflow.start_run(run_name='local_video_inference'):
    mlflow.log_params({'model':'base yolo11n.pt','video':Path(args.video).name,'purpose':'local functionality demonstration, not IDD validation','confidence':.5,'iou':.6})
    subprocess.run([sys.executable,'-m','inference.pipeline','--video',args.video],cwd=ROOT,check=True)
    from pipelines.inference_analytics.aggregate_metrics import aggregate
    result=aggregate()
    if result:
        result['execution_source']=args.execution_source
        client.traffic_system.panel_hourly.replace_one({'camera_id':result['camera_id'],'window_size':'1h'},result,upsert=True)
    inserted=client.traffic_system.metrics.count_documents({})-before
    mlflow.log_metrics({'wall_time_seconds':time.time()-started,'mongo_records_added':inserted})
    print(f'Completed. New MongoDB records: {inserted}. Refresh the dashboard and MLflow.')
