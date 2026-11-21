
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
from io import BytesIO
from pathlib import Path
from uuid import uuid4

app = FastAPI(
    title="GinnoHub 3D Commerce API",
    description="AI-powered Image to 3D API for E-commerce",
    version="1.2.0"
)

# Create the uploads folder automatically
UPLOAD_DIR = Path(__file__).resolve().parent.parent / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


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


@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):

    allowed_types = ["image/jpeg", "image/png"]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only JPG and PNG images are allowed"
        )

    contents = await file.read()

    if len(contents) == 0:
        raise HTTPException(
            status_code=400,
            detail="Uploaded image is empty"
        )

    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="Image must be smaller than 10 MB"
        )

    try:
        image = Image.open(BytesIO(contents))

        actual_format = image.format
        width, height = image.size

        if actual_format not in ["JPEG", "PNG"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid image format"
            )

        if width < 256 or height < 256:
            raise HTTPException(
                status_code=400,
                detail="Image dimensions must be at least 256x256 pixels"
            )

        image.verify()

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid image file"
        )

    # Generate a unique filename
    extension = "jpg" if actual_format == "JPEG" else "png"
    saved_filename = f"{uuid4().hex}.{extension}"

    # Save the validated image
    save_path = UPLOAD_DIR / saved_filename
    save_path.write_bytes(contents)

    return {
        "message": "Image uploaded and saved successfully",
        "original_filename": file.filename,
        "saved_filename": saved_filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
        "width": width,
        "height": height,
        "storage": "Local uploads folder",
        "status": "Ready for 3D processing"
    }
