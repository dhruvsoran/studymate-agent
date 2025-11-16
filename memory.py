USER_MEMORY = {}

def create_user(user_id, profile):
    USER_MEMORY[user_id] = profile

def get_user_profile(user_id):
    return USER_MEMORY.get(user_id, {})
