from fastapi import FastAPI

from modules.auth.api.routes import (
    router as auth_router,
)

from modules.user.api.routes import (
    router as user_router,
)

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)