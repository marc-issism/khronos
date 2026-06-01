from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./khronos.db" #TODO: Swap to postgres

# DATABASE = 'postgresql'
# USER = 'postgres'
# PASSWORD = 'your password'
# HOST = 'localhost'
# PORT = '5432'
# DB_NAME = 'postgres'
# engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME }')


engine = create_engine(
  SQLALCHEMY_DATABASE_URL,
  connect_args={"check_same_thread": False} #TODO: for sqlite only
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# session = transaction with database, autocommit and autoflush = False allow US to control when changes happen

class Base(DeclarativeBase):
  pass


def get_db():
  with SessionLocal() as db: 
    yield db # gives this route a database session