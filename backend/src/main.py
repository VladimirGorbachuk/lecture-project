from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from configure import bind_token_implementations_to_fastapi
from exceptions.auth import BaseAuthTokenException
from views.auth import router as auth_router

app = FastAPI()
app = bind_token_implementations_to_fastapi(app)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api/v1")

@router.get("/")
def read_root():
    return {"Hello": "World"}


@app.exception_handler(BaseAuthTokenException)
def authjwt_exception_handler(request: Request, exc: BaseAuthTokenException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


router.include_router(auth_router, prefix = "/auth")
app.include_router(router)
