import os

DB_HOSTNAME = os.environ.get("DB_HOSTNAME", "ismart-db")
DB_USER = os.environ.get("DB_USER", "ismart")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "ismart")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "ismart")
