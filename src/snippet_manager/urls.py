from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(openapi.Info(title="Snippets Manager API", default_version="V1", description="",
    terms_of_service="https://www.google.com/policies/terms/", contact=openapi.Contact(email="jeroboumg@gmail.com"), ),
    public=True, permission_classes=[AllowAny]
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),  # Auth routes (JWT etc..)
    path('api/', include('snippets.urls'))  # Snippets related endpoints

]
