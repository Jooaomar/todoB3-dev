"""
Aqui definimos uma base do banco de dados SQLite3 e uma sessão.

A partir de agora, quando mexer no banco de dados, você importará esse arquivo e fará uma sessão. """

from multiprocessing.forkserver import connect_to_new_process
from sqlite3 import connect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

# Para desenvolvimento usando postgres
# DB_HOST = 'localhost'
# DB_DATABASE = 'yourdbname'
# DB_USER = 'postgres'
# DB_PASSWORD = 'postgres'
# RDB_PATH = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_DATABASE}'

# Para desenvolvimento usando sqlite
RDB_PATH = "sqlite:///./sql_app.db"


# Produção usando postgresql
# RDB_PATH = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_DATABASE}"

ECHO_LOG = True
 
engine = create_engine(
  RDB_PATH, echo=ECHO_LOG, connect_args={"check_same_thread": False}
)
 
Session = sessionmaker(bind=engine)
session = Session()