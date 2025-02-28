from functools import wraps
from flask import redirect
from flask_login import current_user

def logout_required(route_function):
    @wraps(route_function)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect("/home")
        return route_function(*args, **kwargs)

    return decorated_function
