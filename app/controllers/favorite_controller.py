from app.services import FavoriteService
from app.exceptions import APIException

favorite_service = FavoriteService()

class FavoriteController:

    def register_favorite(self, user_id, book_id):
        try:
            if not book_id:
                raise APIException("Não foi possível carregar os dados do livro", 400)

            response = favorite_service.create_favorite(user_id, book_id)
            return response
        except APIException as e:
            return {"message": str(e), "status": e.status_code}


    def get_favorite_by_user_and_book(self, user_id, book_id):
        return favorite_service.get_favorite_by_user_and_book(user_id, book_id)


    def get_user_favorites(self, user_id):
        favorites = favorite_service.get_user_favorites(user_id)

        return [
            {
                "id": favorite.book.id,
                "favorite_id": favorite.id,
                "title": favorite.book.title,
                "cover": favorite.book.cover,
                "author": favorite.book.author.name if favorite.book.author else "Desconhecido",
                "publisher": favorite.book.publisher.name if favorite.book.publisher else "Desconhecido",
                "publication_year": favorite.book.publication_year
            }
            for favorite in favorites
        ]


    def remove_favorite(self, favorite_id):
        try:
            response = favorite_service.remove_favorite(favorite_id)
            return response
        except APIException as e:
            return {"message": str(e), "status": e.status_code}
