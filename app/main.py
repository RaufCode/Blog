from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import post


app = FastAPI(
    title="Blog CRUD API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(post.router)


@app.get("/")
async def root():
    return {"message": "Blog API is running"}
