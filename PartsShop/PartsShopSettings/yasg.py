from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v1',
        description="Market Place Store",
        terms_of_service="https://www.test.com/",
        contact=openapi.Contact(email="some@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(
        permissions.AllowAny,
    ),
)