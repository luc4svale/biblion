import re
from app.models.author import Author
from app.models.database import db
from app.exceptions import APIException

class AuthorService:

    def verify_is_valid_name(self, name, field="nome do autor"):
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
        if Author.query.filter_by(name=name).first() is None:
            return False
        return True


    def is_valid_author(self, author, verify_name_exists=False):
        try:
            if "name" in author:
                self.verify_is_valid_name(author["name"], "nome do autor")
                if (verify_name_exists and self.is_name_registered(author["name"])):
                    raise ValueError("Nome de autor já registrado.")
            return True
        except Exception as e:
            raise APIException(f"{str(e)}", 400) from e


    def get_author_by_id(self, author_id):
        try:
            author = Author.query.get(author_id)
            if not author:
                raise APIException("Autor não encontrado", 404)
            return author

        except APIException as e:
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            raise APIException ("Erro desconhecido", 500) from e


    def get_all_authors(self):
        try:
            return Author.query.all()

        except Exception as e:
            raise APIException("Erro desconhecido", 500) from e



    def create_author(self, author):
        new_author = Author(name=author["name"])

        try:
            db.session.add(new_author)
            db.session.commit()
            return new_author.id

        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro desconhecido", 500) from e



    def update_author(self, author_id, author_data):
        try:
            author = self.get_author_by_id(author_id)

            if not author:
                raise APIException("Autor não encontrado", 404)

            equal_fields = author_data["name"] == author.name

            if equal_fields:
                raise APIException("Nenhuma alteração foi detectada", 400)

            author.name = author_data["name"]

            db.session.commit()

            return author.to_dict()

        except APIException as e:
            db.session.rollback()
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro desconhecido", 500) from e


    def delete_author(self, author_id):
        try:
            author = self.get_author_by_id(author_id)

            if not author:
                raise APIException("Autor não encontrado", 404)

            db.session.delete(author)
            db.session.commit()

        except APIException as e:
            db.session.rollback()
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro desconhecido", 500) from e
