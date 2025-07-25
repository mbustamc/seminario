from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# --- Producto Schemas ---

class ProductoBase(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = None

class ProductoCreate(ProductoBase):
    pass # No extra fields for creation currently

class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True # Was orm_mode = True in older Pydantic versions

# --- Pedido Schemas ---

class PedidoProductoItem(BaseModel):
    producto_id: int
    cantidad: int

class PedidoCreate(BaseModel):
    cliente: str
    items: List[PedidoProductoItem]

class Pedido(BaseModel):
    id: int
    cliente: str
    total: float
    fecha: datetime
    items: List[PedidoProductoItem] = [] # To include details of products in the order

    class Config:
        from_attributes = True
