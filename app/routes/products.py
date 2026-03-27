from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import Product
import app.models as models
from app.database import get_db
from typing import List
from app.schemas import ProductResponse
from fastapi import HTTPException


router = APIRouter()

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

    return {"message": "Product saved"}


@router.get("/products",response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.product).all()


@router.put("/products/{id}",response_model=ProductResponse)
def update_product(id:int, product:Product,db: Session=Depends(get_db)):
     existing_product= db.query(models,product).filter(models.product.id == id ).first()

     if not existing_product:
         raise HTTPException(status_code=404,details= "product not found")
     
     existing_product.name=product.name
     existing_product.price=product.price
     existing_product.description=product.description

     return existing_product

     

     
