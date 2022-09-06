import environ
import secrets
import string

alphabet = string.ascii_letters + string.digits
password = ''.join(secrets.choice(alphabet) for i in range(20))

env = environ.Env()

REDIS_JWT_PASSWORD = env("REDIS_PASS", default=None)
REDIS_JWT_HOST = env("REDIS_HOST", default='redis')
REDIS_JWT_USERNAME = env("REDIS_USERNAME", default=None)
REDIS_JWT_DB = env('REDIS_DB', default=0)
SECRET_KEY = password
