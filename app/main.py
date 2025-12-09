from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html

from app.core import setup_logger
from app.api.routes import router
from app.api.deps import init_workers

logger = setup_logger(__name__)

title = "Ka-Doe"
version = "1.0.0"

origins = ["*"]

app = FastAPI(title=title, version=version, docs_url=None)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title= app.title + "- Swagger UI",
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/SwaggerDark.css"
    )

app.include_router(router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    logger.info(f"{title} V. {version} is starting up...")
    
    from app.utils.startup import create_admin_user

    create_admin_user()

    await init_workers()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"{title} V. {version} is shutting down...")
