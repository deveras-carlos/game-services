# /models/models.py
from sqlalchemy import Column, Integer, String
from .base_model import BaseModel  # Import Base from the database config

class MenuTextModel(BaseModel):
    __tablename__ = 'menu_text'

    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, nullable=False)
    en = Column(String, nullable=False)
    pt = Column(String, nullable=False)
