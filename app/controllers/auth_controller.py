from app.services.user_service import UserService
from app.exceptions import APIException

user_service = UserService()
class AuthController:

    def register_user(self, user_data):
        user = {
                "first_name": user_data.get("first_name", "").strip(),
                "last_name": user_data.get("last_name", "").strip(),
                "email": user_data.get("email", "").strip(),
                "password": user_data.get("password", ""),
                "confirm_password": user_data.get("confirm_password", ""), 
        }

        try:
            if user_service.is_valid_user(user, verify_email_exists=True):
                user_service.create_user(user)
                return { "message": "Usuário cadastrado com sucesso.", "status": 201 }

            return { "message": "Dados inválidos.", "status": 400 }

        except APIException as e:
            return { "message": f"{str(e)}", "status": e.status_code }

    def login_user(self, user_data):
        email = user_data.get("email", "").strip()
        password = user_data.get("password", "")

        try:
            user_service.authenticate_user(email, password)
            return { "message": "Usuário autenticado com sucesso.", "status": 200 }
        except APIException as e:
            return { "message": f"{str(e)}", "status": e.status_code }
