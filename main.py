from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes import main_process_route

# App initialization
app = FastAPI(
    title="Data Cleaner Bot",
    description="A chatbot for cleaning and visualizing datasets with automated preprocessing and plotting.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(main_process_route.router, prefix="/api", tags=["DataScrub API"])

@app.get("/", tags=["Health Check"])
async def root():
    return {
        "message": "Welcome to the Data Cleaner Bot API. Go to /docs to test endpoints."
    }
