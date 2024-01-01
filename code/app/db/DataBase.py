from sys import modules

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import NullPool, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import *


# def create_test_db():
#
#     if os.environ.get("ENV") != "test":
#
#         raise "the connection is test"
#
#         conn = psycopg2.connect(
#             host=TEST_DB_HOST,
#             user=TEST_DB_USER,
#             password=TEST_DB_PASSWORD,
#             dbname="postgres"
#         )
#         conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#         cur = conn.cursor()
#
#         cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
#
#         cur.execute(f"CREATE DATABASE {TEST_DB_NAME}")
#
#         cur.close()
#         conn.close()


DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
# if "pytest" in modules:
#     DATABASE_URI = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"

engine = create_engine(
    DATABASE_URI,
    echo=False,
    future=True,
    poolclass=NullPool
)

# if os.environ.get("ENV") == "test":
#     create_test_db()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


Base = declarative_base()

