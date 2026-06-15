from fastapi import APIRouter
from fastapi import Depends

from core.dependencies import (
    get_current_user,
    require_roles,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me")
def me(
    current_user=Depends(
        get_current_user
    ),
):
    return current_user


@router.get("")
def list_users(
    current_user=Depends(
        require_roles(
            "ADMIN",
        )
    ),
):
    return {
        "message": "Admin only"
    }