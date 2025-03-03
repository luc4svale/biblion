
from app.services.publisher_service import PublisherService
from app.exceptions import APIException

publisher_service = PublisherService()

class PublisherController:
    def resgiter_publisher(self, publisher_data):

        publisher = {
            "name": publisher_data.get("name", "").strip() 
        }

        try:
            if publisher_service.is_valid_publisher(publisher, verify_name_exists=True):
                publisher_service.create_publisher(publisher)
                return { "message": "Editora cadastrada com sucesso", "status": 201 }

            return { "message": "Dados inválidos.", "status": 400 }

        except APIException as e:
            return { "message": f"{str(e)}", "status": e.status_code}


    def get_publisher(self, publisher_id):
        try:
            publisher = publisher_service.get_publisher_by_id(publisher_id)

            return { "message": "Editora encontrada", "data": publisher.to_dict(), "status": 200}

        except APIException as e:
            return {"message": str(e), "status": e.status_code}


    def get_all_publishers(self):
        try:
            publishers = publisher_service.get_all_publishers()
            publishers_data = {
                "publishers": publishers,
                "publishers_count": len(publishers) 
            }

            return { "message": "Editoras encontradas", "data": publishers_data, "status": 200}

        except APIException as e:
            return {"message": str(e), "status": e.status_code}


    def edit_publisher(self, publisher_id, publisher_data):
        try:
            publisher_data = {
                "name":  publisher_data.get("name", "").strip(),
            }

            if publisher_service.is_valid_publisher(publisher_data):
                updated_publisher = publisher_service.update_publisher(publisher_id, publisher_data)

                return {
                    "message": "Editora editada com sucesso!", 
                    "data": updated_publisher,
                    "status": 200, 
                }

            return { "message": "Dados inválidos.", "status": 400 }

        except APIException as e:
            return { "message": str(e), "status": e.status_code }


    def delete_publisher(self, publisher_id):
        try:
            publisher_service.delete_publisher(publisher_id)

            return {
                "message": "Editora deletada com sucesso!", 
                "status": 200, 
            }

        except APIException as e:
            return { "message": str(e), "status": e.status_code }
