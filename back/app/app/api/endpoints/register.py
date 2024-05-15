from fastapi import APIRouter, Depends, Request, status
from fastapi_users import exceptions, schemas

from app.exceptions import APIException, APIExceptionSchema, ErrorCodes
from app.schemas.user import CreateUserSchema, ReadUserSchema
from app.users import UserManager, get_user_manager

router = APIRouter()


@router.post(
    "/register",
    response_model=ReadUserSchema,
    status_code=status.HTTP_201_CREATED,
    name="register:register",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": APIExceptionSchema,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCodes.REGISTER_USER_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": {
                                "non_field_errors": [],
                                "errors": [
                                    {
                                        "field": "email",
                                        "code": ErrorCodes.REGISTER_USER_ALREADY_EXISTS,
                                    }
                                ],
                            },
                        },
                        ErrorCodes.REGISTER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "non_field_errors": [],
                                "errors": [
                                    {
                                        "field": "password",
                                        "code": ErrorCodes.REGISTER_INVALID_PASSWORD,
                                    }
                                ],
                            },
                        },
                    }
                }
            },
        },
    },
)
async def register(
    request: Request,
    user_create: CreateUserSchema,
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        created_user = await user_manager.create(
            user_create, safe=True, request=request
        )
    except exceptions.UserAlreadyExists:
        raise APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            email=ErrorCodes.REGISTER_USER_ALREADY_EXISTS,
        )
    except exceptions.InvalidPasswordException:
        raise APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            password=ErrorCodes.REGISTER_INVALID_PASSWORD,
        )

    return schemas.model_validate(ReadUserSchema, created_user)
