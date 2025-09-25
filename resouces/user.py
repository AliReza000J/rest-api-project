from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required
import requests
import os
from sqlalchemy import or_ 
from maileroo import MailerooClient, EmailAddress

from blocklist import BLOCKLIST
from db import db
from models import UserModel
from schemas import UserSchema, UserRegisterSchema


blp = Blueprint("Users", "users", description="Operations on users")


def send_verify_email(to, username, subject, body):
    api = os.getenv('MAILEROO_API_KEY')
    client = MailerooClient(api)
    return client.send_basic_email({
    "from": EmailAddress("alrza0000a@gmail.com", "STORE API"),
    "to": [EmailAddress(to, username)],
    "subject": subject,
    # "html": "<h1>Hello World!</h1><p>This is a test email.</p>",
    "plain": body
})


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"]
            )
        ).first():
            abort(
                409, message="A user with that username or email already exists!!"
            )
            
        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        send_verify_email(
            to=user.email,
            username=user.username,
            subject="Succesfully signed up",
            body=f"Hi {user.username}! You have successfully signed up to the Stores REST API.")

        return {"message": "User created successfully"}, 201
    

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self , user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity="user.id", fresh=True)
            refresh_token = create_refresh_token(identity="user.id")
            return {"access_token": access_token, "refresh_token": refresh_token}

        abort(401, message="Invalid credentials!!")



@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"acces_token": new_token}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self, user_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort (401, message="Admin privilege required!!!")
            
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200