from fastapi import APIRouter, HTTPException, status
from typing import List

from ..schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from ..services.producto_service import ProductoService

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("/", response_model=List[ProductoResponse])
def get_productos():
    try:
        productos = ProductoService.listar_productos()
        return productos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar productos: {str(e)}",
        )


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def create_producto(producto: ProductoCreate):
    try:
        result = ProductoService.crear_producto(producto)

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo obtener el producto creado",
            )

        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al insertar producto: {str(e)}",
        )


@router.put("/{producto_id}", response_model=ProductoResponse)
def update_producto(producto_id: int, producto_update: ProductoUpdate):
    try:
        # Verificar que el producto existe
        if not ProductoService.existe_producto(producto_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {producto_id} no encontrado",
            )

        # Ejecutar actualización
        result = ProductoService.actualizar_producto(producto_id, producto_update)

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo obtener el producto actualizado",
            )

        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar producto: {str(e)}",
        )


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(producto_id: int):
    try:
        # Verificar que el producto existe
        if not ProductoService.existe_producto(producto_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con id {producto_id} no encontrado",
            )

        # Ejecutar eliminación
        ProductoService.eliminar_producto(producto_id)
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar producto: {str(e)}",
        )
