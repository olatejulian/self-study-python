from pydantic import  BaseModel, SecretStr

class BaseSchema(BaseModel):
    def _fields(self):
        return {k: v.get_secret_value() if type(v) == SecretStr else v for k, v in self.__dict__.items() if v is not None}

    class Config:
        orm_mode = True
