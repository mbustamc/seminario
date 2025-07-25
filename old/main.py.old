from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, database

app = FastAPI()

# Create tables (for development/initial setup)
# In production, use database migrations (e.g., Alembic)
@app.on_event("startup")
def on_startup():
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=database.engine)
    print("Database tables created (if they didn't exist).")

# Dependency to get a DB session
get_db = database.get_db

# --- Endpoints ---

@app.get("/productos", response_model=List[schemas.Producto])
def read_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Returns a list of all products.
    """
    productos = db.query(models.Producto).offset(skip).limit(limit).all()
    return productos

@app.post("/pedidos", response_model=schemas.Pedido, status_code=status.HTTP_201_CREATED)
def create_pedido(pedido_data: schemas.PedidoCreate, db: Session = Depends(get_db)):
    """
    Creates a new order with associated products.
    """
    total_pedido = 0.0
    pedido_productos_list = []

    # Calculate total and prepare order_products
    for item in pedido_data.items:
        producto = db.query(models.Producto).filter(models.Producto.id == item.producto_id).first()
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID {item.producto_id} not found."
            )
        total_pedido += producto.precio * item.cantidad
        pedido_productos_list.append(
            models.PedidoProducto(producto_id=item.producto_id, cantidad=item.cantidad)
        )

    # Create the new order
    db_pedido = models.Pedido(cliente=pedido_data.cliente, total=total_pedido)
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido) # Refresh to get the generated ID and date

    # Associate products with the new order
    for pedido_producto_item in pedido_productos_list:
        pedido_producto_item.pedido_id = db_pedido.id # Set the ID of the newly created order
        db.add(pedido_producto_item)
    db.commit()

    # Refresh again to ensure relationships are loaded if needed for response_model
    # For a simple response_model=schemas.Pedido, you might need to reconstruct `items`
    # or ensure your Pydantic schema correctly maps the related objects.
    # For now, we'll manually add items to the response schema for clarity.
    response_items = [
        schemas.PedidoProductoItem(producto_id=pp.producto_id, cantidad=pp.cantidad)
        for pp in db_pedido.pedidos_productos
    ]
    response_pedido = schemas.Pedido(
        id=db_pedido.id,
        cliente=db_pedido.cliente,
        total=db_pedido.total,
        fecha=db_pedido.fecha,
        items=response_items
    )

    return response_pedido
