from fastapi import FastAPI

app = FastAPI(
    title="GinnoHub 3D Commerce API",
    description="AI-powered Image to 3D API for E-commerce",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to GinnoHub 3D Commerce API",
        "status": "Running",
        "product": "Image to 3D Conversion"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "GinnoHub API"
    }
