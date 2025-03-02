import re
from app.models.category import Category
from app.models.database import db
from app.exceptions import APIException

class CategoryService:

    def verify_is_valid_name(self, name, field="nome da categoria"):
        invalid_chars_pattern = r"[^a-zA-ZàáâãéêíóôõúÀÁÂÃÉÊÍÓÔÕÚçÇ\s']"
        if re.search(invalid_chars_pattern, name):
            raise ValueError(f"O {field} contém caracteres inválidos")
        invalid_chars_position_or_combination_pattern = r"\s{2,}|'{2,}|^\s+|^'"
        if re.search(invalid_chars_position_or_combination_pattern, name):
            raise ValueError(f"O {field} contém posição ou combinação inválida de caracteres.")
        if (not name) or (len(name) < 2 or len(name) > 100):
            raise ValueError(f"O {field} deve ter entre 2 e 100 caracteres.")
        return True


    def is_name_registered(self, name):
        if Category.query.filter_by(name=name).first() is None:
            return False
        return True


    def is_valid_category(self, category, verify_name_exists=False):
        try:
            if "name" in category:
                self.verify_is_valid_name(category["name"], "nome da categoria")
                if (verify_name_exists and self.is_name_registered(category["name"])):
                    raise ValueError("Nome de categoria já registrado.")
            return True
        except Exception as e:
            raise APIException(f"{str(e)}", 400) from e


    def get_category_by_id(self, category_id):
        try:
            category = Category.query.get(category_id)
            if category:
                return category
            raise APIException("Categoria não encontrada", 404)

        except APIException as e:
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            raise APIException ("Erro desconhecido", 500) from e


    def get_all_categories(self):
        try:
            return Category.query.all()

        except Exception as e:
            raise APIException("Erro desconhecido", 500) from e



    def create_category(self, category):
        new_category = Category(name=category["name"])

        try:
            db.session.add(new_category)
            db.session.commit()
            return new_category.id

        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro desconhecido", 500) from e
