import environ
import dj_database_url

env = environ.Env()
environ.Env.read_env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

DATABASES = {"default": dj_database_url.config(default=env("DATABASE_URL"))}
