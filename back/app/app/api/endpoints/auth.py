from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.openapi import OpenAPIResponseType

from app.exceptions import (
    APIException,
    APIExceptionSchema,
    ErrorCodes,
    UserNotExists,
    UserWrongPassword,
)
from app.users import UserManager, fastapi_users, get_user_manager
from app.users import auth_backend as backend
from app.users.auth import RefreshableJWTStrategy

router = APIRouter()
requires_verification = False
get_current_user_token = fastapi_users.authenticator.current_user_token(
    active=True, verified=requires_verification
)

login_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": APIExceptionSchema,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCodes.USER_BAD_USERNAME: {
                        "summary": "Пользователя с таким email не существует",
                        "value": {
                            "non_field_errors": [],
                            "errors": [
                                {
                                    "field": "username",
                                    "code": ErrorCodes.USER_BAD_USERNAME,
                                }
                            ],
                        },
                    },
                    ErrorCodes.USER_BAD_PASSWORD: {
                        "summary": "Неправильный пароль",
                        "value": {
                            "non_field_errors": [],
                            "errors": [
                                {
                                    "field": "password",
                                    "code": ErrorCodes.USER_BAD_PASSWORD,
                                }
                            ],
                        },
                    },
                }
            }
        },
    },
    **backend.transport.get_openapi_login_responses_success(),
}


@router.post(
    "/login",
    name=f"auth:{backend.name}.login",
    responses=login_responses,
)
async def login(
    request: Request,
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager: UserManager = Depends(get_user_manager),
    strategy: RefreshableJWTStrategy = Depends(backend.get_strategy),
):
    try:
        user = await user_manager.authenticate(credentials)
    except UserNotExists:
        raise APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            username=ErrorCodes.USER_BAD_USERNAME,
        )
    except UserWrongPassword:
        raise APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            password=ErrorCodes.USER_BAD_PASSWORD,
        )

    response = await backend.login(strategy, user)
    await user_manager.on_after_login(user, request, response)
    return response

