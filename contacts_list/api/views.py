from datetime import datetime, timedelta
from functools import wraps
import jwt
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from contacts_list.config import Config
from contacts_list.db import db
from .models import User
from . import api

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        authorization = request.headers.get("Authorization")
        prefix = "Bearer "

        if not authorization:
            return {"detail": 'Missing "Authorization" header'}, 401

        if not authorization.startswith(prefix):
            return {"detail": "Invalid token prefix"}, 401

        token = authorization.split(" ")[1]
        if not token:
            return {"detail": "Missing token"}, 401

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return {"detail": "Token expired"}, 401
        except jwt.exceptions.InvalidTokenError:
            return {"detail": "Invalid token"}, 401

        request.user = db.session.execute(
            db.select(models.User).where(models.User.id == payload["sub"])
        ).scalar_one()

        return func(*args, **kwargs)

    return wrapper

@api.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
@api.route("/users/", methods=["GET", "POST"])
def users(user_id=None):
    if user_id is not None:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"detail": "Usuario no encontrado"}), 404

        if request.method == "PUT":
            data = request.get_json()
            user.username = data.get("username", user.username)
            user.email = data.get("email", user.email)
            user.password = generate_password_hash(data.get("password", user.password))
            user.phone = data.get("phone", user.phone)
            user.address = data.get("address", user.address)

            db.session.commit()

            return jsonify({"detail": f"user {user.username} modified"}), 200

        if request.method == "DELETE":
            db.session.delete(user)
            db.session.commit()

            return jsonify({"detail": f"user {user.username} deleted"}), 200

        return jsonify({
            "id_user": user.id_user,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "address": user.address
        }), 200

    if request.method == "GET":
        users = User.query.all()  
        users_list = [{
            "id_user": user.id_user,
            "username": user.username,
            "email": user.email,
            "phone": user.phone,
            "address": user.address
        } for user in users]
        return jsonify(users_list), 200

    if request.method == "POST":
        data = request.get_json()  
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")
        address = data.get("address")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"detail": "El correo electrónico ya está registrado"}), 400

        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            phone=phone,
            address=address
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"detail": "Usuario registrado exitosamente"}), 201