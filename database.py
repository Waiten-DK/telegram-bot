"""
Работа с базой данных анкет
"""
import json
import os
from typing import List, Dict, Optional


class Database:
    def __init__(self, filepath: str = "data/profiles.json"):
        self.filepath = filepath
        self.profiles = []
        self.favorites = {}  # user_id: [profile_ids]
        self._ensure_data_dir()
        self.load_profiles()
    
    def _ensure_data_dir(self):
        """Создание директории для данных"""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
    
    def load_profiles(self):
        """Загрузка анкет из файла"""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.profiles = data.get('profiles', [])
                    self.favorites = data.get('favorites', {})
            except Exception as e:
                print(f"Ошибка загрузки данных: {e}")
                self.profiles = []
                self.favorites = {}
        else:
            # Создание примера данных
            self._create_sample_data()
    
    def _create_sample_data(self):
        """Создание примера анкет"""
        self.profiles = [
            {
                "id": 0,
                "name": "Анна",
                "city": "Москва",
                "age": 22,
                "height": 175,
                "weight": 55,
                "appearance": "Блондинка, голубые глаза",
                "phone": "+79099999999",
                "telegram": "anna_model",
                "photos": [
                    "https://via.placeholder.com/600x800/FF6B9D/ffffff?text=Anna+1",
                    "https://via.placeholder.com/600x800/C44569/ffffff?text=Anna+2",
                    "https://via.placeholder.com/600x800/FF6B9D/ffffff?text=Anna+3"
                ]
            },
            {
                "id": 1,
                "name": "Мария",
                "city": "Санкт-Петербург",
                "age": 24,
                "height": 168,
                "weight": 52,
                "appearance": "Брюнетка, карие глаза",
                "phone": "+79099999998",
                "telegram": "maria_model",
                "photos": [
                    "https://via.placeholder.com/600x800/6C5CE7/ffffff?text=Maria+1",
                    "https://via.placeholder.com/600x800/A29BFE/ffffff?text=Maria+2"
                ]
            },
            {
                "id": 2,
                "name": "Виктория",
                "city": "Казань",
                "age": 21,
                "height": 172,
                "weight": 54,
                "appearance": "Шатенка, зелёные глаза",
                "phone": "+79099999997",
                "telegram": "vika_model",
                "photos": [
                    "https://via.placeholder.com/600x800/00B894/ffffff?text=Vika+1",
                    "https://via.placeholder.com/600x800/00CEC9/ffffff?text=Vika+2",
                    "https://via.placeholder.com/600x800/00B894/ffffff?text=Vika+3",
                    "https://via.placeholder.com/600x800/00CEC9/ffffff?text=Vika+4"
                ]
            }
        ]
        self.save_profiles()
    
    def save_profiles(self):
        """Сохранение анкет в файл"""
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'profiles': self.profiles,
                    'favorites': self.favorites
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")
    
    def get_profile(self, profile_id: int) -> Optional[Dict]:
        """Получение анкеты по ID"""
        if 0 <= profile_id < len(self.profiles):
            return self.profiles[profile_id]
        return None
    
    def get_all_profiles(self) -> List[Dict]:
        """Получение всех анкет"""
        return self.profiles
    
    def get_total_profiles(self) -> int:
        """Количество анкет"""
        return len(self.profiles)
    
    def add_to_favorites(self, user_id: int, profile_id: int):
        """Добавление в избранное"""
        user_id_str = str(user_id)
        if user_id_str not in self.favorites:
            self.favorites[user_id_str] = []
        
        if profile_id not in self.favorites[user_id_str]:
            self.favorites[user_id_str].append(profile_id)
            self.save_profiles()
    
    def remove_from_favorites(self, user_id: int, profile_id: int):
        """Удаление из избранного"""
        user_id_str = str(user_id)
        if user_id_str in self.favorites and profile_id in self.favorites[user_id_str]:
            self.favorites[user_id_str].remove(profile_id)
            self.save_profiles()
    
    def is_favorite(self, user_id: int, profile_id: int) -> bool:
        """Проверка, в избранном ли анкета"""
        user_id_str = str(user_id)
        return user_id_str in self.favorites and profile_id in self.favorites[user_id_str]
    
    def get_user_favorites(self, user_id: int) -> List[Dict]:
        """Получение избранных анкет пользователя"""
        user_id_str = str(user_id)
        if user_id_str not in self.favorites:
            return []
        
        favorite_profiles = []
        for profile_id in self.favorites[user_id_str]:
            profile = self.get_profile(profile_id)
            if profile:
                favorite_profiles.append(profile)
        
        return favorite_profiles


# Глобальный экземпляр базы данных
db = Database()
