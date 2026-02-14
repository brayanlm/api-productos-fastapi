from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    stock: int


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None


class ProductoResponse(ProductoBase):
    id: int
    fechaRegistro: datetime

    class Config:
        from_attributes = True
