from enum import StrEnum
from typing import Annotated

from fastapi.exceptions import RequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from pydantic import BaseModel, Field
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


class ErrorCodes(StrEnum):
    USER_BAD_USERNAME = "Такого пользователя нет в нашей базе :(("
    USER_BAD_PASSWORD = "Некорректный пароль"
    USER_BAD_EMAIL = "Некорректный логин"
    PASSWORDS_MISMATCH = "Введённые пароли не совпадают"
    WEAK_PASSWORD = "Слишком слабый пароль"
    REGISTER_INVALID_PASSWORD = "Слишком слабый пароль"
    REGISTER_USER_ALREADY_EXISTS = "Пользователь с таким логином уже существует"
    LOGIN_BAD_CREDENTIALS = "Неправильно введён логин или пароль"

class FieldErrorSchema(BaseModel):
    field: Annotated[
        str, Field(..., json_schema_extra={"description": "Название поля с ошибкой"})
    ]
    code: Annotated[str, Field(..., json_schema_extra={"description": "Код ошибки"})]


class APIExceptionSchema(BaseModel):
    non_field_errors: Annotated[
        list[str],
        Field(None, json_schema_extra={"description": "Ошибки запроса в целом"}),
    ]
    errors: Annotated[
        list[FieldErrorSchema],
        Field(None, json_schema_extra={"description": "Ошибки в полях"}),
    ]


class APIException(Exception):
    """
    Исключение, которое нужно поднимать в коде для возвращения HTTP ответа
    с ошибкой по API.
    """

    def __init__(
        self,
        status_code: int,
        headers: dict | None = None,
        non_field_errors: ErrorCodes | list[ErrorCodes] | None = None,
        errors: list | None = None,
        **kwargs: ErrorCodes
    ) -> None:
        """
        :param status_code: статус код ответа
        :param headers: дополнительные заголовки ответа
        :param non_field_errors: код или список кодов ошибок, которые относятся
        к запросу в целом
        :param kwargs: ошибки в полях форм. Здесь название передаваемого аргумента --
        название поля, в котором допущена ошибка; значение -- код ошибки.
        """
        if not non_field_errors and not kwargs and not errors:
            raise ValueError("non_field_errors, errors or kwarg error should be passed")
        self.status_code = status_code
        self.headers = headers
        if isinstance(non_field_errors, str):
            non_field_errors = [non_field_errors]
        elif non_field_errors is None:
            non_field_errors = []
        self.non_field_errors = non_field_errors
        self.errors = errors or []
        for field_name, code in kwargs.items():
            self.errors.append(FieldErrorSchema(field=field_name, code=code))

    def to_schema(self) -> APIExceptionSchema:
        return APIExceptionSchema(
            non_field_errors=self.non_field_errors, errors=self.errors
        )


async def api_exception_handler(request: Request, exc: APIException) -> Response:
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return JSONResponse(
        exc.to_schema().model_dump(), status_code=exc.status_code, headers=headers
    )


# Дополнять по мере необходимости
pydantic_errors_to_codes = {
    "The part after the @-sign is not valid. It should have a period.": "Неверный email",
    "The part after the @-sign is not valid. It is not within a valid top-level domain.": "Неверный email",
    "String should match pattern '^[^\\d\\W_]*[.,' -]*[^\\d\\W_]$'": "В логине допускаются только латинские буквы"
}


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    non_field_errors = []
    errors = []
    for error in exc.errors():
        print(error)

        if error["loc"] == ("body",):
            text = error["msg"].lstrip("Value error, ")
            non_field_errors.append(text)
        else:
            if "ctx" in error and isinstance(error["ctx"].get("error"), ValueError):
                errors.append(
                    FieldErrorSchema(
                        field=error["loc"][1], code=error["msg"].lstrip("Value error, ")
                    )
                )
            elif (
                "ctx" in error
                and error["ctx"].get("reason") in pydantic_errors_to_codes
            ):
                errors.append(
                    FieldErrorSchema(
                        field=error["loc"][1],
                        code=pydantic_errors_to_codes[error["ctx"].get("reason")],
                    )
                )
            elif error["msg"] in pydantic_errors_to_codes:
                errors.append(
                    FieldErrorSchema(
                        field=error["loc"][1],
                        code=pydantic_errors_to_codes[error["msg"]],
                    )
                )
            else:
                errors.append(
                    FieldErrorSchema(field=error["loc"][1], code=error["msg"])
                )

    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=APIExceptionSchema(
            non_field_errors=non_field_errors, errors=errors
        ).model_dump(),
    )


class UserWrongPassword(Exception):
    pass


class UserNotExists(Exception):
    pass
