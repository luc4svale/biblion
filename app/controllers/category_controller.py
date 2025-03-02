
from app.services.category_service import CategoryService
from app.exceptions import APIException

category_service = CategoryService()

class CategoryController:
    def resgiter_category(self, category_data):

        category = {
            "name": category_data.get("name", "").strip() 
        }

        try:
            if category_service.is_valid_category(category, verify_name_exists=True):
                category_service.create_category(category)
                return { "message": "Categoria cadastrada com sucesso", "status": 201 }

            return { "message": "Dados inválidos.", "status": 400 }

        except APIException as e:
            return { "message": f"{str(e)}", "status": e.status_code}


    def get_category(self, category_id):
        try:
            category = category_service.get_category_by_id(category_id)

            return { "message": "Categoria encontrada", "data": category.to_dict(), "status": 200}

        except APIException as e:
            return {"message": str(e), "status": e.status_code}


    def get_all_categories(self):
        try:
            categories = category_service.get_all_categories()
            categories_data = {
                "categories": categories,
                "categories_count": len(categories) 
            }

            return { "message": "Categorias encontradas", "data": categories_data, "status": 200}

        except APIException as e:
            return {"message": str(e), "status": e.status_code}


    def edit_category(self, category_id, category_data):
        try:
            category_data = {
                "name":  category_data.get("name", "").strip(),
            }

            if category_service.is_valid_category(category_data):
                updated_category = category_service.update_category(category_id, category_data)

                return {
                    "message": "Categoria editada com sucesso!", 
                    "data": updated_category,
                    "status": 200, 
                }

            return { "message": "Dados inválidos.", "status": 400 }

        except APIException as e:
            return { "message": str(e), "status": e.status_code }
