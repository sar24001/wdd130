from functools import wraps
from flask import redirect, url_for, session

def require_role(role):
    """
    Decorador que restringe el acceso a una vista
    según el rol de usuario almacenado en session["id_rol"].
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Verificar si el rol en la sesión coincide con el rol requerido
            if session.get("id_rol") != role:
                # Si el rol no coincide, redirigir a una página de acceso denegado o login
                return redirect(url_for('main'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
