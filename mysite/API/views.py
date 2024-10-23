from ninja import NinjaAPI, Swagger
from .routers import *

# Create your views here.
api = NinjaAPI(
    docs=Swagger(),
    title='Hospital SDLG Api',
    version='2.0.1',
    description='Api Del HSDLG para sus aplicaciones y software'
)

api.get('/base_endpoint/')
async def base_endpoint(request):
    return {
        'message': 'Base endpoint reached',
        'method': request.method,
        'path': request.path
    }

api.add_router(prefix='/users/', router=user_router, tags=['users'])
api.add_router(prefix='/schedules/', router=schedule_router, tags=['schedules'])
api.add_router(prefix='/medics/', router=medic_router, tags=['medics'])
api.add_router(prefix='/location/', router=location_router, tags=['location'])
api.add_router(prefix='/departments/', router=department_router, tags=['departments'])
api.add_router(prefix='/services/', router=service_router, tags=['services'])
api.add_router(prefix='/appointments/', router=appointment_router, tags=['appointments'])
api.add_router(prefix='/consultations/', router=consultation_router, tags=['consultations'])