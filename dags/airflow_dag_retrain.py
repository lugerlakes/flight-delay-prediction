from __future__ import annotations
import pendulum
import logging
from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator

# --- MLOps Configuration ---
PERFORMANCE_THRESHOLD = 0.60

# Definimos las funciones de lógica de negocio (Simuladas)
def run_data_ingestion():
    logging.info("🚀 [1/4] Ingesting new flight logs...")

def run_feature_engineering():
    logging.info("⚙️ [2/4] Updating Risk Features...")

def run_model_training():
    logging.info("🧠 [3/4] Retraining XGBoost Classifier...")

def run_model_deployment():
    logging.info("💾 [4/4] Deploying new artifacts...")

# --- DAG Definition using TaskFlow API ---
@dag(
    dag_id="mlops_retrain_xgboost_flight_delay",
    description="Drift detection and automated retraining.",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    schedule="0 4 * * 1",
    catchup=False,
    tags=["mlops", "xgboost", "retraining"],
)
def flight_delay_retraining_pipeline():

    # 1. Tarea de Monitoreo (Branching)
    # El decorador @task.branch maneja la lógica de decisión automáticamente
    @task.branch(task_id="check_model_drift")
    def check_model_drift() -> str:
        logging.info("🔍 Monitoring: Analyzing production Recall...")
        
        # Simulación de métrica (esto vendría de MLflow/DB)
        current_recall = 0.55
        
        logging.info(f"📊 Current Recall: {current_recall:.2f} | Threshold: {PERFORMANCE_THRESHOLD}")

        if current_recall < PERFORMANCE_THRESHOLD:
            logging.warning("⚠️ DRIFT DETECTED. Triggering Retraining.")
            return "ingest_data" # ID de la siguiente tarea a ejecutar
        else:
            logging.info("✅ Model stable.")
            return "no_action"

    # 2. Definición de Tareas
    drift_check = check_model_drift()

    # Rama A: Re-entrenamiento (Usando PythonOperator clásico o @task)
    # Usamos @task para mantenerlo limpio
    @task(task_id="ingest_data")
    def task_ingest():
        run_data_ingestion()

    @task(task_id="feature_engineering")
    def task_fe():
        run_feature_engineering()

    @task(task_id="train_xgboost")
    def task_train():
        run_model_training()

    @task(task_id="deploy_new_version")
    def task_deploy():
        run_model_deployment()

    # Rama B: No hacer nada
    @task(task_id="no_action")
    def task_no_action():
        logging.info("Model Healthy. Pipeline finished.")

    # 3. Flujo de Dependencias
    # Si drift_check dice "ingest_data", sigue este camino:
    ingest = task_ingest()
    fe = task_fe()
    train = task_train()
    deploy = task_deploy()
    
    # Conexiones
    drift_check >> [ingest, task_no_action()]
    ingest >> fe >> train >> deploy

# Instanciar el DAG
dag_instance = flight_delay_retraining_pipeline()