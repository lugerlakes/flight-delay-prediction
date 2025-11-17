from modal import Stub, Image, asgi_app, app
from typing import Dict, Any

# --- 1. Define Environment (Image) ---
# We define a base image with all necessary dependencies installed from requirements.txt.
# This ensures a reproducible environment for Modal.
image = Image.from_registry("python:3.10-slim") \
    .pip_install_from_file("requirements.txt")

# --- 2. Define Stub (Application) ---
# The Stub is the main object Modal uses to manage the application and its deployment.
stub = Stub(name="flight-delay-predictor", image=image)

# --- 3. Define the FastAPI Service ---
@stub.function()
@asgi_app()
def fastapi_app():
    """
    Deploys the FastAPI application for low-latency prediction inference.
    
    Note: The ML artifacts (.pkl files) must be uploaded to Modal's file system 
    or persisted to an external bucket/volume for the app/main.py to load them.
    """
    from app.main import app as fastapi_instance # Import the FastAPI instance
    return fastapi_instance

# --- 4. Define the Streamlit UI ---
@stub.function()
@app()
def streamlit_ui():
    """Deploys the Streamlit UI for the human interface (Dispatcher/Analyst)."""
    # NOTE: This requires the Streamlit app to be configured to call the FastAPI endpoint
    # that Modal generates for the 'fastapi_app' function.
    
    # We execute the Streamlit application file directly
    import subprocess
    subprocess.run(["streamlit", "run", "app/streamlit_app.py"])

# --- Deployment Instructions ---
# To deploy this: modal deploy modal_stub.py
# After deployment, Modal provides URLs for the FastAPI endpoint and the Streamlit UI.