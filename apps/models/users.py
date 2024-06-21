from apps import db
from sqlalchemy.orm import relationship
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    is_google_login = db.Column(db.Boolean, default=False)
    is_microsoft_login = db.Column(db.Boolean, default=False)
    chat_setting = db.Column(db.Integer, default=25)
    active = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)

    user_workspaces = relationship('UserWorkspace', back_populates='user')  # Relationship to UserWorkspace
    # user_workspaces = relationship('UserWorkspace', back_populates='user')
    def __repr__(self):
        return f'<User {self.email}>'
