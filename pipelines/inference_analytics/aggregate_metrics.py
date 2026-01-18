def aggregate():
    from utils.config import (
        MONGO_URI,
        DB_NAME,
        INFERENCE_COLLECTION_NAME
    )
    from utils.mongo_helper import get_collection
    from datetime import datetime, timedelta
    print("Starting aggregation of inference metrics...")
    end = datetime.utcnow()
    start = end - timedelta(hours=1)
    print(f"Aggregation window: {start} to {end}")
    col = get_collection(
        MONGO_URI,
        DB_NAME,
        INFERENCE_COLLECTION_NAME
    )
    print("Fetching raw metrics from MongoDB...")
    # ---------------- FETCH RAW METRICS ----------------
    data = list(
        col.find(
            {"timestamp": {"$gte": start, "$lt": end}},
            {"_id": 0}
        )
    )
    print(f"Fetched {len(data)} documents for aggregation.")
    
    if not data:
        print("No inference data found for aggregation window.")
        return None
    # ---------------- VEHICLE COUNT ----------------
    total_vehicles = 0
    for d in data:
        interval_counts = d.get("vehicle_count_interval", {})
        total_vehicles += sum(interval_counts.values())
    # ---------------- FLOW ----------------
    flows = [d.get("flow", 0) for d in data]
    avg_flow = sum(flows) / len(flows)
    peak_flow = max(flows)
    # ---------------- DENSITY ----------------
    densities = [d.get("density", 0) for d in data]
    avg_density = sum(densities) / len(densities)
    if avg_density > 0.7:
        congestion_level = "HIGH"
    elif avg_density > 0.4:
        congestion_level = "MEDIUM"
    else:
        congestion_level = "LOW"

    aggregated_doc = {
        "camera_id": data[0]["camera_id"],
        "window_size": "1h",
        "start_time": start,
        "end_time": end,
        "total_vehicles": total_vehicles,
        "avg_flow": round(avg_flow, 2),
        "peak_flow": round(peak_flow, 2),
        "avg_density": round(avg_density, 2),
        "congestion_level": congestion_level,
    }

    print("Aggregation completed successfully.")
    return aggregated_doc
