from app.services.user_service import UserService
from app.exceptions import APIException

user_service = UserService()

class UserController:
    def get_user_profile(self, user_id):
        try:
            user = user_service.get_user_by_id(user_id)
            user_profile = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "photo": user.photo,
            }

            return { "message": "Perfil encontrado", "data": user_profile, "status": 200}

        except APIException as e:
            return {"message": str(e), "status": e.status_code}


    def change_user_personal_info(self, user_id, user_data):
        try:
            user = {
                "first_name":  user_data.get("first_name", "").strip(),
                "last_name": user_data.get("last_name", "").strip(),
                "email": user_data.get("email", "").strip(),
            }

            if user_data["photo"]:
                user["photo"] = user_data["photo"]

            user_data = user

            if user_service.is_valid_user(user):
                response = user_service.update_user_personal_info(user_id, user_data)

                return {
                    "message": "Informações alteradas com sucesso!", 
                    "status": 200, 
                    "keep_logged": response["keep_logged"] 
                }

            return { "message": "Dados inválidos.", "status": 400 }

        except APIException as e:
            return { "message": str(e), "status": e.status_code }



    def change_user_password(self, user_id, password_data):
        try:
            password_data = {
                "current_password": password_data.get("current_password"),
                "new_password": password_data.get("new_password"),
                "confirm_new_password": password_data.get("confirm_new_password")
            }

            user_service.update_user_password(user_id, password_data)

            return { "message": "Senha alterada com sucesso", "status": 200 }

        except APIException as e:
            return {"message": str(e), "status": e.status_code}
