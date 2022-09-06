import redis
import settings
import jwt


payload_data = {
  "user_id": 1,
  "username": "test@testing.redis.com",
  "exp": 1234567891,
  "email": "test@testing.redis.com",
  "orig_iat": 1234567891
}

secret_key = settings.SECRET_KEY


def get_redis_for_jwt() -> redis.Redis:
    """
    Returns a Redis instance set up for JWT token validation
    """
    return redis.Redis(
        host=settings.REDIS_JWT_HOST,
        password=settings.REDIS_JWT_PASSWORD,
        username=settings.REDIS_JWT_USERNAME,
        db=settings.REDIS_JWT_DB
    )


def invalidate_token(token, username):
    """
    Store the token hash in Redis to invalidate it and avoid usage for future calls
    """
    try:
        jwt_hash = token.decode().split('.')[2]
        redis_instance = get_redis_for_jwt()
        # Saving Token HASH
        redis_instance.set(jwt_hash, username, ex=300)
    except Exception as ex:
        print(ex.__str__())

def is_jwt_hash_invalid(token: str) -> bool:
    """
    This method match the Hash of a JWT with the cache provided on Redis.
    Returns:
        True if Token is invalid. It raises an Error if Token couldn't be validated
    :param token: JSON Web Token
    """
    redis_instance = None
    error_redis_message = 'Error reaching redis instance while validating jwt hash'
    try:
        redis_instance = get_redis_for_jwt()
    except Exception as e:
        print(error_redis_message)
        raise ConnectionError(error_redis_message)

    jwt_token = token.decode().split('.') if token else []
    if len(jwt_token) != 3:
        raise ValueError('Invalid token format')

    jwt_hash = jwt_token[2]
    print('Token hash --> ' + jwt_hash)
    try:
        redis_key_exists = bool(redis_instance.exists(jwt_hash))
    except Exception as e:
        print(error_redis_message)
        raise ConnectionError(error_redis_message)
    return redis_key_exists

if __name__ == '__main__':
    token = jwt.encode(payload_data, secret_key, algorithm='HS256')
    print("Testing Redis \n================= \nTesting connection and invalidating token...")
    invalidate_token(token, payload_data['username'])
    print("Token invalidated. Testing retrieval of hash from Redis...")
    key_exists = is_jwt_hash_invalid(token)
    print(f"Key exists (token is invalid): {key_exists}")
