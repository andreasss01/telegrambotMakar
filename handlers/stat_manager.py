from datetime import datetime

class StatManger:
    def __init__(self,db_instance):
        self.db = db_instance
        

    async def get_top_respect(self, limit=3):
        # Возвращает список: [(user_id, username, respect), ...]
        result = await self.db.get_top_respects(limit)
        if result:
            return result
        else:
            return f"Ошибка!"

    async def get_system_stats(self):
        # Возвращает: total_users, total_warns
        result = await self.db.get_system_stats()
        print(result)
        if result:
            return result
        else:
            return f"Ошибка!"
        
    async def format_stats_message(self,stats_data, top_respect):
        total_users = stats_data['total_users']
        total_warns = stats_data['total_warns'] 
        total_balance = stats_data['total_balance']
        
        # Формируем топ респектов
        top_respect_text = ""
        for i, (user_id, username, respect) in enumerate(top_respect, 1):
            top_respect_text += f"{i}. {username or 'Без username'} • {round(respect,2)} ⭐\n"
        
        message = (
            f"📊 <b>СТАТИСТИКА СИСТЕМЫ</b>\n"
            f"┌─────────────────\n"
            f"│ 👥 <b>Пользователей:</b> <code>{total_users}</code>\n"
            f"│ ⚠️  <b>Всего варнов:</b> <code>{total_warns}</code>\n"
            f"│ 💰 <b>Общий баланс:</b> <code>{total_balance}</code>\n"
            f"├─────────────────\n"
            f"│ 🏆 <b>ТОП ПО РЕСПЕКТАМ</b>\n"
            f"{top_respect_text}"
            f"└─────────────────\n"
            f"⏱ Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )
        
        return message
            

    