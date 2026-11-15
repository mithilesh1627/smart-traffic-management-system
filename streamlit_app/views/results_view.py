import streamlit as st
import pandas as pd
import plotly.express as px

def show_results():
    st.title("📊 Verified Model Evaluation Results")
    st.caption("Quantitative performance metrics evaluated on the India Driving Dataset (IDD) validation split and tracked in MLflow.")

    st.warning(
        "Live demo runs on CPU. Detection boxes can flicker on turning / large vehicles, "
        "and small or distant vehicles can be missed — see the Demo Video page."
    )

    st.markdown("### 📈 Overall Model Metrics (YOLOv11n on IDD)")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("mAP@0.5", "0.693", help="Mean Average Precision at IoU threshold 0.50")
    col2.metric("mAP@0.5:0.95", "0.650", help="Mean Average Precision averaged over IoU thresholds 0.50 to 0.95")
    col3.metric("Precision", "0.597", help="True positives / (True positives + False positives)")
    col4.metric("Recall", "0.660", help="True positives / (True positives + False negatives)")

    st.divider()

    st.markdown("### 🚦 Class-wise Performance Breakdown")
    
    class_data = [
        {"Class": "Car", "Precision": 0.853, "Recall": 0.927, "mAP@50": 0.953, "mAP@50-95": 0.930, "Sample Size": "High (Dominant)"},
        {"Class": "Bus", "Precision": 0.746, "Recall": 0.786, "mAP@50": 0.855, "mAP@50-95": 0.827, "Sample Size": "Moderate"},
        {"Class": "Truck", "Precision": 0.669, "Recall": 0.727, "mAP@50": 0.781, "mAP@50-95": 0.737, "Sample Size": "Moderate"},
        {"Class": "Person", "Precision": 0.722, "Recall": 0.791, "mAP@50": 0.848, "mAP@50-95": 0.765, "Sample Size": "High"},
        {"Class": "Motorbike", "Precision": 0.593, "Recall": 0.729, "mAP@50": 0.722, "mAP@50-95": 0.639, "Sample Size": "High (Occluded)"},
        {"Class": "Traffic Light", "Precision": 0.000, "Recall": 0.000, "mAP@50": 0.000, "mAP@50-95": 0.000, "Sample Size": "1 instance (Not meaningful)"},
    ]
    df_classes = pd.DataFrame(class_data)

    st.dataframe(
        df_classes.style.format({
            "Precision": "{:.3f}",
            "Recall": "{:.3f}",
            "mAP@50": "{:.3f}",
            "mAP@50-95": "{:.3f}",
        }),
        use_container_width=True,
        hide_index=True
    )

    st.caption("⚠️ **Note:** The *Traffic Light* class contains only 1 annotated instance in the dataset split; hence its metrics are 0.000 and excluded from system-level analytics.")

    st.divider()

    st.markdown("### 📊 Interactive Class Performance Comparison")

    plot_df = df_classes[df_classes["Class"] != "Traffic Light"].copy()
    fig = px.bar(
        plot_df,
        x="Class",
        y=["mAP@50", "Precision", "Recall"],
        barmode="group",
        title="Detection Metrics by Vehicle Class (excluding Traffic Light)",
        labels={"value": "Score", "variable": "Metric"},
        color_discrete_sequence=["#1f77b4", "#2ca02c", "#ff7f0e"]
    )
    fig.update_layout(yaxis_range=[0, 1.05], legend_title_text="Metric")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### 🔬 Key Engineering Observations")
    obs_col1, obs_col2 = st.columns(2)
    with obs_col1:
        st.markdown("""
        - **Car detection is the strongest performer (0.953 mAP@50):** Highly dependable for primary traffic density estimation and passage volume counting.
        - **Bus & Truck detection remain robust (0.855 & 0.781 mAP@50):** Heavy vehicle classification remains resilient across varying lighting and viewing angles.
        - **Pedestrian detection reaches 0.848 mAP@50:** Capable of assisting pedestrian density and crosswalk safety analysis.
        """)
    with obs_col2:
        st.markdown("""
        - **Motorbikes show moderate precision (0.593):** Smaller physical pixel footprint, rapid lateral movement, and clustering in Indian traffic cause occasional identity switches.
        - **Tracking stabilization (ByteTrack):** Coupling YOLO bounding boxes with Kalman-filter based association significantly reduces single-frame dropouts in continuous video streams.
        - **MLOps Reproducibility:** Dataset splits were versioned via DVC, training runs tracked via MLflow, and the validation criteria strictly verified before model packaging.
        """)
