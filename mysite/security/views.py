from ninja import Router
from .routers import *

# Create your views here.

security_router = Router()

security_router.add_router('/credentials/', router=JWT_router, tags=['Json Web Token'])
security_router.add_router('/google/', router=google_router, tags=['Google Handler Session'])