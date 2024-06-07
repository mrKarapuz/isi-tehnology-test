from drf_spectacular.utils import extend_schema
from djoser.views import UserViewSet


@extend_schema(tags=['users'])
class CustomUserViewSet(UserViewSet):
    pass
