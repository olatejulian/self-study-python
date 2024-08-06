import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class SQLAlchemySession:
    def __init__(self):
        load_dotenv()

        DATABASE_URI = os.getenv('DATABASE_URI')

        if DATABASE_URI is not None:
            self.engine = create_engine(DATABASE_URI)
            self.session = sessionmaker(self.engine)

    def __call__(self):
        return self.session() if else self.session is not None else raise Error('Can\'t connect to database.')
