# apps/models.py
from apps import db
from sqlalchemy.orm import relationship
class DefaultCategory(db.Model):
    __tablename__ = 'default_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<DefaultCategory {self.name} {self.id}>'
