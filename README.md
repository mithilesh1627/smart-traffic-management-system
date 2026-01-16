#  Smart Traffic Management System

**End-to-End Computer Vision + MLOps Pipeline using YOLO, Airflow, MLflow & DVC**

This project implements a production-grade **Smart Traffic Management System** that processes traffic videos to detect, track, and analyze vehicles. The system is fully automated using **Apache Airflow**, supports **dataset versioning with DVC**, and tracks experiments using **MLflow**.

Designed as a **resume-grade flagship MLOps + Computer Vision project**.

---

## 🎯 Problem Statement & Motivation

Urban traffic monitoring systems often rely on manual analysis or fragmented tools,
making it difficult to derive real-time insights such as vehicle density, flow,
and congestion patterns.

This project aims to build a **scalable, automated, and reproducible traffic analytics system**
that:
- Converts raw traffic videos into structured insights
- Automates training and inference using MLOps best practices
- Enables rapid experimentation and deployment of CV models

---
## ✨ Key Features

| Feature | Description |
|------|-----------|
| 🚗 Vehicle Detection | YOLO-based real-time object detection |
| 🎯 Object Tracking | Persistent ID tracking across frames |
| 📈 Traffic Metrics | Vehicle count, flow, density estimation |
| 🧪 Dataset Validation | Integrity checks & auto-labeling |
| 🔁 Experiment Tracking | MLflow logging & reproducibility |
| 📊 Visualization | Streamlit dashboards |

---
## 🧰 Tech Stack

| Layer | Tools |
|-----|------|
| Computer Vision | YOLO (Ultralytics), OpenCV |
| Deep Learning | PyTorch |
| Workflow Orchestration | Apache Airflow |
| Experiment Tracking | MLflow |
| Dataset Versioning | DVC |
| Database | MongoDB |
| Visualization | Streamlit, Plotly |
| Language | Python 

## 📁 Project Structure
>  **Repository Overview**  
> This repository follows a **production-ready, modular layout** inspired by
> real-world ML systems.

