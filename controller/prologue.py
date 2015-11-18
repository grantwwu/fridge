from contextlib import contextmanager
import getpass

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

psql_engine = create_engine('postgresql://' + getpass.getuser() + ':15291@localhost/main')
session_factory = sessionmaker(bind=psql_engine)
Session = scoped_session(session_factory)

@contextmanager
def makeSession():
    dbSession = Session()
    try:
        yield dbSession
    finally:
        dbSession.close()

Base = declarative_base()

def defer_create():
    Base.metadata.create_all(psql_engine)
