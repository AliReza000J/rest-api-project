from datetime import datetime, timedelta
from db import db

class PasswordResetTokenModel(db.Model):
    __tablename__ = "password_reset_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    token_hash = db.Column(db.String(64), unique=True, nullable=False, index=True) # sha256 hex
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    expires_at = db.Column(db.DateTime, nullable=False)
    used_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship(
        "UserModel",
        backref=db.backref("password_reset_tokens", lazy="dynamic", cascade="all, delete-orphan")
    )

    @property
    def is_expired(self) -> bool:
        return datetime.now() >= self.expires_at

    @property
    def is_used(self) -> bool:
        return self.used_at is not None
