from airflow.decorators import dag, task
from datetime import datetime, timedelta

default_args = {
    "owner": "Mithilesh Chaurasiya",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

@dag(
    dag_id="traffic_inference_analytics_dag",
    start_date=datetime(2026, 1, 1),
    schedule="0 5 * * *",  
    catchup=False,
    tags=["inference", "analytics", "traffic"],
    default_args=default_args,
)
def traffic_analytics_dag():
    """
                Cron format has 5 fields:

            ┌──────── minute (0–59)
            │ ┌────── hour (0–23)
            │ │ ┌──── day of month (1–31)
            │ │ │ ┌── month (1–12)
            │ │ │ │ ┌─ day of week (0–6, Sun=0)
            │ │ │ │ │
            0  *  *  *  *

             Breakdown
            Field	    Value	    Meaning
            Minute	       0	   At minute 0
            Hour	       *	    Every hour
            Day	           *	    Every day
            Month	       *	    Every month
            Weekday	       *	   Every day of week
    """

    @task
    def fetch_raw_metrics():
        from pipelines.inference_analytics.fetch_metric import fetch_metrics
        return fetch_metrics()
    
    @task
    def aggregate_metrics():
        from pipelines.inference_analytics.aggregate_metrics import aggregate
        return aggregate()

    @task
    def store_analytics(final_doc):
        from pipelines.inference_analytics.store_results import store
        store(final_doc)

    raw = fetch_raw_metrics()
    aggregated = aggregate_metrics(raw)
    store_analytics(aggregated)


# dag = traffic_analytics_dag()
