from modal import Stub, Image, asgi_app, web_endpoint, mount, Secret
import subprocess
import os

# --- 1. Base Image Configuration ---
# Uses the Python 3.10 slim image and installs all dependencies 
# specified in your requirements.txt.
image = Image.from_registry("python:3.10-slim").pip_install_from_file("requirements.txt")

# Define the stub (the main application)
stub = Stub(name="flight-delay-predictor-v2", image=image)

# Define local mounts to upload application code and model artifacts.
app_files = mount.Mount.from_local_dir("app")
model_files = mount.Mount.from_local_dir("models")

# --------------------------------------------------------------------------
# --- 2. Backend Function (FastAPI - Low-Latency Inference) ---
# --------------------------------------------------------------------------

@stub.function(
    # Uploads app code and model artifacts
    mounts=[app_files, model_files], 
    # Loads secrets for environment variables (e.g., API Keys)
    secrets=[Secret.from_name("my-api-secrets")] 
)
@asgi_app()
def api():
    """Deploys the FastAPI application for prediction inference."""
    # Import the FastAPI instance defined in app/main.py
    from app.main import app as fastapi_instance 
    return fastapi_instance

# --------------------------------------------------------------------------
# --- 3. Frontend Function (Streamlit - User Interface) ---
# --------------------------------------------------------------------------

@stub.function(
    mounts=[app_files, model_files],
)
# Key Improvement: This tells Modal to start the Streamlit server 
# using the specified file, managing host and port automatically.
@web_endpoint(streamlit=True) 
def ui():
    """Deploys the Streamlit UI for the operational analyst."""
    # Executes Streamlit. Modal manages host and port assignment.
    subprocess.run(["streamlit", "run", "app/streamlit_app.py"])

# Deployment Command (Conceptual): modal deploy modal_stub.py