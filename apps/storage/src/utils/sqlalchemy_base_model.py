from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SQLBaseModel(Base):
    def _fields(self):
        return {k: v for k, v in self.__dict__.items()}