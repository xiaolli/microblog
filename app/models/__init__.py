import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import os

sqlite_path = os.path.dirname(os.path.dirname(__file__))
sqlite = 'sqlite:///' + sqlite_path + '/microblog.db'
engine=sa.create_engine(sqlite)

DBSession = sessionmaker(engine)
session = DBSession()