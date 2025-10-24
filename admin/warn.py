from .mute_manager import mute_user


class WarnManager:
    def __init__(self,db_instance):
        self.db = db_instance
        self.WARNS_FOR_MUTE = 4 # КОЛИЧЕСТВО ВАРНОВ НУЖНОЕ ДЛЯ АВТОМУТА
        self.TIME_FOR_MUTE = 1 # КОЛ-ВО ЧАСОВ МУТА
        

    async def add_warn(self, user_id, admin_id, reason, username,chat_id):
        if not await self.db.is_admin(admin_id):
            return "❌ Не админ!"
        
        if not reason:
            return "❌ Нет причины!"
        
        await self.db.add_warn(user_id, admin_id, reason)
        _, warns_count = await self.db.get_user_warns(user_id)
        if warns_count >= self.WARNS_FOR_MUTE:
            mut_result = await mute_user(chat_id,user_id,self.TIME_FOR_MUTE,"м","[AdminSystem] Автомут","System",username)
            if mut_result:
                return mut_result
        else:
            return f"✅ Варн выдан {username}\nВсего варнов: {warns_count}"



            

