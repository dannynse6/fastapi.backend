from typing import Annotated, Any
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database.session import get_db
from .security import get_current_user, require_roles

# Database
DBSession = Annotated[
    Session,
    Depends(get_db),
]

# OAuth2 Login Form
LoginForm = Annotated[
    OAuth2PasswordRequestForm,
    Depends(),
]

# Current User
CurrentUser = Annotated[
    dict[str, Any],
    Depends(get_current_user),
]

# Roles
AdminUser = Annotated[
    dict[str, Any],
    Depends(require_roles("admin")),
]