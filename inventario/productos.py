from sqlalchemy import Column, Integer, String, Float
from .bd import Base


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    autor = Column(String)
    cantidad = Column(Integer)
    precio = Column(Float)