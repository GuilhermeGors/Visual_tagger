from fastapi import APIRouter
from backend.src.api.v1 import v1_router

# Este router pode ser usado para agrupar todas as versões da API, se houver múltiplas (ex: /api/v1, /api/v2)
api_router = APIRouter(prefix="/api")

# Inclui o router da versão 1
api_router.include_router(v1_router)

# No futuro, você pode adicionar outras versões da API aqui:
# from backend.src.api.v2 import v2_router
# api_router.include_router(v2_router)