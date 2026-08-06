from fastapi import FastAPI

from app.auth.router import router as auth_router

app = FastAPI(
    title="Enterprise Knowledge Assistant"
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "API is running"}
