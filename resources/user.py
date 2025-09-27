# from flask import current_app
import os, secrets, hashlib
from flask import jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required)
from sqlalchemy import or_ 
from datetime import datetime, timedelta

from db import db
from models import UserModel, PasswordResetTokenModel, TokenBlocklistModel
from schemas import UserSchema, UserRegisterSchema, ForgotPasswordRequestSchema, ResetPasswordConfirmSchema
from tasks import send_user_registration_email, send_password_reset_email
from security.admin_required import admin_required



blp = Blueprint("Users", "users", description="Operations on users")



@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        email_norm = user_data["email"].strip().lower()
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == email_norm
            )
        ).first():
            return jsonify({"message":"A user with that username or email already exists!!"}), 409
            
            
        user = UserModel(
            username=user_data["username"],
            email=email_norm,
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        # current_app.queue.enqueue(send_user_registration_email, user.email, user.username)

        send_user_registration_email(
            email=user.email,
            username=user.username
        )
        
        return jsonify({"message": "User created successfully"}), 201
    


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self , user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return jsonify({"message":"Invalid credentials!!"}), 401


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        jwt_data = get_jwt()
        user_id = jwt_data["sub"]

        db.session.add(TokenBlocklistModel(
            jti=jwt_data["jti"],
            token_type="refresh",
            user_id=user_id,
            expires_at=datetime.fromtimestamp(jwt_data["exp"]),
        ))

        new_access = create_access_token(identity=user_id, fresh=False)
        new_refresh = create_refresh_token(identity=user_id)

        db.session.commit()
        return {"access_token": new_access, "refresh_token": new_refresh}, 200

@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jwt_data = get_jwt()
        db.session.add(TokenBlocklistModel(
            jti=jwt_data["jti"],
            token_type=jwt_data.get("type", "access"),
            user_id=jwt_data.get("sub"),
            expires_at=datetime.fromtimestamp(jwt_data["exp"]),
        ))
        db.session.commit()
        return jsonify({"message": "Successfully logged out."}), 200



@blp.route("/user/<int:user_id>")
class User(MethodView):
    @admin_required
    @blp.response(200, UserSchema)
    def get(self, user_id):
        return UserModel.query.get_or_404(user_id)
    
    @admin_required
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200

    


@blp.route("/user/forgot-password")
class ForgotPassword(MethodView):
    @blp.arguments(ForgotPasswordRequestSchema)
    def post(self, args):
        email = args["email"].strip().lower()

        status_payload = {"message": "If that account exists, an email will be sent shortly."}

        user = UserModel.query.filter(
            UserModel.email.ilike(email)
        ).first()

        if not user:
            return status_payload, 202
            

        ttl_minutes = int(os.getenv("PASSWORD_RESET_TTL_MINUTES", "60"))

        raw_token = secrets.token_urlsafe(48)
        token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

        PasswordResetTokenModel.query.filter(
            PasswordResetTokenModel.user_id == user.id,
            PasswordResetTokenModel.used_at.is_(None)
            ).delete(synchronize_session=False)
            
        prt = PasswordResetTokenModel(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=datetime.now() + timedelta(minutes=ttl_minutes)
        )

        db.session.add(prt)
        db.session.commit()


        base_reset_url = os.getenv("FRONTEND_RESET_URL")
        reset_url = f"{base_reset_url}?token={raw_token}"


        # current_app.queue.enqueue(send_password_reset_email, user.email, user.username, reset_url)

        send_password_reset_email(user.email, user.username, reset_url)

        return status_payload, 202



@blp.route("/user/reset-password")
class ResetPassword(MethodView):
    @blp.arguments(ResetPasswordConfirmSchema)
    def post(self, args):
        token = args["token"]
        new_password = args["password"]

        token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
        prt = PasswordResetTokenModel.query.filter_by(token_hash=token_hash).first()

        if (not prt) or prt.is_used or prt.is_expired:
            abort(400, message="Invalid or expired token.")

        user = prt.user
        user.password = pbkdf2_sha256.hash(new_password)
        prt.used_at = datetime.now()

        db.session.commit()

        return {"message": "Password updated successfully."}, 200
