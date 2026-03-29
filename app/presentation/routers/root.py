from fastapi import APIRouter

from app.presentation.schemas.root import RootResponse, build_root_response

router = APIRouter()


@router.get("/", response_model=RootResponse)
def read_root() -> RootResponse:
    return build_root_response()
