from fastapi import APIRouter, UploadFile, File, Form
from core.rag_pipeline import ingest_document
import tempfile, os, shutil

router = APIRouter()

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    tenant_id: str = Form(...)
):
    # This part saves the uploaded file temporarily so the AI can read it
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    try:
        result = ingest_document(tmp_path, tenant_id=tenant_id)
        return {"status": "success", "message": result}
    finally:
        os.unlink(tmp_path) # Deletes the temp file to keep your Mac clean