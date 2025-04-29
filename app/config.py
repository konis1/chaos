from pydantic import BaseSettings


class Settings(BaseSettings):
    freshdesk_api_key: str
    freshdesk_domain: str
    gpt_model: str = "gpt-3.5-turbo"
    openai_api_key: str

    class Config():
        env_file = ".env"


settings = Settings()
