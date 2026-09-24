from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import router
from config.settings import settings

app = FastAPI(
    title="CodeGen Agent API",
    description="Autonomous Multi-Agent Code Generation Service powered by LangGraph, LangChain, and Groq Llama 3.3.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
