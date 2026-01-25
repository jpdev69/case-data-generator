from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import cases, health, submissions
from app.core.config import get_settings


def create_application() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, debug=settings.debug)

    app.include_router(health.router, prefix=settings.api_prefix)
    app.include_router(cases.router, prefix=settings.api_prefix)
    app.include_router(submissions.router, prefix=settings.api_prefix)

    # Serve a simple static page with a "generate case" button under /ui.
    app.mount("/ui", StaticFiles(directory="app/static", html=True), name="static")

    @app.get("/")
    async def root_redirect():
        return RedirectResponse(url="/ui/")

    return app


app = create_application()
