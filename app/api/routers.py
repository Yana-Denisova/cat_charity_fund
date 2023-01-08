from fastapi import APIRouter

from app.api.endpoints import user_router, project_router, donation_router


main_router = APIRouter()

main_router.include_router(
    project_router, prefix='/charity_project', tags=['Charity projects']
)
main_router.include_router(
    donation_router, prefix='/donation', tags=['Donation']
)
main_router.include_router(user_router)