from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core import setup_logger, Settings, AuthToken
from app.schemas import Token, UserCreate
from app.services import ServiceUser
from app.api.deps import get_admin_user

router = APIRouter(prefix="/token")
_logger = setup_logger("Token Handler")

@router.post("/login", include_in_schema=False)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    _logger.debug("Attempting to login.")
    user = ServiceUser.authenticate_user(form_data.username, form_data.password)
    if not user:
        _logger.debug("Incorrect username or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = AuthToken.create_access_token(
        data={"sub": user.username},
        expires_delta=Settings.ACCESS_TOKEN_EXPIRE_DELTA
    )
    
    _logger.debug("Successfully login")
    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", include_in_schema=False, dependencies=[Depends(get_admin_user)])
async def register(user: UserCreate):
    _logger.debug("Registering new user.")
    ServiceUser.create_user(
        username=user.username,
        password=user.password,
        email=user.email,
        full_name=user.full_name
    )

