from modal import Stub, Image, asgi_app, web_endpoint, mount, Secret
import os

# Define the base image, installing dependencies from requirements.txt
image = Image.from_registry("python:3.10-slim").pip_install_from_file("requirements.txt")

# Define the stub (the application)
stub = Stub(name="flight-delay-predictor-v2", image=image)

# Define which local files to upload to Modal for the app to access them.
# This ensures that the FastAPI and Streamlit apps can find the models and code.
app_files = mount.Mount.from_local_dir("app")
model_files = mount.Mount.from_local_dir("models")

# --- 1. FastAPI Backend Function (Low-Latency Inference) ---
# We use web_endpoint for the FastAPI deployment

@stub.function(
    mounts=[app_files, model_files], # Upload app code and model artifacts
    secrets=[Secret.from_name("my-api-secrets")] # Optionally load secrets (e.g., WEATHER_API_KEY)
)
@asgi_app()
def api():
    """Deploys the FastAPI application for low-latency prediction inference."""
    # Import the FastAPI instance defined in app/main.py
    from app.main import app as fastapi_instance 
    return fastapi_instance

# --- 2. Streamlit UI Function (Human-in-the-Loop Interface) ---
# We use modal.web_endpoint with web_endpoint=streamlit for the UI

@stub.function(
    mounts=[app_files, model_files],
)
@web_endpoint(method="GET")
def ui():
    """Deploys the Streamlit UI for the operational analyst."""
    # This command tells Modal to run the Streamlit file
    import subprocess
    subprocess.run(["streamlit", "run", "app/streamlit_app.py", "--server.port", "8000"])


# Deployment Command (Conceptual): modal deploy modal_stub.py