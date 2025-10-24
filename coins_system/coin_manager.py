import random

from datetime import datetime
from .config import FARM_COOLDOWN_HOURS,FARM_MAX_COINS,FARM_MIN_COINS

class CoinManager:
    def __init__(self, db):
        self.db = db
    
    async def can_farm(self, user_id: int) -> bool:
        last_farm_str = await self.db.get_last_farm_time(user_id)
        print(f"🔍 DEBUG can_farm: user_id={user_id}, last_farm_str={last_farm_str}")
        
        if last_farm_str is None:
            print("✅ DEBUG: Никогда не фармил - можно!")
            return True
        
        last_farm = datetime.fromisoformat(last_farm_str)
        now = datetime.now()
        hours_passed = (now - last_farm).total_seconds() / 3600
        print(f"🔍 DEBUG: hours_passed={hours_passed}, need={FARM_COOLDOWN_HOURS}")
        
        result = hours_passed >= FARM_COOLDOWN_HOURS
        print(f"🔍 DEBUG: can_farm result={result}")
        return result
        
    async def farm_coins(self, user_id: int) -> tuple[int, str]:
        if not await self.can_farm(user_id):
            last_farm = await self.db.get_last_farm_time(user_id)
            # Вычисляем когда можно снова фармить
            return 0, "❌ Фармить можно раз в 24 часа!"
        
        coins = random.randint(FARM_MIN_COINS, FARM_MAX_COINS)
        
        await self.db.update_user_balance(user_id, coins)
        await self.db.update_last_farm_time(user_id)
        return coins, f"✅Успешно\n Вы сфармили {coins} токс-коинов!"

    async def get_balance(self,user_id: int) -> int:
        balance = await self.db.get_user_balance(user_id)
        if balance:
            return balance
        else:
            return 0

    #async def exchange_respect_to_coins(self, user_id: int, respect_amount: float) -> bool:
        # обмен респектов на коины