from app.services.book_service import BookService
from app.exceptions import APIException


book_service = BookService()

class BookController:
    def register_book(self, book_data):

        book = {
            "cover": book_data["cover"],
            "title": book_data.get("title", "").strip(),
            "author": book_data.get("author", "").strip(),
            "publisher": book_data.get("publisher", "").strip(),
            "category": book_data.get("category", "").strip(),
            "publication_year": book_data.get("publication_year", "").strip(),
            "synopsis": book_data.get("synopsis", "").strip(),
            "file": book_data["file"],
        }

        try:
            if book_service.is_valid_book(book, verify_title_exists=True):
                book_service.create_book(book)
                return { "message": "Livro cadastrado com sucesso", "status": 201 }

            return { "message": "Dados inválidos.", "status": 400 }

        except APIException as e:
            return { "message": f"{str(e)}", "status": e.status_code}


    def get_all_books(self):
        try:
            books = book_service.get_all_books()
            books_data = {
                "books": books,
                "books_count": len(books) 
            }

            return { "message": "Livros encontrados", "data": books_data, "status": 200}

        except APIException as e:
            return {"message": str(e), "status": e.status_code}


    def get_book(self, book_id):
        try:
            author = book_service.get_book_by_id(book_id)

            return { "message": "Livro encontrado", "data": author.to_dict(), "status": 200}

        except APIException as e:
            return {"message": str(e), "status": e.status_code}


    def edit_book(self, book_id, book_data):
        try:
            book = {
                "title":  book_data.get("title", "").strip(),
                "author": book_data.get("author", "").strip(),
                "publisher": book_data.get("publisher", "").strip(),
                "category": book_data.get("category", "").strip(),
                "publication_year": book_data.get("publication_year", "").strip(),
                "synopsis": book_data.get("synopsis", "").strip(),
            }

            if book_data["cover"]:
                book["cover"] = book_data["cover"]

            if book_data["file"]:
                book["file"] = book_data["file"]

            book_data = book

            if book_service.is_valid_book(book):
                response = book_service.update_book(book_id, book_data)

                return {
                    "message": "Livro editado com sucesso!", 
                    "data": response["updated_book"],
                    "status": 200, 
                }

            return { "message": "Dados inválidos.", "status": 400 }

        except APIException as e:
            return { "message": str(e), "status": e.status_code }


    def delete_book(self, book_id):
        try:
            book_service.delete_book(book_id)

            return {
                "message": "Livro deletado com sucesso!", 
                "status": 200, 
            }

        except APIException as e:
            return { "message": str(e), "status": e.status_code }


    def get_books_by_category(self):
        try:
            books_by_category = book_service.get_books_by_category()

            return {
                "message": "Livros por categoria encontrados",
                "data": books_by_category,
                "status": 200
            }

        except APIException as e:
            return {
                "message": str(e),
                "data": {},
                "status": e.status_code
            }


    def get_book_details(self, book_id):
        try:
            book = book_service.get_book_by_id(book_id)

            return {
                "message": "Detalhes do livro encontrados",
                "data": {
                    "id": book.id,
                    "title": book.title,
                    "synopsis": book.synopsis,
                    "publication_year": book.publication_year,
                    "cover": book.cover,
                    "author": book.author.name if book.author else "Desconhecido",
                    "publisher": book.publisher.name if book.publisher else "Desconhecido",
                },
                "status": 200
            }

        except APIException as e:
            return {"message": str(e), "data": None, "status": e.status_code}



    def get_book_file(self, book_id):
        try:
            book_file = book_service.get_book_file(book_id)
            print("CONTROLLER:", book_file)

            return {
                "message": "Arquivo do livro encontrado",
                "data": book_file,
                "status": 200
            }

        except APIException as e:
            return {"message": str(e), "data": None, "status": e.status_code}
