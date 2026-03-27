from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import Product
import app.models as models
from app.database import get_db

router = APIRouter()

@router.post("/products")
def create_product(product: Product, db: Session = Depends(get_db)):
    
    new_product = models.Product(
        name=product.name,
        price=product.price,
        description=product.description
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"message": "Product saved"}