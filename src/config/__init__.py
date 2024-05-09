import os

class Config:
    def __init__(self) -> None:
        self.POSTGRES_DB_SCHEMA = self._read_env("POSTGRES_DB_SCHEMA")
        self.POSTGRES_DB = self._read_env("POSTGRES_DB")
        self.POSTGRES_HOST = self._read_env("POSTGRES_HOST")
        self.POSTGRES_USER = self._read_env("POSTGRES_USER")
        self.POSTGRES_PASSWORD = self._read_env("POSTGRES_PASSWORD")
        self.TABLE_NAME_BUILDINGS = self._read_env("TABLE_NAME_BUILDINGS")
        self.TABLE_NAME_FLOORS = self._read_env("TABLE_NAME_FLOORS")
        self.TABLE_NAME_WALLS = self._read_env("TABLE_NAME_WALLS")
        self.TABLE_NAME_DOC_DOORS= self._read_env("TABLE_NAME_DOC_DOORS")
        self.TABLE_NAME_FURNITURE = self._read_env("TABLE_NAME_FURNITURE")

    def _read_env(self, key, nullable = False):
        val = os.environ.get(key, None)
        if not nullable and val is None:
            raise ValueError(f"export env {key} before running application")
        return val
        
APP_CONFIG = Config()