```text
smart-traffic-management-system/        # End-to-end Smart Traffic Management (CV + MLOps)

├── airflow/                            # Airflow orchestration layer (pipelines & DAGs)
│   └── dags/                           # Airflow DAG definitions
│       ├── data_preprocessing_dag.py   # Dataset preprocessing & validation DAG
│       ├── smart_traffic_pipeline.py   # End-to-end traffic ML pipeline DAG
│       ├── train_yolo_dag.py            # YOLO training DAG (GPU-enabled)
│       ├── __init__.py
│       └── individual_dags/             # Split-wise dataset DAGs
│           ├── test_dataset_dags.py     # Test dataset pipeline
│           ├── train_dataset_dags.py    # Train dataset pipeline
│           └── valid_dataset_dags.py    # Validation dataset pipeline
│
├── data_processing/                    # Dataset utilities & experiments (offline scripts)
│   ├── rename_dataset_images.py        # Normalize dataset image names
│   ├── test_auto_labeling.py           # Auto-labeling for test split
│   ├── test_image_dataset.py           # Dataset sanity checks (test)
│   ├── train_auto_labeling.py          # Auto-labeling for train split
│   ├── train_image_dataset.py          # Train dataset preparation
│   ├── valid_auto_labeling.py          # Auto-labeling for validation split
│   ├── valid_image_dataset.py          # Validation dataset preparation
│   ├── verify_yolo_bboxes.py           # YOLO bounding-box visualization
│   └── __init__.py
│
├── docker/                             # Dockerization for services
│   ├── airflow/                       # Airflow container setup
│   │   └── Dockerfile
│   ├── inference/                     # Inference service container
│   │   └── Dockerfile
│   └── streamlit/                     # Streamlit dashboard container
│       └── Dockerfile
│
├── IDD_Dataset/                       # IDD dataset (DVC-tracked, large files ignored)
│   ├── Processed_dataset/             # Cleaned & split dataset
│   │   ├── train/                     # Training split
│   │   │   ├── images/                # Train images
│   │   │   └── label/                 # Train labels (YOLO format)
│   │   ├── test/                      # Test split
│   │   │   ├── images/
│   │   │   └── label/
│   │   └── valid/                     # Validation split
│   │       ├── images/
│   │       └── label/
│   ├── data.yaml                      # YOLO dataset config
│   ├── train.txt                      # Train image paths
│   ├── test.txt                       # Test image paths
│   └── val.txt                        # Validation image paths
│
├── inference/                         # Inference pipeline (runtime execution)
│   ├── pipeline.py                    # CLI-based inference pipeline
│   ├── pipeline_without_cmd.py        # Programmatic inference pipeline
│   └── __init__.py
│
├── mlruns/                            # MLflow experiment tracking (auto-generated)
│
├── notebook/                          # Research & experimentation notebooks
│   ├── auto_label.ipynb               # Auto-labeling experiments
│   ├── data_analysis.ipynb            # Dataset analysis
│   ├── test_split.py                  # Dataset split testing
│   └── yolo11n.pt                     # Pretrained YOLO weights
│
├── pipelines/                         # Core ML pipeline logic (used by Airflow)
│   ├── dataset_cleaner.py             # Remove corrupt/unlabeled images
│   ├── dataset_labeling.py            # YOLO-based auto labeling
│   ├── dataset_validator.py           # Dataset integrity validation
│   ├── mark_dataset_ready.py          # Dataset readiness (.done marker)
│   ├── mlflow_dedup.py                # Training deduplication logic
│   ├── mlflow_dvc_logger.py           # DVC + MLflow logging
│   ├── mlflow_yolo_logger.py          # YOLO model MLflow logging
│   ├── test_dataset_builder.py        # Test dataset builder
│   ├── training_fingerprint.py        # Unique training signature
│   ├── training_params.py             # Centralized training parameters
│   ├── train_dataset_builder.py       # Train dataset builder
│   ├── valid_dataset_builder.py       # Validation dataset builder
│   ├── yolo_training.py               # YOLO training logic
│   └── __init__.py
│
├── streamlit_app/                     # Interactive Streamlit dashboard
│   ├── app.py                         # Streamlit app entry point
│   ├── components/                   # Reusable UI components
│   │   ├── camera_utils.py
│   │   ├── charts.py
│   │   ├── config_streamlit.py
│   │   ├── mlflow_reader.py
│   │   ├── mongo_reader.py
│   │   ├── run_job.py
│   │   ├── upload_handler.py
│   │   ├── video.py
│   │   └── __init__.py
│   ├── views/                        # Dashboard pages
│   │   ├── camera_dashboard.py
│   │   ├── dashboard.py
│   │   ├── home.py
│   │   ├── live_traffic.py
│   │   ├── video_analyzer.py
│   │   └── __init__.py
│   └── __init__.py
│
├── traffic_metrics/                  # Domain-specific traffic analytics
│   ├── density.py                    # Traffic density estimation
│   ├── flow.py                       # Vehicle flow calculation
│   ├── traffic_engine.py             # Core traffic logic engine
│   ├── vehicle_count.py              # Vehicle counting logic
│   └── __init__.py
│
├── user_upload_data/                 # User-uploaded inference data
│   ├── outputs/                      # Inference outputs
│   └── uploads/                      # Uploaded videos
│
├── utils/                            # Shared utilities & helpers
│   ├── airflow_config.py             # Global Airflow configs
│   ├── config.py                     # Global project configs
│   ├── insert_fake_data.py           # Test data insertion
│   ├── metrics_aggregator.py         # Metric aggregation
│   ├── mlflow_tracker.py             # MLflow helpers
│   ├── mongo.py                      # MongoDB connection
│   ├── mongo_writer.py               # MongoDB writers
│   ├── tracker_adapter.py            # Tracker abstraction
│   ├── video_reader.py               # Video input utilities
│   ├── yolo_tracker.py               # YOLO inference wrapper
│   └── __init__.py
│
├── visualization/                    # Visualization helpers
│   ├── draw_utils.py                 # Bounding box rendering
│   ├── video_writer.py               # Output video writer
│   └── __init__.py
│
├── docker-compose.yml                # Multi-container orchestration
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
└── LICENSE                           # License

```

