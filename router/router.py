from fastapi import APIRouter, FastAPI

app_controllers = [

]

def setup_routes():
    router = APIRouter()
    for controller in app_controllers:
        router.include_router(router=controller.get('router'), tags=controller.get('tags'))
    return router