from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, license, license_domain, license_source, license_restriction

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(license.router, prefix="/license", tags=["license"])
api_router.include_router(license_domain.router, prefix="/license/domain", tags=["license"])
api_router.include_router(license_source.router, prefix="/license/source", tags=["license"])
api_router.include_router(license_restriction.router, prefix="/license/restriction", tags=["license"])
