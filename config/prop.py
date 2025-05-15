import os
from dataclasses import dataclass
from metaclases import Singleton as mtc

@dataclass
class Secrets(metaclass=mtc.SingletonMeta):
    chat_id: int = int(os.getenv("CHAT_ID"))
    api_token: str = os.getenv("API_TOKEN")
    api_key: str = os.getenv("API_KEY")


def secrets():
    return Secrets()

if __name__ == "__main__":
    secrets = Secrets()
    print(secrets.chat_id)
    print(secrets.api_token)
    print(secrets.api_key)

