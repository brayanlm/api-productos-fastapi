from typing import List, Optional, Dict, Any
from ..repositories.producto_repository import ProductoRepository
from ..schemas.producto import ProductoCreate, ProductoUpdate


class ProductoService:
    """Servicio para operaciones de productos"""

    @staticmethod
    def listar_productos() -> List[Dict[str, Any]]:
        """Obtiene todos los productos"""
        return ProductoRepository.listar_productos()

    @staticmethod
    def crear_producto(producto: ProductoCreate) -> Optional[Dict[str, Any]]:
        """Crea un nuevo producto"""
        return ProductoRepository.insertar_producto(
            nombre=producto.nombre,
            descripcion=producto.descripcion,
            precio=producto.precio,
            stock=producto.stock,
        )

    @staticmethod
    def obtener_producto(producto_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un producto por su ID"""
        return ProductoRepository.obtener_producto_por_id(producto_id)

    @staticmethod
    def actualizar_producto(
        producto_id: int, producto_update: ProductoUpdate
    ) -> Optional[Dict[str, Any]]:
        """Actualiza un producto existente"""
        return ProductoRepository.actualizar_producto(
            producto_id=producto_id,
            nombre=producto_update.nombre,
            descripcion=producto_update.descripcion,
            precio=producto_update.precio,
            stock=producto_update.stock,
        )

    @staticmethod
    def eliminar_producto(producto_id: int) -> bool:
        """Elimina un producto"""
        return ProductoRepository.eliminar_producto(producto_id)

    @staticmethod
    def existe_producto(producto_id: int) -> bool:
        """Verifica si un producto existe"""
        return ProductoRepository.existe_producto(producto_id)
