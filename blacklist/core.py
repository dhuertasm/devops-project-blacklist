import secrets
import hashlib
from datetime import timedelta, datetime
from .models import Usuarios, db
from flask_jwt_extended import create_access_token


def creacion_usuario(request):

    try:
        existe_usuario = Usuarios.query.filter(Usuarios.username == request.json["username"]).first()
        existe_email = Usuarios.query.filter(Usuarios.email == request.json["email"]).first()
        if existe_usuario is not None or existe_email is not None:
            return {"mensaje": "El usuario ya existe, pruebe con otro"}, 412

        salt = secrets.token_hex(8)
        password = f"{request.json['password']}{salt}"

        nuevo_usuario = Usuarios(
            username=request.json["username"],
            email=request.json["email"],
            password=hashlib.sha256(password.encode()).hexdigest(),
            salt=salt,
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return {"id": nuevo_usuario.id, "createdAt": datetime.now().isoformat()}, 201
    except Exception as e:
        print(e)
        return {"mensaje": f"falta {e}"}, 400

def autenticar_usuario(request):
    try:

        usuario_auth = Usuarios.query.filter(Usuarios.username == request.json["username"]).first()

        if usuario_auth is None:
            return {"mensaje": "Usuario con username no exista o contrasena incorrecta"}, 404

        password_input = f"{request.json['password']}{usuario_auth.salt}"
        password = Usuarios.query.filter(Usuarios.username == request.json["username"],
                                         Usuarios.password == hashlib.sha256(password_input.encode()).hexdigest()
                                         ).first()

        if password is None:
            return {"mensaje": "Usuario con username no exista o contrasena incorrecta"}, 404

        token_user = create_access_token(identity=usuario_auth.id)
        expireAt = datetime.now() + timedelta(minutes=30)
        usuario_auth.expireAt = expireAt
        usuario_auth.token = token_user
        db.session.commit()
        return {"id": usuario_auth.id,
                "token": token_user,
                "expireAt": expireAt.isoformat()}, 200

    except Exception as e:
        print(e)
        return {"mensaje": f"falta {e}"}, 400


def self_information(request):
    token_headers = request.headers.get('Authorization')
    if token_headers is None:
        return {"mensaje": "No viene token"}, 400

    token_user = token_headers.split(" ")[1]
    curren_user = Usuarios.query.filter(Usuarios.token == token_user).first()

    if curren_user is None:
        return {"mensaje": "token no válido"}, 401

    if curren_user.expireAt > (datetime.now() + timedelta(minutes=30)):
        return {"mensaje": "token expirado"}, 401

    return {"id": curren_user.id,
            "username": curren_user.username,
            "email": curren_user.email}, 200


