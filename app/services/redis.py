from loader import redis_client


class Redis:
    redis_client = redis_client

    async def insert_value(self, value: str, user_id: str):
        return self.redis_client.set(f"manager_{user_id}", value)

    async def append_value(self, value: str, user_id: str):
        return self.redis_client.append(f"manager_{user_id}", f" {value}")

    async def get_value(self, user_id: str):
        return self.redis_client.get(f"manager_{user_id}").decode("utf-8").split()

    async def check_value(self, user_id: str):
        if self.redis_client.exists(f"manager_{user_id}"):
            return True

    async def remove_value(self, user_id: str):
        return self.redis_client.delete(f"manager_{user_id}")