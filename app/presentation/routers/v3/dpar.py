import redis
from fastapi import APIRouter, Depends, HTTPException, status

from app.application.use_cases.dpar import DparUseCase
from app.domain.exceptions import NotFoundError
from app.infrastructure.redis import get_redis
from app.infrastructure.repositories.dpar import RedisDparRepository
from app.presentation.schemas.dpar import DparKeysResponse, DparResponse, DparSet

router = APIRouter(prefix="/dpar", tags=["dpar"])


def get_dpar_use_case(client: redis.Redis = Depends(get_redis)) -> DparUseCase:
    return DparUseCase(repo=RedisDparRepository(client))


@router.get("/", response_model=DparKeysResponse, summary="キー一覧取得")
def list_keys(
    pattern: str = "*",
    use_case: DparUseCase = Depends(get_dpar_use_case),
) -> DparKeysResponse:
    keys = use_case.keys(pattern)
    return DparKeysResponse(keys=keys, count=len(keys))


@router.get("/{key}", response_model=DparResponse, summary="値取得")
def get_dpar(key: str, use_case: DparUseCase = Depends(get_dpar_use_case)) -> DparResponse:
    try:
        dpar = use_case.get(key)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    return DparResponse(key=dpar.key, value=dpar.value, ttl=dpar.ttl)


@router.put("/{key}", response_model=DparResponse, summary="値設定")
def set_dpar(
    key: str,
    data: DparSet,
    use_case: DparUseCase = Depends(get_dpar_use_case),
) -> DparResponse:
    dpar = use_case.set(key, data.value, ttl=data.ttl)
    return DparResponse(key=dpar.key, value=dpar.value, ttl=dpar.ttl)


@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT, summary="値削除")
def delete_dpar(key: str, use_case: DparUseCase = Depends(get_dpar_use_case)) -> None:
    try:
        use_case.delete(key)
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
