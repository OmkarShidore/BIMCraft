import os

class Config:
    def __init__(self) -> None:
        self.ENV = self._read_env("ENV")
        self.PORT = self._read_env("PORT")
        
        self.DB_NAME = self._read_env("DB_NAME")
        self.DB_SCHEMA = self._read_env("DB_SCHEMA")
        self.DB_HOST = self._read_env("DB_HOST")
        self.DB_USER = self._read_env("DB_USER")
        self.DB_PASSWORD = self._read_env("DB_PASSWORD")
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