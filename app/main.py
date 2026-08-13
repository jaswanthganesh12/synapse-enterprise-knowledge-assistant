from fastapi import FastAPI
from app.chat.router import router as chat_router
from app.chat.conversation_router import router as conversation_router

from app.auth.router import router as auth_router
from app.api.document import router as document_router

app = FastAPI(
    title="Enterprise Knowledge Assistant"
)

app.include_router(auth_router)
app.include_router(document_router)
app.include_router(chat_router)
app.include_router(conversation_router)


@app.get("/")
def root():
    return {"message": "API is running"}
