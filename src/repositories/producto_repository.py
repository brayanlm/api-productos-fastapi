from sqlalchemy import text
from typing import List, Optional, Dict, Any
from ..config.database import engine


class ProductoRepository:
    """Repositorio para operaciones de productos usando procedimientos almacenados"""

    @staticmethod
    def listar_productos() -> List[Dict[str, Any]]:
        """Obtiene todos los productos usando sp_listar_productos"""
        with engine.connect() as connection:
            result = connection.execute(text("EXEC sp_listar_productos"))
            productos = []
            for row in result.mappings():
                productos.append(
                    {
                        "id": row["id"],
                        "nombre": row["nombre"],
                        "descripcion": row["descripcion"],
                        "precio": float(row["precio"]),
                        "stock": row["stock"],
                        "fechaRegistro": row["fechaRegistro"],
                    }
                )
            return productos

    @staticmethod
    def insertar_producto(
        nombre: str, descripcion: Optional[str], precio: float, stock: int
    ) -> Optional[Dict[str, Any]]:
        """Inserta un nuevo producto usando sp_insertar_producto"""
        with engine.connect() as connection:
            query = text("""
                EXEC sp_insertar_producto 
                    @nombre = :nombre,
                    @descripcion = :descripcion,
                    @precio = :precio,
                    @stock = :stock
            """)
            result = connection.execute(
                query,
                {
                    "nombre": nombre,
                    "descripcion": descripcion,
                    "precio": precio,
                    "stock": stock,
                },
            )
            connection.commit()

            # Obtener el producto insertado
            row = result.mappings().first()
            if row:
                return {
                    "id": row["id"],
                    "nombre": row["nombre"],
                    "descripcion": row["descripcion"],
                    "precio": float(row["precio"]),
                    "stock": row["stock"],
                    "fechaRegistro": row["fechaRegistro"],
                }

            # Si el SP no retorna datos, consultamos el último registro
            result = connection.execute(
                text("SELECT TOP 1 * FROM Productos ORDER BY id DESC")
            )
            row = result.mappings().first()
            if row:
                return {
                    "id": row["id"],
                    "nombre": row["nombre"],
                    "descripcion": row["descripcion"],
                    "precio": float(row["precio"]),
                    "stock": row["stock"],
                    "fechaRegistro": row["fechaRegistro"],
                }
            return None

    @staticmethod
    def actualizar_producto(
        producto_id: int,
        nombre: str,
        descripcion: Optional[str],
        precio: float,
        stock: int,
    ) -> Optional[Dict[str, Any]]:
        """Actualiza un producto usando sp_actualizar_producto"""
        with engine.connect() as connection:
            query = text("""
                EXEC sp_actualizar_producto 
                    @id = :id,
                    @nombre = :nombre,
                    @descripcion = :descripcion,
                    @precio = :precio,
                    @stock = :stock
            """)
            connection.execute(
                query,
                {
                    "id": producto_id,
                    "nombre": nombre,
                    "descripcion": descripcion,
                    "precio": precio,
                    "stock": stock,
                },
            )
            connection.commit()

            # Obtener el producto actualizado
            result = connection.execute(
                text("SELECT * FROM Productos WHERE id = :id"), {"id": producto_id}
            )
            row = result.mappings().first()

            if row:
                return {
                    "id": row["id"],
                    "nombre": row["nombre"],
                    "descripcion": row["descripcion"],
                    "precio": float(row["precio"]),
                    "stock": row["stock"],
                    "fechaRegistro": row["fechaRegistro"],
                }
            return None

    @staticmethod
    def eliminar_producto(producto_id: int) -> bool:
        """Elimina un producto usando sp_eliminar_producto"""
        with engine.connect() as connection:
            query = text("EXEC sp_eliminar_producto @id = :id")
            connection.execute(query, {"id": producto_id})
            connection.commit()
            return True

    @staticmethod
    def obtener_producto_por_id(producto_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene un producto por su ID"""
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT * FROM Productos WHERE id = :id"), {"id": producto_id}
            )
            row = result.mappings().first()
            if row:
                return {
                    "id": row["id"],
                    "nombre": row["nombre"],
                    "descripcion": row["descripcion"],
                    "precio": float(row["precio"]),
                    "stock": row["stock"],
                    "fechaRegistro": row["fechaRegistro"],
                }
            return None

    @staticmethod
    def existe_producto(producto_id: int) -> bool:
        """Verifica si un producto existe"""
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT id FROM Productos WHERE id = :id"), {"id": producto_id}
            )
            return result.fetchone() is not None