---

## 🏗️ System Architecture

The Smart Traffic Management System follows a layered, production-grade MLOps architecture
covering **data ingestion → training → inference → analytics**, orchestrated via Apache Airflow.

<p align="center">
  <img src="docs/system_architecture.png"
       alt="Smart Traffic Management System Architecture"
       width="850"/>
</p>

<p align="center">
  <em>End-to-end Computer Vision + MLOps architecture using YOLO, Airflow, MLflow & DVC</em>
</p>

### 🏗️ Architecture Flow Summary

1. **Data Ingestion**  
   Raw traffic videos are collected from cameras or user uploads.

2. **Data Processing**  
   Videos are preprocessed and validated to ensure label integrity and data quality.

3. **Dataset Versioning (DVC)**  
   Clean datasets are versioned and reproducible across experiments.

4. **Model Training (YOLO)**  
   YOLO models are trained using Airflow-managed pipelines with full experiment tracking in MLflow.

5. **Model Registry**  
   Trained models are stored and promoted for inference.

6. **Inference Pipeline**  
   Videos are processed using the trained model, followed by object tracking and traffic analytics.

7. **Storage & Visualization**  
   Metrics are stored in MongoDB / CSV and visualized via a Streamlit dashboard.


## 🧠 Airflow DAG Design

The system is orchestrated using Apache Airflow with modular DAGs:

| DAG Name | Responsibility |
|--------|----------------|
| data_preprocessing_dag | Dataset cleaning, validation, and auto-labeling |
| train_yolo_dag | YOLO training with MLflow & DVC integration |
| smart_traffic_pipeline | End-to-end pipeline from data → inference |
| train/test/valid DAGs | Split-wise dataset processing |

Each DAG is designed to be:
- Idempotent
- Retry-safe
- Independently triggerable



##  Airflow DAG Orchestration

Apache Airflow is used to orchestrate the complete ML lifecycle — from dataset validation
to model training and inference — ensuring reproducibility and automation.

###  End-to-End Smart Traffic Pipeline DAG

<p align="center">
  <img src="docs/airflow/smart_traffic_pipeline_dag.png"
       alt="Smart Traffic End-to-End Airflow DAG"
       width="900"/>
</p>

<p align="center">
  <em>Master DAG coordinating preprocessing, training, inference, and monitoring</em>
</p>



###  YOLO Training DAG

<p align="center">
  <img src="docs/airflow/train_yolo_dag.png"
       alt="YOLO Training Airflow DAG"
       width="900"/>
</p>

<p align="center">
  <em>Automated YOLO training with dataset validation, DVC versioning, and MLflow tracking</em>
</p>



###  Dataset Preprocessing & Validation DAG

<p align="center">
  <img src="docs/airflow/data_preprocessing_dag.png"
       alt="Dataset Preprocessing Airflow DAG"
       width="900"/>
</p>

<p align="center">
  <em>Ensures dataset integrity before training or inference</em>
</p>

---
## 📊 Streamlit Dashboard

The system includes an interactive **Streamlit dashboard** for monitoring traffic analytics,
model performance, and inference outputs in real time.

###  Home Dashboard

<p align="center">
  <img src="docs/streamlit/home_dashboard.png"
       alt="Streamlit Home Dashboard"
       width="900"/>
</p>

<p align="center">
  <em>Central control panel for traffic monitoring and job execution</em>
</p>

---

###  Live Traffic Analysis

<p align="center">
  <img src="docs/streamlit/live_traffic.png"
       alt="Live Traffic Analysis"
       width="900"/>
</p>

<p align="center">
  <em>Real-time vehicle detection, tracking, and traffic density visualization</em>
</p>

---

###  Analytics & Metrics Dashboard

<p align="center">
  <img src="docs/streamlit/analytics_dashboard.png"
       alt="Traffic Analytics Dashboard"
       width="900"/>
</p>

