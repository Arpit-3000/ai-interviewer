from fastapi import APIRouter, UploadFile
import os

router = APIRouter()

@router.post("/upload-resume")
async def upload_resume(file: UploadFile):
    # Ensure uploads directory exists
    os.makedirs("uploads", exist_ok=True)
    
    path = f"uploads/{file.filename}"

    content = await file.read()

    with open(path, "wb") as f:
        f.write(content)

    return {
        "message": "Resume uploaded successfully",
        "path": path
    }