from typing import Any, Optional

import jwt
from fastapi import status
from fastapi_users import exceptions
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.jwt import SecretType, decode_jwt, generate_jwt
from fastapi_users.openapi import OpenAPIResponseType

from app.config import settings
from app.models.user import User
from app.schemas.auth import BearerResponse, RefreshResponse
from app.users.manager import UserManager


class RefreshableJWTStrategy(JWTStrategy):
    """
    JWT strategy that enables refresh tokens
    """

    def __init__(
        self,
        secret: SecretType,
        access_lifetime_seconds: Optional[int],
        refresh_lifetime_seconds: Optional[int],
        token_audience: list[str] = ["fastapi-users:auth"],
        algorithm: str = "HS256",
        public_key: Optional[SecretType] = None,
    ):
        super().__init__(
            secret, access_lifetime_seconds, token_audience, algorithm, public_key
        )
        self.refresh_lifetime_seconds = refresh_lifetime_seconds

    async def write_access_token(self, user: User) -> str:
        data = {
            "sub": str(user.id),
            "aud": self.token_audience,
            "token_type": "access",
        }
        return generate_jwt(
            data, self.encode_key, self.lifetime_seconds, algorithm=self.algorithm
        )

    async def write_refresh_token(self, user: User) -> str:
        data = {
            "sub": str(user.id),
            "aud": self.token_audience,
            "token_type": "refresh",
        }
        return generate_jwt(
            data,
            self.encode_key,
            self.refresh_lifetime_seconds,
            algorithm=self.algorithm,
        )

    async def read_token(
        self, token: Optional[str], user_manager: UserManager
    ) -> User | None:
        if token is None:
            return None

        try:
            data = decode_jwt(
                token, self.decode_key, self.token_audience, algorithms=[self.algorithm]
            )
            user_id = data.get("sub")
            if user_id is None:
                return None
        except jwt.PyJWTError:
            return None

        try:
            parsed_id = user_manager.parse_id(user_id)
            return await user_manager.get(
                parsed_id
            )
        except exceptions.InvalidID:
            return None


def get_jwt_strategy() -> RefreshableJWTStrategy:
    return RefreshableJWTStrategy(
        secret=settings.SECRET_KEY,
        access_lifetime_seconds=settings.ACCESS_LIFETIME_SECONDS,
        refresh_lifetime_seconds=settings.REFRESH_LIFETIME_SECONDS,
    )


class RefreshableBearerTransport(BearerTransport):
    @staticmethod
    def get_openapi_login_responses_success() -> OpenAPIResponseType:
        return {
            status.HTTP_200_OK: {
                "model": BearerResponse,
                "content": {
                    "application/json": {
                        "example": {
                            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1"
                            "c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2Z"
                            "DMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS"
                            "11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ."
                            "M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
                            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1"
                            "c2VyX2lkIjoiZTZjODk4NDktYzgxYy00N2FmLWE2OTEtOTIxYTQ2MzBmZj"
                            "Q5IiwiYXVkIjpbImZhc3RhcGktdXNlcnM6YXV0aCJdLCJ0b2tlbl90eXBl"
                            "jIoicmVmcmVzaCIsImV4cCI6MTY3NDgyOTk2N30.lCZKSuHzlU__C9q9"
                            "1TFv7f8gRIAO26iu4JDUoVv9r10",
                            "token_type": "bearer",
                        }
                    }
                },
            },
        }


class RefreshableAuthenticationBackend(AuthenticationBackend):
    async def login(
        self,
        strategy: RefreshableJWTStrategy,
        user: User,
    ) -> Any:
        access_token = await strategy.write_access_token(user)
        refresh_token = await strategy.write_refresh_token(user)

        login_response = BearerResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

        return login_response

    async def refresh(
        self,
        strategy: RefreshableJWTStrategy,
        user: User,
    ) -> Any:
        access_token = await strategy.write_access_token(user)
        login_response = RefreshResponse(
            access_token=access_token,
            token_type="bearer",
        )
        return login_response


bearer_transport = RefreshableBearerTransport(tokenUrl="auth/jwt/login")

auth_backend = RefreshableAuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
