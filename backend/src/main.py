from fastapi import APIRouter, FastAPI 

app = FastAPI()

router = APIRouter(prefix="/api/v1")

@router.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(router)