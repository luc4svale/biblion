from app.models import db, Favorite
from app.services import BookService
from app.exceptions import APIException

book_service = BookService()

class FavoriteService:

    def get_favorite_by_user_and_book(self, user_id, book_id):
        return Favorite.query.filter_by(user_id=user_id, book_id=book_id).first()


    def create_favorite(self, user_id, book_id):
        try:

            book = book_service.get_book_by_id(book_id)
            favorite = self.get_favorite_by_user_and_book(user_id, book_id)

            if book and favorite:
                raise APIException("O livro já está na lista de favoritos", 400)


            favorite = Favorite(user_id=user_id, book_id=book_id)
            db.session.add(favorite)
            db.session.commit()

            return {"message": "Livro adicionado aos favoritos", "status": 201}

        except APIException as e:
            db.session.rollback()
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            db.session.rollback()
            raise APIException ("Erro desconhecido", 500) from e


    def get_favorite_by_id(self, favorite_id):
        try:
            favorite = Favorite.query.get(favorite_id)

            if not favorite:
                raise APIException("Favorito não encontrado", 404)
            return favorite

        except APIException as e:
            raise APIException(f"{str(e)}", e.status_code) from e

        except Exception as e:
            raise APIException ("Erro desconhecido", 500) from e


    def get_user_favorites(self, user_id):
        return Favorite.query.filter_by(user_id=user_id).all()

    def remove_favorite(self, favorite_id):
        try:
            favorite = self.get_favorite_by_id(favorite_id)

            if not favorite:
                raise APIException("O livro não está na sua lista de favoritos", 404)

            db.session.delete(favorite)
            db.session.commit()

            return { "message": "Livro removido dos favoritos", "status": 200 }

        except APIException as e:
            raise e
        except Exception as e:
            db.session.rollback()
            raise APIException("Erro desconhecido", 500) from e
