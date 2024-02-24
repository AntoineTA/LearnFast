from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import api

urlpatterns = [
    path('users', api.UserList.as_view(), name='users'),
    path('profile', api.UserDetail.as_view(), name='profile'),
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui', SpectacularSwaggerView.as_view(url_name='api:schema'), name='swagger-ui'),
]