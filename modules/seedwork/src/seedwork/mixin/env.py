import dotenv
import os


class EnvMixin:
    def __init__(self):
        dotenv.load_dotenv()

        for key, _type in self.__annotations__.items():
            value = self.getenv(key.upper())

            if not value:
                raise ValueError(f"Missing environment variable: {key.upper()}")

            if not isinstance(value, _type):
                raise TypeError(f"Invalid type for environment variable: {key.upper()}")

            setattr(self, key, value)

    def getenv(self, key):
        return os.getenv(key)
