import re
import os
from pathlib import Path
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user
from flask_bcrypt import Bcrypt
from app.models import db, User
from app.exceptions import APIException
from app.utils.random_str import str_rand

bcrypt = Bcrypt()

class UserService:

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


    def verify_is_valid_photo(self, photo_file):
        try:
            valid_types = {"image/jpeg", "image/png", "image/webp", "image/svg+xml"}
            max_size = 5 * 1024 * 1024


            if not photo_file:
                raise ValueError("Problema ao carregar a foto de perfil.")


            filename = secure_filename(photo_file.filename)
            if filename == "":
                raise ValueError("Nome inválido para foto de perfil.")


            mime_type = photo_file.mimetype
            if mime_type not in valid_types:
                raise ValueError("Tipo de arquivo inválido para foto de perfil.")


            photo_file.seek(0, os.SEEK_END)
            file_size = photo_file.tell()
            photo_file.seek(0)

            if file_size > max_size:
                raise ValueError("Tamanho máximo de 5MB excedido para foto de perfil.")

            return True
        except Exception as e:
            raise ValueError(f"{str(e)}") from e


    def save_photo(self, photo_file):
        try:
            if photo_file is None:
                return None

            extension_for_each_type = {"image/jpeg": "jpeg", "image/png": "png", "image/webp": "webp", "image/svg+xml": "svg"}
            photo_filename = f"{str_rand(64)}.{extension_for_each_type[photo_file.mimetype]}"
            upload_folder = "uploads/profiles"
            os.makedirs(upload_folder, exist_ok=True)
            upload_path = os.path.join(upload_folder, photo_filename)
            photo_file.save(upload_path)

            return photo_filename

        except Exception as e:
            raise ValueError("Erro ao salvar foto de perfil") from e


    def delete_photo(self, photo_path):
        path = Path(photo_path)

        if path.exists():
            return path.unlink()
        return None


    def is_email_registered(self, email):
        if User.query.filter_by(email=email).first() is None:
            return False

        return True


    def verify_is_valid_password(self, password, label="senha"):
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&\.])[A-Za-z\d@$!%*?&\.]{8,}$"

        if not re.fullmatch(password_pattern, password):
            raise ValueError(f"A {label} deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula, uma minúscula, um número e um caractere especial (@$!%*?&.).")

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
                    raise ValueError("Verifique a confirmação de senha. As senhas não coincidem.")

            if "photo" in user:
                self.verify_is_valid_photo(user["photo"])

            return True

        except Exception as e:
            raise APIException(f"{str(e)}", 400) from e


    def get_user_by_id(self, user_id):
        try:
            user = User.query.get(user_id)
            if user:
                return user
            raise APIException("Usuário não encontrado", 404)

        except APIException as e:
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            raise APIException ("Erro desconhecido", 500) from e


    def authenticate_user(self, email, password):
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return user.to_dict()

        raise APIException("Credenciais inválidas.", 401)


    def logout_user(self):
        return logout_user()


    def create_user(self, user):
        new_user = User(first_name=user["first_name"], last_name=user["last_name"], email=user["email"])
        new_user.set_password(user["password"])

        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user.id

        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro desconhecido", 500) from e


    def update_user_personal_info(self, user_id, user_data):
        try:
            user = self.get_user_by_id(user_id)

            if user:

                has_changed_email = user_data["email"] != user.email
                has_changed_photo = user_data.get("photo", None) is not None


                equal_fields = (
                    (not has_changed_photo)
                    and (not has_changed_email)
                    and (user_data["first_name"] == user.first_name)
                    and (user_data["last_name"] == user.last_name)
                )


                if equal_fields:
                    raise APIException("Nenhuma alteração foi detectada", 400)

                photo_filename = self.save_photo(user_data["photo"]) if has_changed_photo else None

                user.first_name = user_data["first_name"]
                user.last_name = user_data["last_name"]
                user.email = user_data["email"]

                last_photo_path = os.path.join("uploads/profiles", user.photo)
                user.photo = user.photo if photo_filename is None else photo_filename

                if has_changed_photo:
                    self.delete_photo(last_photo_path)

                db.session.commit()

                return { "keep_logged": not has_changed_email, "updated_user": user.to_dict }

            raise APIException("Usuário não encontrado", 404)

        except APIException as e:
            db.session.rollback()
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro desconhecido", 500) from e


    def update_user_password(self, user_id, password_data):
        try:
            user = self.get_user_by_id(user_id)

            if not user:
                raise APIException("Usuário não encontrado", 404)

            if password_data["current_password"] == "":
                raise APIException("Informe a senha atual", 400)

            if not bcrypt.check_password_hash(user.password, password_data["current_password"]):
                raise APIException("Senha atual incorreta", 400)

            if password_data["new_password"] == "":
                raise APIException("Informe a nova senha", 400)

            self.verify_is_valid_password(password_data["new_password"], "nova senha")


            if password_data["current_password"] == password_data["new_password"]:
                raise APIException("A senha atual e a nova senha não devem coincidir", 400)

            if password_data["new_password"] != password_data["confirm_new_password"]:
                raise APIException("Verifique a confirmação de nova senha. As senhas não coincidem.", 400)

            user.set_password(password_data["new_password"])

            db.session.commit()

        except APIException as e:
            db.session.rollback()
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            db.session.rollback()
            raise APIException (f"{str(e)}", 500) from e
