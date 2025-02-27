from app.services.user_service import UserService
from app.exceptions import APIException

userService = UserService()
class AuthController:
    def register_user(self, user_data):
        user = {
                "first_name": user_data.get("first_name", "").strip(),
                "last_name": user_data.get("last_name", "").strip(),
                "email": user_data.get("email", "").strip(),
                "password": user_data.get("password", ""),
                "confirm_password": user_data.get("confirm_password", ""), 
        }

        print(user)

        try:
            if userService.is_valid_user(user, verify_email_exists=True):
                userService.create_user(user)
                return { "message": "Usuário cadastrado com sucesso.", "status": 201 }
            return { "message": "Erro desconhecido.", "status": 500}
        except APIException as e:
            return { "message": f"{str(e)}", "status": e.status_code }
