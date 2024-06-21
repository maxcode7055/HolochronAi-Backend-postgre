from apps import db
from sqlalchemy.orm import relationship

class WorkspaceCollaborators(db.Model):
    __tablename__ = 'workspace_collaborators'
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspaces.id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    def __init__(self,  workspace_id, user_id):
       
        self.workspace_id = workspace_id
        self.user_id = user_id