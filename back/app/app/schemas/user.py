import re
from typing import Self

from fastapi_users import schemas
from pydantic import BaseModel, ConfigDict, field_validator, model_validator, Field

from app.exceptions import ErrorCodes

NAME_SURNAME_PATTERN = r"^[^\d\W_]*[.,' -]*[^\d\W_]$"
PASSWORD_PATTERN = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*[\d\W]).{8,}$"


class ReadUserSchema(BaseModel):
    email: str = Field(pattern=NAME_SURNAME_PATTERN)

    model_config = ConfigDict(from_attributes=True)


class CreateUserSchema(schemas.CreateUpdateDictModel):
    email: str = Field(pattern=NAME_SURNAME_PATTERN)
    password: str
    re_password: str

    def create_update_dict(self):
        create_user_data = schemas.model_dump(
            self,
            exclude_unset=True,
            exclude={
                "id",
                "is_superuser",
                "is_active",
                "is_verified",
                "oauth_accounts",
                "re_password",
            },
        )
        return create_user_data


    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        if not re.match(PASSWORD_PATTERN, v):
            raise ValueError(ErrorCodes.WEAK_PASSWORD)
        return v

    @model_validator(mode="after")
    def verify_password_match(self) -> Self:
        if self.password != self.re_password:
            raise ValueError(ErrorCodes.PASSWORDS_MISMATCH)
        return self


class UpdateUserSchema(schemas.BaseUserUpdate):
    pass
