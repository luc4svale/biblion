from app.models.database import db
from app.models.user import User

def register_user(user):
    """Lógica para cadastrar um usuário"""
    new_user = User(
      first_name=user["first_name"],
      last_name=user["last_name"],
      email=user["email"],
      password=user["password"],
    )

    db.session.add(new_user)
    db.session.commit()

    return {"status": "success", "message": "Usuário cadastrado com sucesso"}
