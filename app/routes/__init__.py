"""Routes package."""
from .main import main
from .auth import auth
from .media import media
from .api import api
from .blog import blog

__all__ = ['main', 'auth', 'media', 'api', 'blog']
