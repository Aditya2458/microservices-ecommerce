from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import Product, ProductResponse
import app.models as models
from app.database import get_db

router = APIRouter()


# CREATE
@router.post("/products", response_model=ProductResponse)
def create_product(product: Product, db: Session = Depends(get_db)):
    
    new_product = models.Product(
        name=product.name,
        price=product.price,
        description=product.description
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# READ ALL
@router.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


# UPDATE
@router.put("/products/{id}", response_model=ProductResponse)
def update_product(id: int, product: Product, db: Session = Depends(get_db)):
    
    existing_product = db.query(models.Product).filter(models.Product.id == id).first()

    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    existing_product.name = product.name
    existing_product.price = product.price
    existing_product.description = product.description

    db.commit()
    db.refresh(existing_product)

    return existing_product


# DELETE
@router.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):

    product = db.query(models.Product).filter(models.Product.id == id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()

    return {"message": "Product deleted"}