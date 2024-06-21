from apps import db
from sqlalchemy.orm import relationship

class UserWorkspace(db.Model):
    __tablename__ = 'user_workspaces'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)  # Foreign key constraint
    workspace_id = db.Column(db.Integer,  db.ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    deleted = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    user = relationship('User', back_populates='user_workspaces')  # Relationship to User
    workspace = relationship('Workspace', back_populates='user_workspaces')  # Relationship to User

    def __init__(self, user_id, workspace_id, deleted, active):
        self.user_id = user_id
        self.workspace_id = workspace_id
        self.deleted = deleted
        self.active = active