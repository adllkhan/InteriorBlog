from sqlalchemy.orm import Session
from typing import List

from . import models, schemas


def create_card(database: Session, card: schemas.Card):
    database_card = models.Card(**card)
    database.add(database_card)
    database.commit()
    database.refresh(database_card)
    return database_card

def get_cards(database: Session, skip: int = 0, limit: int = 100):
    return database.query(models.Card).offset(skip).limit(limit).all()

def get_card(database: Session, card_id: int):
    return database.query(models.Card).filter(models.Card.id == card_id).first()

# def update_card(database: Session, id: int):
#     card = database.query(models.Card).filter(models.Card.id == id).first()
#     card
#     database_card = models.Card(**card.dict(), id=id)
#     database_card.json

def delete_card(database: Session, card_id: int):
    card = database.query(models.Card).filter(models.Card.id == card_id).first()
    database.delete(card)
    database.commit()
    return card