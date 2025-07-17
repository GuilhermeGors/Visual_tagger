from fastapi import APIRouter
from backend.src.api.v1.endpoints import analyze

v1_router = APIRouter(prefix="/v1", tags=["v1"]) # Prefixo e tags para a versão 1

v1_router.include_router(analyze.router)

# Você pode adicionar mais routers específicos da v1 aqui, se tiver outros arquivos em `endpoints/`
# v1_router.include_router(outro_modulo.router)