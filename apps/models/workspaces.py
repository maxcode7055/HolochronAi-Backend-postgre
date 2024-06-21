from apps import db
from sqlalchemy.orm import relationship

class Workspace(db.Model):
    __tablename__ = 'workspaces'
    id = db.Column(db.Integer, primary_key=True)
    workspace_name = db.Column(db.String(255), nullable=False)
    settings = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    deleted = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    workspace_unique_id = db.Column(db.String(255), nullable=False)
    is_default = db.Column(db.Boolean, nullable=False)
    # collaborators = relationship('User', secondary='workspace_collaborators')


    user_workspaces = relationship('UserWorkspace', back_populates='workspace')  # Relationship to User
    character = relationship('Character', back_populates='workspace')

    def __init__(self,  workspace_name, settings, created_at, deleted, active, workspace_unique_id, is_default):
       
        self.workspace_name = workspace_name
        self.settings = settings
        self.created_at = created_at
        self.deleted = deleted
        self.active = active
        self.workspace_unique_id = workspace_unique_id
        self.is_default = is_default
        # self.collaborators = collaborators
