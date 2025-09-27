from datetime import datetime
from db import db

class TokenBlocklistModel(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), unique=True, index=True, nullable=False)
    token_type = db.Column(db.String(10), nullable=False)  # "access" | "refresh"
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    revoked_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    expires_at = db.Column(db.DateTime, nullable=False)

    user = db.relationship(
        "UserModel",
        backref=db.backref("revoked_tokens", lazy="dynamic", cascade="all, delete-orphan")
    )
