import re
from flask_bcrypt import Bcrypt
from app.models import db, User
from app.exceptions import APIException

bcrypt = Bcrypt()

class UserService:

    def authenticate_user(self, email, password):
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        raise APIException("Credenciais inválidas.", 401)

    def verify_is_valid_name(self, name, field="Nome"):
        invalid_chars_pattern = r"[^a-zA-ZàáâãéêíóôõúÀÁÂÃÉÊÍÓÔÕÚçÇ\s']"
        if re.search(invalid_chars_pattern, name):
            raise ValueError(f"O {field} contém caracteres inválidos")
        invalid_chars_position_or_combination_pattern = r"\s{2,}|'{2,}|^\s+|^'"
        if re.search(invalid_chars_position_or_combination_pattern, name):
            raise ValueError(f"O {field} contém posição ou combinação inválida de caracteres.")
        if (not name) or (len(name) < 2 or len(name) > 100):
            raise ValueError(f"O {field} deve ter entre 2 e 100 caracteres.")
        return True

    def verify_is_valid_email(self, email):
        email_pattern = r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z]{2,})+$"
        if ((not email) or len(email) > 120) or (not re.fullmatch(email_pattern, email)):
            raise ValueError("Email inválido.")
        return True

    def is_email_registered(self, email):
        if User.query.filter_by(email=email).first() is None:
            return False
        return True

    def verify_is_valid_password(self, password):
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&\.])[A-Za-z\d@$!%*?&\.]{8,}$"
        if not re.fullmatch(password_pattern, password):
            raise ValueError("A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula, uma minúscula, um número e um caractere especial (@$!%*?&.).")
        return True

    def is_valid_user(self, user, verify_email_exists=False):
        try:
            if "first_name" in user:
                self.verify_is_valid_name(user["first_name"], "nome")
            if "last_name" in user:
                self.verify_is_valid_name(user["last_name"], "sobrenome")
            if "email" in user:
                self.verify_is_valid_email(user["email"])
                if (verify_email_exists and self.is_email_registered(user["email"])):
                    raise ValueError("Email já registrado.")
            if "password" in user:
                self.verify_is_valid_password(user["password"])
                if "confirm_password" in user and (user["password"] != user["confirm_password"]):
                    raise ValueError("As senhas não coincidem.")
            return True
        except Exception as e:
            raise APIException(f"{str(e)}", 400) from e



    def create_user(self, user):
        new_user = User(first_name=user["first_name"], last_name=user["last_name"], email=user["email"])
        new_user.set_password(user["password"])

        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user.id
        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro ao cadastrar usuário", 500) from e
