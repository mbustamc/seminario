from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base # Relative import

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
    descripcion = Column(String, nullable=True)

    pedidos_productos = relationship("PedidoProducto", back_populates="producto")

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String)
    total = Column(Float)
    fecha = Column(DateTime, default=func.now())

    pedidos_productos = relationship("PedidoProducto", back_populates="pedido")

class PedidoProducto(Base):
    __tablename__ = "pedido_productos"

    pedido_id = Column(Integer, ForeignKey("pedidos.id"), primary_key=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), primary_key=True)
    cantidad = Column(Integer)

    pedido = relationship("Pedido", back_populates="pedidos_productos")
    producto = relationship("Producto", back_populates="pedidos_productos")