<p align="center">
  <em>Historical metrics, flow analysis, and ML experiment insights</em>
</p>

---

## 📦 Dataset Information

This project uses the India Driving Dataset (IDD) for training and evaluation of traffic
object detection models.

 Dataset Details

Name: India Driving Dataset (IDD)

Domain: Road scene understanding (Indian traffic conditions)

Content: Images captured from Indian roads

Annotations: Vehicle classes, road objects, and scene elements

Use Case: Vehicle detection, traffic analysis, and urban mobility research

Dataset Credits

> Authors: IIT Madras Research Team

> Official Website: https://idd.insaan.iiit.ac.in/

### 🧠 Why IDD?

Indian traffic presents unique challenges:

Mixed traffic (cars, bikes, buses, pedestrians)

Non-lane-based driving

Dense urban scenes

Using IDD ensures the model learns real-world complexity, making the system more robust
than models trained on synthetic or western datasets.

### 📂 Dataset Management

Dataset is versioned using DVC

Large files are excluded from Git and pulled on demand

Train / Test / Validation splits are fully reproducible
``` bash
dvc pull
```
⚠️ Note: The dataset itself is not redistributed with this repository.
Please follow the original IDD license terms.

##  Setup & Installation

This section explains how to set up the Smart Traffic Management System locally for **training, inference, and visualization**.

### 1) Prerequisites

Ensure the following are installed:

- Python ≥ 3.9  
- Git  
- DVC (for dataset versioning)  
- MongoDB (local or remote)  
- Apache Airflow  
- (Optional) CUDA + GPU for faster YOLO training  

### 2) Clone the Repository

```bash
git clone https://github.com/mithilesh1627/smart-traffic-management-system.git
cd smart-traffic-management-system
```

### 3) Create & Activate Virtual Environment
  ##### a) Linux / macOS / WSL
  ``` bash
      python3 -m venv venv
      source venv/bin/activate
   ```
  ##### b) Windows (PowerShell)
  ```bash
    python -m venv venv
    venv\Scripts\activate
  ```
### 4) Install Dependencies
  ```bash
  pip install --upgrade pip
  pip install -r requirements.txt
  ```
### 5) Dataset Setup (DVC)
 This project uses DVC to manage large datasets.
```bash
dvc pull
```
Ensure your DVC remote is configured before running this command.

### 6) Configure Environment Variables

Create a .env file in the project root:
``` env 
# MongoDB
MONGO_URI=mongodb://localhost:27017
MONGO_DB=traffic_db

# MLflow
MLFLOW_TRACKING_URI=sqlite:///mlflow.db

# Paths
DATA_ROOT=IDD_Dataset
MODEL_ROOT=models
```
### 7) Airflow Setup

Initialize Airflow metadata database:
``` bash
airflow db init
```

Start Airflow services:
```bash
airflow webserver --port 8080
airflow scheduler
```
Open Airflow UI:
  > http://localhost:8080

### 8) Run Training Pipeline

Trigger the YOLO training pipeline from the Airflow UI:
``` sql
DAGs → train_yolo_dag → Trigger
```

This pipeline performs:

      Dataset validation
      
      DVC versioning

      YOLO training

      MLflow experiment tracking
      
### 9) Run Inference Pipeline

Run inference on a video file:
```bash
python inference/pipeline.py --source /path/to/video.mp4
```

Outputs:

    Tracked video
    Traffic metrics
    MongoDB / CSV records
    
###  10) Launch Streamlit Dashboard (Optional)
```bash
cd streamlit_app
streamlit run app.py
```
Open in browser:
>  http://localhost:8501

## 🚀 Future Enhancements

- Multi-camera tracking  
- Detect whether the driver is wearing a helmet and notify administrators via IoT (Raspberry Pi)  
- Vehicle re-identification  
- Number plate recognition  
- Detection of traffic rule violations  
- Real-time Kafka-based data ingestion  

<hr/>

<p align="center">
  Built with  by <b>Mithilesh Chaurasiya</b>  
  <br/>
  NIT-Agartala
  2026
</p>
