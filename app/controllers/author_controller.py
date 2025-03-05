
from app.services.author_service import AuthorService
from app.exceptions import APIException

author_service = AuthorService()

class AuthorController:
    def register_author(self, author_data):

        author = {
            "name": author_data.get("name", "").strip() 
        }

        try:
            if author_service.is_valid_author(author, verify_name_exists=True):
                author_service.create_author(author)
                return { "message": "Autor cadastrado com sucesso", "status": 201 }

            return { "message": "Dados inválidos.", "status": 400 }

        except APIException as e:
            return { "message": f"{str(e)}", "status": e.status_code}


    def get_author(self, author_id):
        try:
            author = author_service.get_author_by_id(author_id)

            return { "message": "Autor encontrado", "data": author.to_dict(), "status": 200}

        except APIException as e:
            return {"message": str(e), "status": e.status_code}


    def get_all_authors(self):
        try:
            authors = author_service.get_all_authors()
            authors_data = {
                "authors": authors,
                "authors_count": len(authors) 
            }

            return { "message": "Autores encontrados", "data": authors_data, "status": 200}

        except APIException as e:
            return {"message": str(e), "status": e.status_code}


    def edit_author(self, author_id, author_data):
        try:
            author_data = {
                "name":  author_data.get("name", "").strip(),
            }

            if author_service.is_valid_author(author_data):
                updated_author = author_service.update_author(author_id, author_data)

                return {
                    "message": "Autor editado com sucesso!", 
                    "data": updated_author,
                    "status": 200, 
                }

            return { "message": "Dados inválidos.", "status": 400 }

        except APIException as e:
            return { "message": str(e), "status": e.status_code }


    def delete_author(self, author_id):
        try:
            author_service.delete_author(author_id)

            return {
                "message": "Autor deletado com sucesso!", 
                "status": 200, 
            }

        except APIException as e:
            return { "message": str(e), "status": e.status_code }
