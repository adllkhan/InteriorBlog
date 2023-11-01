from sqlalchemy import Column, Integer, String, JSON

from .database import Base


class Card(Base):
    __tablename__ = "card"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    image_dir = Column(String, nullable=False)

