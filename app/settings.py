from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    userid= ''
    passwd= ''
    dbname= 'clouds2024.db'
    dburl = ''
    sqlite_url = f'sqlite:///app/{dbname}'

config = Settings()