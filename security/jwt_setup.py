# security/jwt_setup.py
import os
from datetime import datetime, timedelta
from flask import jsonify
from flask_jwt_extended import JWTManager
from models import UserModel, TokenBlocklistModel

jwt = JWTManager()

def init_jwt(app):
    access_minutes = int(os.getenv("JWT_ACCESS_MINUTES", "60"))
    refresh_days = int(os.getenv("JWT_REFRESH_DAYS", "30"))
    app.config.setdefault("JWT_ACCESS_TOKEN_EXPIRES", timedelta(minutes=access_minutes))
    app.config.setdefault("JWT_REFRESH_TOKEN_EXPIRES", timedelta(days=refresh_days))
    jwt.init_app(app)

@jwt.token_in_blocklist_loader
def token_in_blocklist(jwt_header, jwt_payload):
    # DB blocklist check (logout / refresh rotation / manual revoke)
    jti = jwt_payload.get("jti")
    return bool(jti and TokenBlocklistModel.query.filter_by(jti=jti).first())

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "description": "the token has been revoked!",
        "error": "token_revoked"
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return jsonify({
        "description": "The token is not fresh",
        "error": "fresh_token_required"
    }), 401

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.query.get(identity)
    return {"is_admin": bool(user and user.is_admin)}

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        "message": "The token has been expired.",
        "error": "token_expired"
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error_string: str):
    return jsonify({
        "message": "Signature verification failed.",
        "error": "invalid_expired"
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error_string: str):
    return jsonify({
        "description": "request does not contain an access token.",
        "error": "authorization_required"
    }), 401
