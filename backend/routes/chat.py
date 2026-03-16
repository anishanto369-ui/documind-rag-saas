from fastapi import APIRouter
from pydantic import BaseModel
from core.rag_pipeline import query_documents

router = APIRouter()

class ChatRequest(BaseModel):
    question: str
    tenant_id: str

@router.post("/chat")
async def chat(req: ChatRequest):
    answer = query_documents(req.question, req.tenant_id)
    return {"answer": answer, "tenant_id": req.tenant_id}