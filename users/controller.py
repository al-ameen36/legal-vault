from db import db


class User:
    def get_user(self, user_id: int):
        response = db.table("users").select("*").eq("id", user_id).execute()
        return response

    def get_chat_history(self, user_id: int):
        response = db.table("chat").select("*").eq("user", user_id).execute()
        return response

    def clear_chat_history(self, user_id: int):
        response = db.table("chat").delete().eq("user", user_id).execute()
        return response

    def save_message(self, user_id: int, message: str, role: str):
        response = (
            db.table("chat")
            .insert({"message": message, "role": role, "user": user_id})
            .execute()
        )
        return response
