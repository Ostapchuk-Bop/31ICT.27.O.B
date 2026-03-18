from app.db.fake_db import fake_users_db

def get_all_users():
    return fake_users_db

def get_user(user_id: int):
    return fake_users_db.get(user_id)

def create_user(user_id: int, user_data: dict):
    fake_users_db[user_id] = user_data
    return fake_users_db[user_id]

def update_user(user_id: int, user_data: dict):
    if user_id in fake_users_db:
        fake_users_db[user_id].update(user_data)
        return fake_users_db[user_id]
    return None

def delete_user(user_id: int):
    return fake_users_db.pop(user_id, None)