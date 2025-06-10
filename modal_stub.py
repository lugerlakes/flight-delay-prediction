# Deploy via Modal
 
import modal

stub = modal.Stub("flight-delay-api")

@stub.function()
def run_api():
    from app.main import app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
