from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get('DATABASE_HOST')
DB_PORT = os.environ.get('DATABASE_PORT')
DB_NAME = os.environ.get('DATABASE_NAME')
DB_USER = os.environ.get('DATABASE_USER')
DB_PASSWORD = os.environ.get('DATABASE_PASSWORD')

TEST_DB_HOST = os.environ.get('TEST_DATABASE_HOST')
TEST_DB_PORT = os.environ.get('TEST_DATABASE_PORT')
TEST_DB_NAME = os.environ.get('TEST_DATABASE_NAME')
TEST_DB_USER = os.environ.get('TEST_DATABASE_USER')
TEST_DB_PASSWORD = os.environ.get('TEST_DATABASE_PASSWORD')

SECRET_KEY = os.environ.get('SECRET_KEY')

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

