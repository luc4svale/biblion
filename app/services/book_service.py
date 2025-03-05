from datetime import datetime
from collections import defaultdict
import re
import os
from pathlib import Path
from werkzeug.utils import secure_filename
from app.models import db, Book
from app.services import AuthorService, PublisherService, CategoryService
from app.exceptions import APIException
from app.utils.random_str import str_rand

author_service = AuthorService()
publisher_service = PublisherService()
category_service = CategoryService()

class BookService:

    def verify_is_valid_cover_file(self, cover_file):
        try:
            valid_types = {"image/jpeg", "image/png", "image/webp", "image/svg+xml"}
            max_size = 5 * 1024 * 1024


            if not cover_file:
                raise ValueError("É necessário carregar uma imagem para a capa do livro.")


            filename = secure_filename(cover_file.filename)
            if filename == "":
                raise ValueError("Nome inválido para arquivo da imagem de capa do livro.")


            mime_type = cover_file.mimetype
            if mime_type not in valid_types:
                raise ValueError("Tipo de arquivo inválido para a imagem de capa do livro.")


            cover_file.seek(0, os.SEEK_END)
            file_size = cover_file.tell()
            cover_file.seek(0)

            if file_size > max_size:
                raise ValueError("Tamanho máximo de 5MB excedido para imagem de capa do livro.")

            return True
        except Exception as e:
            raise ValueError(f"{str(e)}") from e


    def save_cover_file(self, cover_file):
        try:
            if cover_file is None:
                return None

            extension_for_each_type = {"image/jpeg": "jpeg", "image/png": "png", "image/webp": "webp", "image/svg+xml": "svg"}
            cover_filename = f"{str_rand(64)}.{extension_for_each_type[cover_file.mimetype]}"
            upload_folder = "uploads/covers"
            os.makedirs(upload_folder, exist_ok=True)
            upload_path = os.path.join(upload_folder, cover_filename)
            cover_file.save(upload_path)

            return cover_filename

        except Exception as e:
            raise ValueError("Erro ao salvar imagem de capa do livro") from e


    def delete_cover_file(self, cover_file_path):
        path = Path(cover_file_path)

        if path.exists():
            return path.unlink()
        return None


    def verify_is_valid_book_file(self, book_file):
        try:
            valid_types = {"application/pdf"}
            max_size = 20 * 1024 * 1024


            if not book_file:
                raise ValueError("É necessário carregar o arquivo de conteúdo do livro.")


            filename = secure_filename(book_file.filename)
            if filename == "":
                raise ValueError("Nome inválido para arquivo da conteúdo do livro.")


            mime_type = book_file.mimetype
            if mime_type not in valid_types:
                raise ValueError("Tipo de arquivo inválido arquivo de conteúdo do livro.")


            book_file.seek(0, os.SEEK_END)
            file_size = book_file.tell()
            book_file.seek(0)

            if file_size > max_size:
                raise ValueError("Tamanho máximo de 5MB excedido para arquivo de conteúdo do livro.")

            return True
        except Exception as e:
            raise ValueError(f"{str(e)}") from e


    def save_book_file(self, book_file):
        try:
            if book_file is None:
                return None

            extension_for_each_type = { "application/pdf": "pdf" }
            book_file_name = f"{str_rand(32)}.{extension_for_each_type[book_file.mimetype]}"
            upload_folder = "uploads/books"
            os.makedirs(upload_folder, exist_ok=True)
            upload_path = os.path.join(upload_folder, book_file_name)
            book_file.save(upload_path)

            return book_file_name

        except Exception as e:
            raise ValueError("Erro ao salvar arquivo de conteúdo do livro") from e


    def delete_book_file(self, book_file_path):
        path = Path(book_file_path)

        if path.exists():
            return path.unlink()
        return None


    def verify_is_valid_title(self, title, field="título"):
        invalid_chars_pattern = r"[^\sa-zA-Z0-9.,-/ª°ºàáâãéêíóôõúÀÁÂÃÉÊÍÓÔÕÚçÇ']"
        if re.search(invalid_chars_pattern, title):
            raise ValueError(f"O {field} contém caracteres inválidos")
        invalid_chars_position_or_combination_pattern = r"^[0-9]+$|\s{2,}|'{4,}|\.{2,}|,{2,}|-{2,}|\/{2,}|ª{2,}|º{2,}|°{2,}|^'+|^\.+|^,+|^-+|^\/+|^ª+|^º+|^°+"
        if re.search(invalid_chars_position_or_combination_pattern, title):
            raise ValueError(f"O {field} contém posição ou combinação inválida de caracteres.")
        if (not title) or (len(title) < 2 or len(title) > 200):
            raise ValueError(f"O {field} deve ter entre 2 e 200 caracteres.")
        return True


    def is_title_registered(self, title):
        try:
            if Book.query.filter_by(title=title).first() is None:
                return False
            return True

        except Exception as e:
            raise APIException ("Erro desconhecido", 500) from e


    def verify_is_valid_author(self, author_id):
        try:
            if not author_id:
                raise ValueError("Por favor, selecione o autor do livro")
            if author_service.get_author_by_id(author_id) is None:
                raise ValueError("Autor inválido")
            return 

        except APIException as e:
            raise APIException (f"{str(e)}", e.status_code) from e


    def verify_is_valid_publisher(self, publisher_id):
        try:
            if not publisher_id:
                raise ValueError("Por favor, selecione a editora do livro")
            if publisher_service.get_publisher_by_id(publisher_id) is None:
                raise ValueError("Editora inválida")  
            return True

        except APIException as e:
            raise APIException (f"{str(e)}", e.status_code) from e


    def verify_is_valid_category(self, category_id):
        try:
            if not category_id:
                raise ValueError("Por favor, selecione a categoria do livro")
            if category_service.get_category_by_id(category_id) is None:
                raise ValueError("Categoria inválida")  
            return True

        except APIException as e:
            raise APIException (f"{str(e)}", e.status_code) from e


    def is_valid_publication_year(self, publication_year):
        current_year = datetime.now().year

        if isinstance(publication_year, (int, float)):
            return 1500 <= publication_year <= current_year

        if isinstance(publication_year, str) and publication_year.isdigit():
            year = int(publication_year)
            return 1500 <= year <= current_year

        return False


    def verify_is_valid_synopsis(self, synopsis, field="sinopse"):
        invalid_chars_pattern = r"[^\sa-zA-Z0-9.,-/ª°ºàáâãéêíóôõúÀÁÂÃÉÊÍÓÔÕÚçÇ']"
        if re.search(invalid_chars_pattern, synopsis):
            raise ValueError(f"A {field} contém caracteres inválidos.")
        invalid_chars_position_or_combination_pattern = r"^[0-9]+$|\s{2,}|'{4,}|\.{2,}|,{2,}|-{2,}|\/{2,}|ª{2,}|º{2,}|°{2,}|^'+|^\.+|^,+|^-+|^\/+|^ª+|^º+|^°+"
        if re.search(invalid_chars_position_or_combination_pattern, synopsis):
            raise ValueError(f"A {field} contém posição ou combinação inválida de caracteres.")
        if (not synopsis) or (len(synopsis) < 20 or len(synopsis) > 2000):
            raise ValueError(f"A {field} deve ter entre 20 e 2000 caracteres.")
        return True


    def is_valid_book(self, book, verify_title_exists=False):
        try:
            if "cover" in book:
                self.verify_is_valid_cover_file(book["cover"])
            if "title" in book:
                self.verify_is_valid_title(book["title"], "título do livro")
                if (verify_title_exists and self.is_title_registered(book["title"])):
                    raise ValueError("Título de livro já registrado.")
            if "author" in book:
                self.verify_is_valid_author(book["author"])
            if "publisher" in book:
                self.verify_is_valid_publisher(book["publisher"])
            if "category" in book:
                self.verify_is_valid_category(book["category"])
            if ("publication_year" in book) and (not self.is_valid_publication_year(book["publication_year"])):
                raise ValueError("O ano de publicação deve estar entre 1500 e o ano atual")
            if "synopsis" in book:
                self.verify_is_valid_synopsis(book["synopsis"])
            if "file" in book:
                self.verify_is_valid_book_file(book["file"])
            return True
        except Exception as e:
            raise APIException(f"{str(e)}", 400) from e


    def get_book_by_id(self, book_id):
        try:
            book = Book.query.get(book_id)
            if not book:
                raise APIException("Livro não encontrado", 404)
            return book

        except APIException as e:
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            raise APIException ("Erro desconhecido", 500) from e


    def get_all_books(self):
        try:
            return Book.query.order_by(Book.created_at.desc()).all()

        except Exception as e:
            raise APIException("Erro desconhecido", 500) from e


    def create_book(self, book):
        try:
            cover_file_name = self.save_cover_file(book["cover"])
            book_file_name = self.save_book_file(book["file"])

            new_book = Book(
                title=book["title"],
                author_id=book["author"],
                publisher_id=book["publisher"],
                category_id=book["category"],
                publication_year=book["publication_year"],
                synopsis=book["synopsis"],
                cover=cover_file_name,
                file=book_file_name,
            )


            db.session.add(new_book)
            db.session.commit()
            return new_book.id

        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro desconhecido", 500) from e


    def update_book(self, book_id, book_data):
        try:
            book = self.get_book_by_id(book_id)

            if not book:
                raise APIException("Livro não encontrado", 404)

            has_changed_title = (book_data["title"] != book.title)
            has_changed_author = (book_data["author"] != book.author.id)
            has_changed_publisher = (book_data["publisher"] != book.publisher.id)
            has_changed_category = (book_data["category"] != book.category.id)
            has_changed_publication_year = (int(book_data["publication_year"]) != book.publication_year)
            has_changed_synopsis = (book_data["synopsis"] != book.synopsis)
            has_changed_cover = (book_data.get("cover", None) is not None)
            has_changed_file = (book_data.get("file", None) is not None)

            equal_fields = (
                (not has_changed_title)
                and (not has_changed_author)
                and (not has_changed_publisher)
                and (not has_changed_category)
                and (not has_changed_publication_year)
                and (not has_changed_synopsis)
                and (not has_changed_cover)
                and (not has_changed_file)            
            )


            if equal_fields:
                raise APIException("Nenhuma alteração foi detectada", 400)

            cover_filename = self.save_cover_file(book_data["cover"]) if has_changed_cover else None
            book_file_name = self.save_book_file(book_data["file"]) if has_changed_file else None

            book.title = book_data["title"]
            book.author_id = book_data["author"]
            book.publisher_id = book_data["publisher"]
            book.category_id = book_data["category"]
            book.publication_year = book_data["publication_year"]
            book.synopsis = book_data["synopsis"]

            last_cover_path = os.path.join("uploads/covers", book.cover)
            book.cover = book.cover if cover_filename is None else cover_filename

            last_book_file_path = os.path.join("uploads/books", book.file)
            book.file = book.file if book_file_name is None else book_file_name


            if has_changed_cover:
                self.delete_cover_file(last_cover_path)

            if has_changed_file:
                self.delete_book_file(last_book_file_path)

            db.session.commit()

            return { "updated_book": book.to_dict() }

        except APIException as e:
            db.session.rollback()
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro desconhecido", 500) from e


    def delete_book(self, book_id):
        try:
            book = self.get_book_by_id(book_id)

            if not book:
                raise APIException("Livro não encontrado", 404)

            db.session.delete(book)
            db.session.commit()

        except APIException as e:
            db.session.rollback()
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro desconhecido", 500) from e


    def get_books_by_category(self):
        try:
            books = Book.query.all()

            books_by_category = defaultdict(list)
            for book in books:
                books_by_category[book.category.name].append(book)


            books_by_category = dict(books_by_category)

            return books_by_category

        except Exception as e:
            raise APIException("Erro desconhecido", 500) from e


    def get_book_file(self, book_id):
        try:
            book = Book.query.get(book_id)

            if not book:
                raise APIException("Livro não encontrado", 404)

            if not book.file:
                raise APIException("Arquivo do livro não disponível", 400)

            return book.file

        except Exception as e:
            raise APIException("Erro ao buscar o livro", 500) from e
