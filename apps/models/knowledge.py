# # apps/models.py
# from apps import db
# from sqlalchemy.orm import relationship
# class Knowledge(db.Model):
#     __tablename__ = 'knowledge'

#     _id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=db.uuid.uuid4)
#     knowledge_name = db.Column(db.String)
#     knowledge_description = db.Column(db.String)
#     knowledge_information = db.Column(db.String)
#     characters = db.Column(db.JSON, db.ForeignKey('characters.id'))
#     user_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('users.id'))
#     workspace_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('workspaces.id'))
#     character = relationship('Character', back_populates='knowledge')

#     def __init__(self, knowledge_name, knowledge_description, knowledge_information, characters, user_id, workspace_id):
#         self.knowledge_name = knowledge_name
#         self.knowledge_description = knowledge_description
#         self.knowledge_information = knowledge_information
#         self.characters = characters
#         self.workspace_id = workspace_id
#         self.user_id = user_id



from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

class Knowledge(db.Model):
    __tablename__ = 'knowledge'

    _id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    knowledge_name = db.Column(db.String)
    knowledge_description = db.Column(db.String)
    knowledge_information = db.Column(db.String)
    characters = db.Column(db.JSON, db.ForeignKey('characters.id'))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    workspace_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('workspaces.id'))
    character = db.relationship('Character', back_populates='knowledge')

    def __init__(self, knowledge_name, knowledge_description, knowledge_information, characters, user_id, workspace_id, character):
        self.knowledge_name = knowledge_name
        self.knowledge_description = knowledge_description
        self.knowledge_information = knowledge_information
        self.characters = characters
        self.workspace_id = workspace_id
        self.user_id = user_id
        self.character = character


