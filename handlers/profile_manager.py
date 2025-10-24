from datetime import datetime

class ProfileManager:
    def __init__(self, db_instance):
        self.db = db_instance
        self.role_emojis = {
            "Участник": "👤",
            "Бродяга": "🦊", 
            "Свояк": "🐺",
            "LEGENDARY": "🐉",
            "Администратор": "👮"
        }

    async def get_full_profile(self, user_id: int) -> str:
        """Получить готовый профиль пользователя"""
        user_data = await self.db.get_user_info(user_id)
        if not user_data:
            return "❌ Пользователь не найден"
        
        warns_data = await self.db.get_user_warns(user_id)
        balance = await self.db.get_user_balance(user_id) or 0
        days_in_system = await self._get_days_in_system(user_data['join_date'])
        warns_count = warns_data[1] if warns_data else 0
        
        return self._format_profile(user_data, balance, warns_count, days_in_system)

    async def _get_days_in_system(self, join_date_str: str) -> int:
        """Получить количество дней в системе"""
        join_date = datetime.fromisoformat(join_date_str)
        return (datetime.now() - join_date).days

    def _format_profile(self, user_data: dict, balance: int, warns_count: int, days: int) -> str:
        """Форматировать профиль в красивый текст"""
        role_emoji = self.role_emojis.get(user_data['role'], '👤')
        
        return (
            f"🎖 <b>ПРОФИЛЬ СОЛДАТА</b>\n"
            f"┌─────────────────\n"
            f"│ 🔹 <b>ID:</b> <code>{user_data['user_id']}</code>\n"
            f"│ 🔹 <b>Роль:</b> {user_data['role']} {role_emoji}\n"
            f"│ 🔹 <b>Респекты:</b> <b>{user_data['respects']:.2f}</b> ⭐\n"
            f"├─────────────────\n"
            f"│ 💰 <b>Токс-коины:</b> <code>{balance}</code> 🪙\n"
            f"│ ⚠️  <b>Варны:</b> <code>{warns_count}/3</code>\n"
            f"│ 📅 <b>В системе:</b> {days} дней\n"
            f"└─────────────────"
        )