from local_env import configure
configure()
from pymongo import MongoClient
c = MongoClient('mongodb://127.0.0.1:27017', serverSelectionTimeoutMS=3000)
doc = c.traffic_system.panel_hourly.find_one({'execution_source': 'Airflow panel_traffic_live_demo'})
assert doc and doc.get('execution_source') == 'Airflow panel_traffic_live_demo', 'Airflow analytics not found'
assert c.traffic_system.metrics.count_documents({}) > 0, 'No inference metrics found'
print('Verified real inference metrics and Airflow-produced hourly analytics in MongoDB.')
print('Refresh http://localhost:8501 and http://localhost:5000 to inspect results.')
