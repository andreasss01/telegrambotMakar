from .role_config import BASE_ROLE, Role

class RoleManager:
    def __init__(self, db_instance):
        self.db = db_instance

    async def get_role_by_respect(self, respect: float) -> Role:
        for role in sorted(BASE_ROLE, key=lambda x: x.threshold, reverse=True):
            if respect >= role.threshold:
                return role
        return BASE_ROLE[0]  # роль по умолчанию
    
    async def set_user_role (self,user_id: int, new_role: str):
        current_role = await self.db.get_user_role(user_id)
        roles_names = [role.name for role in BASE_ROLE]
        if new_role not in roles_names:
            return "❌ Данной роли, нет в списке ролей!"
        if current_role == new_role:
            return f"❌ Текущая роль уже = {new_role}"
        
        await self.db.set_user_role(user_id, new_role)
        return f"✅ Успешно! \nУ пользователя: {user_id} теперь роль: {new_role}"