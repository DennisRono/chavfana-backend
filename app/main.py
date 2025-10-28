from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, Depends, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from chavfana.core.config import settings
from app.api.routes import api_router
from chavfana.core.exceptions import setup_exception_handlers
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting ChavFana System API...")
    yield
    logging.info("Shutting down...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Farm Management System",
    debug=settings.ENVIRONMENT.lower() == "development",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    contact={
        "name": "ChavFana System",
        "url": "https://chavfana.co.ke",
        "email": "support@chavfana.ke",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/static", StaticFiles(directory="static"), name="static")

directory = Path(__file__).joinpath("../../static").resolve()
templates = Jinja2Templates(directory)

@app.get("/rapi-docs", include_in_schema=False)
async def rapi_docs(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "/docs.html",
        {
            "request": request,
            "schema_url": "/openapi.json",
            "title": str(settings.PROJECT_NAME),
        },
    )


app.include_router(api_router, prefix="/api/v1")


setup_exception_handlers(app)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "ChavFana API",
        "version": settings.VERSION,
        "status": "running",
    }

from fastapi import WebSocket


@app.websocket("/ws/echo")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        await ws.send_text(f"Echo: {data}")
