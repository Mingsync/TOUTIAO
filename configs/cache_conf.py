import json

import redis.asyncio as redis


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0
# 创建 Redis 连接
redis_client = redis.Redis(host=REDIS_HOST, # Redis 服务器地址
                            port = REDIS_PORT, # Redis 服务器端口
                            db=REDIS_DB,  # 使用默认数据库0
                            decode_responses=True # 将 Redis 存储的字节数据解码为字符串
                            )


# 读取字符串
async def get_cache(key: str):
    try:
        value = await redis_client.get(key)
        return value
    except Exception as e:
        print(f"Error getting cache for key {key}: {e}")
        return None
    

# 读取列表或字典
async def get_json_cache(key: str):
    try:
        value = await redis_client.get(key)
        if value is not None:
            return json.loads(value)  # 将JSON字符串转换回列表或字典
        return None
    except Exception as e:
        print(f"Error getting JSON cache for key {key}: {e}")
        return None
    
# 设置缓存
async def set_cache(key:str, value, expire: int = 3600):
    try:
        if isinstance(value, (list, dict)):
            # value = str(value) # 将列表或字典转换为字符串存储
            value = json.dumps(value, ensure_ascii=False) # 将列表或字典转换为JSON字符串存储,并保持中文字符不被转义
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"Error setting cache for key {key}: {e}")
        return False
    