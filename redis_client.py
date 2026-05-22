import redis
import os

try:
    redis_client = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6379)),
        decode_responses=False
    )

    redis_client.ping()
    print("Connected to Redis")

except:
    redis_client = None
    print("Redis not available")