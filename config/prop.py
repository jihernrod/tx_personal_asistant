import os
from dataclasses import dataclass
from metaclases import Singleton as mtc

DEFAULT_MODEL = "gpt-4o-mini-2024-07-18"
CHAT_ID = "CHAT_ID"
API_TOKEN = "API_TOKEN"
API_KEY = "API_KEY"

@dataclass
class Secrets(metaclass=mtc.SingletonMeta):
    chat_id: int = int(os.getenv("CHAT_ID"))
    api_token: str = os.getenv("API_TOKEN")
    api_key: str = os.getenv("API_KEY")

@dataclass
class LLMModels(metaclass=mtc.SingletonMeta):
    default_model: str = DEFAULT_MODEL

def models():
    return LLMModels()

def secrets():
    return Secrets()

if __name__ == "__main__":
    secrets = Secrets()
    print(secrets.chat_id)
    print(secrets.api_token)
    print(secrets.api_key)

