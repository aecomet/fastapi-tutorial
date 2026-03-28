from fastapi import APIRouter

from app.services.hello import build_hello_message

router = APIRouter()


@router.get("/")
def read_root() -> dict:
    return build_hello_message()
