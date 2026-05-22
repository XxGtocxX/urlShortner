import redis

redis_client = None

try:
    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )

    redis_client.ping()

except:
    print("Redis not available")