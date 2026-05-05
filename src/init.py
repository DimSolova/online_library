from src.config import setting
from src.connectors.redis_connector import RedisManager

redis_manager = RedisManager(
    host=setting.REDIS_HOST,
    port=setting.REDIS_PORT,
)
