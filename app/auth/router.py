from fastapi import APIRouter

from app.auth.exceptions import UnexpectedErr1, UnexpectedErr2
from app.auth.models import AuthStartResponse, AuthItemResponse
from core.docs import doc_e
from core.response import AppResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get(
    "/start",
    response_model=AppResponse[AuthStartResponse],
    description=doc_e(UnexpectedErr1, UnexpectedErr2)
)
def start() -> AuthStartResponse:
    return AuthStartResponse(state="OK")


@router.get(
    "/items/{item_id}",
    response_model=AppResponse[AuthItemResponse],
    description=doc_e(UnexpectedErr1)
)
def get_item(item_id: int) -> AuthItemResponse:
    return AuthItemResponse(item=item_id)
