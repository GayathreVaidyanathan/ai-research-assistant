from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers.research import router

app = FastAPI(title="AI Research Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/research", tags=["research"])

@app.get("/")
def root():
    return {"message": "AI Research Assistant API is running!"}