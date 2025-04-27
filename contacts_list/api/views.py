from datetime import datetime, timedelta
from functools import wraps
import jwt
from flask import request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from contacts_list.config import Config
from contacts_list.db import db
from . import api, models
from .models import Contact

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        payload = jwt.decode(
            token,
            Config.SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_sub": False} 
        )
        user = db.session.execute(
            db.select(models.User).where(models.User.id_user == payload["sub"])
        ).scalar_one()
        request.user = user
        return func(*args, **kwargs)
    return wrapper

@api.route("/login/", methods=["POST"])
def login():
    """Login an app user"""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"detail": "missing email or password"}, 400

    user = db.session.execute(
        db.select(models.User).where(models.User.email == email)
    ).scalar_one_or_none()

    if not user or not check_password_hash(user.password, password):
        return {"detail": "invalid email or password"}, 401

    token = jwt.encode(
        {
            "sub": user.id_user,
            "exp": datetime.utcnow() + timedelta(minutes=30),
        },
        Config.SECRET_KEY,
    )

    return {"token": token}

@api.route("/profile/", methods=["POST"])
@token_required
def profile():
    """Returns current user details"""
    user = request.user
    return {
        "usernmae": user.username,
        "email": user.email,
    }


@api.route("/users/<int:user_id>", methods=["GET", "PUT", "DELETE"])
@api.route("/users/", methods=["GET", "POST"])
def users(user_id=None): 

    if user_id is not None:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"detail": "User not found"}), 404

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
            return jsonify({"detail": "The email is already registered"}), 400

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

        return jsonify({"detail": "Successfully registered user"}), 201


@api.route("/contacts/<int:contact_id>", methods=["GET", "PUT", "DELETE"])
@api.route("/contacts/", methods=["GET", "POST"])
@token_required
def contacts(contact_id=None):
    user = request.user  

    if contact_id is not None:
        contact = Contact.query.filter_by(id_contact=contact_id, id_user=user.id_user).first()

        if not contact:
            return jsonify({"detail": "Contact not found or you don't have permission"}), 404

        if request.method == "PUT":
            data = request.get_json()
            contact.name = data.get("name", contact.name)
            contact.email = data.get("email", contact.email)
            contact.phone = data.get("phone", contact.phone)
            contact.address = data.get("address", contact.address)

            db.session.commit()

            return jsonify({"detail": f"Contact {contact.name} modificado"}), 200

        if request.method == "DELETE":
            db.session.delete(contact)
            db.session.commit()

            return jsonify({"detail": f"Contact {contact.name} eliminado"}), 200

        return jsonify({
            "id_contact": contact.id_contact,
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "address": contact.address,
            "id_user": contact.id_user
        }), 200

    if request.method == "GET":
        contacts = Contact.query.filter_by(id_user=user.id_user).all()
        contacts_list = [{
            "id_contact": contact.id_contact,
            "name": contact.name,
            "email": contact.email,
            "phone": contact.phone,
            "address": contact.address,
            "id_user": contact.id_user
        } for contact in contacts]
        return jsonify(contacts_list), 200

    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        address = data.get("address")

        if not all([name, email, phone]):
            return jsonify({"detail": "Name, email and phone number are required"}), 400

        new_contact = Contact(
            name=name,
            email=email,
            phone=phone,
            address=address,
            id_user=user.id_user  
        )

        db.session.add(new_contact)
        db.session.commit()

        return jsonify({"detail": "Contact successfully registered"}), 201
