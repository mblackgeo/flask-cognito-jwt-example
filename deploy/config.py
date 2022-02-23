from typing import Optional

from pydantic import BaseSettings, Field


class Conf(BaseSettings):
    ENV: str = Field("prod")
    AWS_REGION: str = Field("eu-west-1")
    AWS_ACCOUNT: str = Field(...)
    AWS_DOMAIN_NAME: Optional[str] = Field(...)
    AWS_API_SUBDOMAIN: Optional[str] = Field(...)
    AWS_COGNITO_SUBDOMAIN: Optional[str] = Field(...)

    class Config:
        env_prefix = ""
        case_sentive = False
        env_file = "../.env"
        env_file_encoding = "utf-8"
