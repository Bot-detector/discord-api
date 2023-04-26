from pydantic import BaseSettings, Field
import os


class Config(BaseSettings):
    MYSQL_URL: str
    BEARER: str
    RELEASE_VERSION: str = "0.1"
    SECRETS: list = []

    def __init__(self, **data):
        data["SECRETS"] = [
            data["MYSQL_URL"],
            data["BEARER"],
        ]
        super().__init__(**data)


CONFIG: Config = Config(
    RELEASE_VERSION="0.1",
    MYSQL_URL=os.environ.get("SQL_URI"),
    BEARER=os.environ.get("BEARER")
)
