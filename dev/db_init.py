import redis

# Инициализация Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


# Хранение пользователей в памяти
users_db = {}