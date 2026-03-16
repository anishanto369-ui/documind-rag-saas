from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.upload import router as upload_router
from routes.chat import router as chat_router

app = FastAPI(title="DocuMind RAG SaaS API")

# 🛠️ THE FIX: This allows your React frontend (port 5173) 
# to talk to your FastAPI backend (port 8000).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, you'd replace "*" with your actual domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our API routes
app.include_router(upload_router, prefix="/api")
app.include_router(chat_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "DocuMind API is online and ready!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)