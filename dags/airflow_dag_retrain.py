from __future__ import annotations
import pendulum
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.branch import BaseBranchOperator
from airflow.utils.context import Context
import logging
import os

# --- MLOps Configuration ---
# Threshold defined in Stage 3 for operational Recall/ROC AUC
PERFORMANCE_THRESHOLD = 0.60
MODEL_VALIDATION_NOTEBOOK = "notebooks/03_Model_Training_and_Evaluation.ipynb"

# --- 1. Custom Operator for Performance Check ---
class PerformanceCheckOperator(BaseBranchOperator):
    """
    Checks the model's performance metrics (e.g., Recall/ROC AUC) 
    against a predefined operational threshold.
    """
    def __init__(self, task_id: str, threshold: float, **kwargs) -> None:
        super().__init__(task_id=task_id, **kwargs)
        self.threshold = threshold

    def select_branch(self, context: Context) -> str:
        # NOTE: In a real system, this task would query the production log database.
        
        logging.info("Querying production metrics for Model Drift analysis...")
        
        # --- SIMULATION: Fetching last validated metric ---
        # Simulate a drop in production Recall (e.g., from 0.65 down to 0.55)
        current_performance = 0.55 
        
        logging.info(f"Current production performance: {current_performance:.2f}")

        if current_performance < self.threshold:
            logging.warning(f"Performance {current_performance:.2f} is below threshold {self.threshold}. TRIGGERING RETRAINING.")
            return 'trigger_retraining'
        else:
            logging.info("Performance is stable. Skipping full retraining.")
            return 'no_action'

# --- 2. Define Retraining Pipeline Functions ---

def run_data_ingestion(**kwargs):
    """Simulates running Stage 1: Load new raw data from logs/DB and create target."""
    logging.info("--- 1/3: Running Data Ingestion (Stage 1 logic) ---")
    # Execute modular code: from src.data.data_pipeline import run_ingestion
    pass

def run_feature_engineering(**kwargs):
    """Simulates running Stage 2: Create historical features and perform imputation."""
    logging.info("--- 2/3: Running Feature Engineering (Stage 2 logic) ---")
    # Execute modular code: from src.features.feature_engineering import run_fe
    pass

def run_model_training_and_deploy(**kwargs):
    """Simulates running Stage 3 & 4: Train model, save new artifacts, and deploy."""
    logging.info("--- 3/3: Running Model Training, Evaluation, and Persisting Artifacts ---")
    # NOTE: This task would execute the core logic of 03_Model_Training_and_Evaluation.ipynb
    # and save the new .pkl files to a storage service (like an S3 bucket or Modal Volume).
    logging.info("New model artifacts (preprocessor/model) saved. Ready for final deployment.")

# --- 3. Define Airflow DAG ---

with DAG(
    dag_id="mlops_model_governance_flight_delay",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule="0 4 * * *", # Run daily at 4:00 AM UTC
    catchup=False,
    tags=["mlops", "governance", "retraining"],
) as dag:
    
    # T1: Monitor performance in production
    monitor_performance = PerformanceCheckOperator(
        task_id="check_for_model_drift",
        threshold=PERFORMANCE_THRESHOLD,
    )

    # T2: Branch 1 - Retrain the model
    trigger_retraining = run_data_ingestion(task_id="trigger_retraining")
    
    # T3: Branch 2 - No action needed (Dummy task)
    no_action = PythonOperator(
        task_id='no_action',
        python_callable=lambda: logging.info("Model performance stable. Maintenance complete.")
    )

    # T4: Retraining sequence
    ingest_data = PythonOperator(
        task_id="ingest_new_data",
        python_callable=run_data_ingestion,
    )

    fe_pipeline = PythonOperator(
        task_id="feature_engineering_pipeline",
        python_callable=run_feature_engineering,
    )

    train_and_deploy = PythonOperator(
        task_id="train_evaluate_and_deploy_artifacts",
        python_callable=run_model_training_and_deploy,
    )

    # --- Set DAG dependencies ---
    
    # 1. Check performance and branch
    monitor_performance >> [ingest_data, no_action]

    # 2. Retraining pipeline sequence
    ingest_data >> fe_pipeline >> train_and_deploy