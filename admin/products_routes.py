from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from database.connection import SessionLocal
from database.models import Product
from sqlalchemy import or_
import json
import io
import csv
from datetime import datetime

router = APIRouter(prefix="/api/products", tags=["products"])

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    currency: str = "COP"
    category: str
    status: str = "AVAILABLE"
    stock: Optional[int] = None
    image_url: Optional[str] = None
    images: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    autoResponse: Optional[str] = None
    paymentLinkMercadoPago: Optional[str] = None
    paymentLinkPayPal: Optional[str] = None
    paymentLinkCustom: Optional[str] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    images: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    autoResponse: Optional[str] = None
    paymentLinkMercadoPago: Optional[str] = None
    paymentLinkPayPal: Optional[str] = None
    paymentLinkCustom: Optional[str] = None

@router.get("")
async def get_products(
    search: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    """Obtener lista de productos con filtros"""
    db = SessionLocal()
    
    try:
        query = db.query(Product)
        
        # Filtros
        if search:
            query = query.filter(
                or_(
                    Product.name.ilike(f"%{search}%"),
                    Product.description.ilike(f"%{search}%")
                )
            )
        
        if category:
            query = query.filter(Product.category == category)
        
        # Status filter solo si existe en el modelo
        if status and hasattr(Product, 'status'):
            query = query.filter(Product.status == status)
        
        # Paginación
        total = query.count()
        products = query.offset(skip).limit(limit).all()
        
        # Convertir a dict y parsear JSON fields
        result = []
        for product in products:
            product_dict = {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "currency": getattr(product, 'currency', 'COP'),
                "category": product.category,
                "status": getattr(product, 'status', 'AVAILABLE'),
                "stock": product.stock,
                "image_url": product.image_url,
                "images": json.loads(product.images) if product.images and isinstance(product.images, str) else (product.images or []),
                "tags": json.loads(product.tags) if hasattr(product, 'tags') and product.tags and isinstance(product.tags, str) else [],
                "autoResponse": getattr(product, 'autoResponse', None),
                "paymentLinkMercadoPago": getattr(product, 'paymentLinkMercadoPago', None),
                "paymentLinkPayPal": getattr(product, 'paymentLinkPayPal', None),
                "paymentLinkCustom": getattr(product, 'paymentLinkCustom', None),
                "views": product.views or 0,
                "sales_count": product.sales_count or 0,
                "createdAt": product.created_at.isoformat() if hasattr(product, 'created_at') and product.created_at else None,
                "updatedAt": product.updated_at.isoformat() if hasattr(product, 'updated_at') and product.updated_at else None
            }
            result.append(product_dict)
        
        return {
            "products": result,
            "total": total,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        print(f"Error getting products: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.post("")
async def create_product(product: ProductCreate):
    """Crear un nuevo producto"""
    db = SessionLocal()
    
    try:
        new_product = Product(
            name=product.name,
            description=product.description,
            price=product.price,
            category=product.category,
            stock=product.stock,
            image_url=product.image_url,
            images=json.dumps(product.images) if product.images else "[]"
        )
        
        # Agregar status solo si existe en el modelo
        if hasattr(Product, 'status'):
            new_product.status = product.status
        
        # Agregar campos opcionales si existen en el modelo
        if hasattr(Product, 'currency'):
            new_product.currency = product.currency
        if hasattr(Product, 'tags'):
            new_product.tags = json.dumps(product.tags) if product.tags else "[]"
        if hasattr(Product, 'autoResponse'):
            new_product.autoResponse = product.autoResponse
        if hasattr(Product, 'paymentLinkMercadoPago'):
            new_product.paymentLinkMercadoPago = product.paymentLinkMercadoPago
        if hasattr(Product, 'paymentLinkPayPal'):
            new_product.paymentLinkPayPal = product.paymentLinkPayPal
        if hasattr(Product, 'paymentLinkCustom'):
            new_product.paymentLinkCustom = product.paymentLinkCustom
        
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        return {
            "id": new_product.id,
            "name": new_product.name,
            "message": "Producto creado exitosamente"
        }
        
    except Exception as e:
        db.rollback()
        print(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get("/{product_id}")
async def get_product(product_id: int):
    """Obtener un producto por ID"""
    db = SessionLocal()
    
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "currency": getattr(product, 'currency', 'COP'),
            "category": product.category,
            "status": product.status,
            "stock": product.stock,
            "image_url": product.image_url,
            "images": json.loads(product.images) if product.images and isinstance(product.images, str) else (product.images or []),
            "tags": json.loads(product.tags) if hasattr(product, 'tags') and product.tags and isinstance(product.tags, str) else [],
            "autoResponse": getattr(product, 'autoResponse', None),
            "paymentLinkMercadoPago": getattr(product, 'paymentLinkMercadoPago', None),
            "paymentLinkPayPal": getattr(product, 'paymentLinkPayPal', None),
            "paymentLinkCustom": getattr(product, 'paymentLinkCustom', None),
            "views": product.views or 0,
            "sales_count": product.sales_count or 0
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting product: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.put("/{product_id}")
async def update_product(product_id: str, product: ProductUpdate):
    """Actualizar un producto"""
    db = SessionLocal()
    
    try:
        db_product = db.query(Product).filter(Product.id == product_id).first()
        
        if not db_product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        # Actualizar campos
        update_data = product.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            if key in ['images', 'tags'] and value is not None:
                setattr(db_product, key, json.dumps(value))
            elif hasattr(db_product, key):
                setattr(db_product, key, value)
        
        db.commit()
        db.refresh(db_product)
        
        return {
            "id": db_product.id,
            "name": db_product.name,
            "message": "Producto actualizado exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error updating product: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.delete("/{product_id}")
async def delete_product(product_id: str):
    """Eliminar un producto"""
    db = SessionLocal()
    
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        db.delete(product)
        db.commit()
        
        return {"message": "Producto eliminado exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error deleting product: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.post("/bulk-delete")
async def bulk_delete_products(product_ids: List[int]):
    """Eliminar múltiples productos"""
    db = SessionLocal()
    
    try:
        deleted_count = db.query(Product).filter(Product.id.in_(product_ids)).delete(synchronize_session=False)
        db.commit()
        
        return {
            "message": f"{deleted_count} productos eliminados exitosamente",
            "count": deleted_count
        }
        
    except Exception as e:
        db.rollback()
        print(f"Error bulk deleting products: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get("/tags/all")
async def get_all_tags():
    """Obtener todos los tags únicos"""
    db = SessionLocal()
    
    try:
        products = db.query(Product).all()
        all_tags = set()
        
        for product in products:
            if hasattr(product, 'tags') and product.tags:
                try:
                    tags = json.loads(product.tags) if isinstance(product.tags, str) else product.tags
                    if isinstance(tags, list):
                        all_tags.update(tags)
                except:
                    pass
        
        return {"tags": sorted(list(all_tags))}
        
    except Exception as e:
        print(f"Error getting tags: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.post("/import")
async def import_products(file: UploadFile = File(...)):
    """Importar productos desde JSON"""
    db = SessionLocal()
    
    try:
        content = await file.read()
        products_data = json.loads(content)
        
        created_count = 0
        for product_data in products_data:
            product = Product(
                name=product_data['name'],
                description=product_data.get('description'),
                price=product_data['price'],
                category=product_data.get('category', 'PHYSICAL'),
                status=product_data.get('status', 'AVAILABLE'),
                stock=product_data.get('stock'),
                image_url=product_data.get('image_url'),
                images=json.dumps(product_data.get('images', []))
            )
            db.add(product)
            created_count += 1
        
        db.commit()
        
        return {
            "message": f"{created_count} productos importados exitosamente",
            "count": created_count
        }
        
    except Exception as e:
        db.rollback()
        print(f"Error importing products: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get("/export/json")
async def export_products_json():
    """Exportar productos a JSON"""
    db = SessionLocal()
    
    try:
        products = db.query(Product).all()
        
        products_data = []
        for product in products:
            products_data.append({
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": product.category,
                "status": product.status,
                "stock": product.stock,
                "image_url": product.image_url,
                "images": json.loads(product.images) if product.images and isinstance(product.images, str) else []
            })
        
        json_str = json.dumps(products_data, indent=2, ensure_ascii=False)
        
        return StreamingResponse(
            io.BytesIO(json_str.encode('utf-8')),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename=products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"}
        )
        
    except Exception as e:
        print(f"Error exporting products: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
