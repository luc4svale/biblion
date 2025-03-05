import re
from app.models.publisher import db, Publisher
from app.exceptions import APIException

class PublisherService:

    def verify_is_valid_name(self, name, field="nome da editora"):
        invalid_chars_pattern = r"[^\.a-zA-ZàáâãéêíóôõúÀÁÂÃÉÊÍÓÔÕÚçÇ\s']"
        if re.search(invalid_chars_pattern, name):
            raise ValueError(f"O {field} contém caracteres inválidos")
        invalid_chars_position_or_combination_pattern = r"\.{2,}|\s{2,}|'{2,}|^\s+|^'"
        if re.search(invalid_chars_position_or_combination_pattern, name):
            raise ValueError(f"O {field} contém posição ou combinação inválida de caracteres.")
        if (not name) or (len(name) < 2 or len(name) > 100):
            raise ValueError(f"O {field} deve ter entre 2 e 100 caracteres.")
        return True


    def is_name_registered(self, name):
        try:
            if Publisher.query.filter_by(name=name).first() is None:
                return False
            return True
        except Exception as e:
            raise APIException ("Erro desconhecido", 500) from e



    def is_valid_publisher(self, publisher, verify_name_exists=False):
        try:
            if "name" in publisher:
                self.verify_is_valid_name(publisher["name"], "nome da editora")
                if (verify_name_exists and self.is_name_registered(publisher["name"])):
                    raise ValueError("Nome de editora já registrado.")
            return True
        except Exception as e:
            raise APIException(f"{str(e)}", 400) from e


    def get_publisher_by_id(self, publisher_id):
        try:
            publisher = Publisher.query.get(publisher_id)
            if not publisher:
                raise APIException("Editora não encontrada", 404)
            return publisher
            
        except APIException as e:
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            raise APIException ("Erro desconhecido", 500) from e


    def get_all_publishers(self):
        try:
            return Publisher.query.order_by(Publisher.name.asc()).all()

        except Exception as e:
            raise APIException("Erro desconhecido", 500) from e



    def create_publisher(self, publisher):
        new_publisher = Publisher(name=publisher["name"])

        try:
            db.session.add(new_publisher)
            db.session.commit()
            return new_publisher.id

        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro desconhecido", 500) from e



    def update_publisher(self, publisher_id, publisher_data):
        try:
            publisher = self.get_publisher_by_id(publisher_id)

            if not publisher:
                raise APIException("Editora não encontrada", 404)

            equal_fields = publisher_data["name"] == publisher.name

            if equal_fields:
                raise APIException("Nenhuma alteração foi detectada", 400)

            publisher.name = publisher_data["name"]

            db.session.commit()

            return publisher.to_dict()

        except APIException as e:
            db.session.rollback()
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro desconhecido", 500) from e


    def delete_publisher(self, publisher_id):
        try:
            publisher = self.get_publisher_by_id(publisher_id)

            if not publisher:
                raise APIException("Editora não encontrada", 404)

            db.session.delete(publisher)
            db.session.commit()

        except APIException as e:
            db.session.rollback()
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro desconhecido", 500) from e
