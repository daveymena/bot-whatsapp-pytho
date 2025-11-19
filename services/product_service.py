from sqlalchemy.orm import Session
from database.models import Product
from typing import List, Optional

class ProductService:
    @staticmethod
    def get_all_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
        return db.query(Product).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    def search_products(db: Session, query: str) -> List[Product]:
        search = f"%{query}%"
        return db.query(Product).filter(
            (Product.name.ilike(search)) | 
            (Product.description.ilike(search))
        ).all()
    
    @staticmethod
    def get_products_by_category(db: Session, category: str) -> List[Product]:
        return db.query(Product).filter(Product.category == category).all()
    
    @staticmethod
    def get_digital_products(db: Session) -> List[Product]:
        return db.query(Product).filter(Product.is_digital == True).all()
    
    @staticmethod
    def get_dropshipping_products(db: Session) -> List[Product]:
        return db.query(Product).filter(Product.is_dropshipping == True).all()
    
    @staticmethod
    def create_product(db: Session, product_data: dict) -> Product:
        product = Product(**product_data)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    
    @staticmethod
    def update_stock(db: Session, product_id: int, quantity: int) -> Optional[Product]:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.stock = quantity
            db.commit()
            db.refresh(product)
        return product
