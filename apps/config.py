from pydantic import BaseSettings

class Settings( BaseSettings):
    database_hostname: str = ""
    database_port: str = "localhost"

    database_name: str = ""    
    database_password: str = ""
    database_username: str = "postgres"

    algorithm : str = ""
    secret_key: str = "kjdfkjdlfkjldjfl49903"
    access_token_expire_minutes : int = 30


    class Config:
        env_file = ".env"

settings = Settings()