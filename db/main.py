import uuid
from typing import List, Annotated
from fastapi import Depends, APIRouter, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

IMAGES_DIR = 'db/images/'

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_database():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

@router.post("/cards/")
async def create_card(
        title: Annotated[str, Form()],
        description: Annotated[str, Form()],
        database: Session = Depends(get_database),
        file: UploadFile = File(...)):

    file.filename = f'{uuid.uuid4()}.jpg'
    contents = await file.read()

    with open(f'{IMAGES_DIR}{file.filename}', 'wb') as f:
        f.write(contents)

    card = {
        'id': str(uuid.uuid4()),
        'title': title,
        'description': description,
        'image_dir': file.filename
    }

    return crud.create_card(database=database, card=card)


@router.get("/cards/", response_model=List[schemas.Card])
def read_cards(skip: int = 0, limit: int = 100, db: Session = Depends(get_database)):
    cards = crud.get_cards(db, skip=skip, limit=limit)
    return cards


@router.get("/cards/{card_id}", response_model=schemas.Card)
def read_card(card_id: str, database: Session = Depends(get_database)):
    card = crud.get_card(database, card_id=card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@router.delete("/cards/{card_id}", response_model=schemas.Card)
def delete_card(card_id: str, database: Session = Depends(get_database)):
    card = crud.get_card(database, card_id=card_id)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return crud.delete_card(database, card_id)
