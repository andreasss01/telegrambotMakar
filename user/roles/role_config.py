from dataclasses import dataclass

@dataclass
class Role:
    name: str           # название
    threshold: float    # порог респектов
    description: str    # описание       
    
# Создаём объекты ролей
BASE_ROLE = [
    Role("Бродяга", 10.0, "Почти свой"),
    Role("Свояк", 50.0, "Полностью свой"),
    Role("LEGENDARY", 100.0, "Легенда")
]

