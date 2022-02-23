from os.path import abspath, dirname, join
from typing import Optional

from pydantic import BaseSettings, Field


class CDKConfig(BaseSettings):
    ENV: str = Field(default="prod")
    AWS_REGION: str = Field(default="eu-west-1")
    AWS_ACCOUNT: str = Field(...)
    AWS_DOMAIN_NAME: Optional[str] = Field(None)
    AWS_API_SUBDOMAIN: Optional[str] = Field(None)
    AWS_COGNITO_SUBDOMAIN: Optional[str] = Field(None)

    class Config:
        env_prefix = ""
        case_sentive = False
        env_file = abspath(join(dirname(__file__), "..", "..", ".env"))
        env_file_encoding = "utf-8"


cfg = CDKConfig()
