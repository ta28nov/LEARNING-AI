"""API routers."""

from .auth import router as auth_router
from .courses import router as courses_router
from .uploads import router as uploads_router
from .quiz import router as quiz_router
from .chat import router as chat_router
from .dashboard import router as dashboard_router

__all__ = [
    "auth_router", "courses_router", "uploads_router", 
    "quiz_router", "chat_router", "dashboard_router"
]
