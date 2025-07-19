from fastapi import Depends

from src.application.services.post_service import PostService
from src.infarastructure.database.dependencies import get_post_service_impl


def get_post_service(service: PostService = Depends(get_post_service_impl)) -> PostService:
    return service
