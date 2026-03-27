from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    description: str


class ProductResponse(BaseModel):
    id : str
    name : str
    price : float
    description: str

    class Config:
        orm_mode=True
    
