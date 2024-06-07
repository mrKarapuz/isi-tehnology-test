from django.contrib import admin
from django.urls import include
from django.urls import path
from django.conf.urls.static import static
from app import settings
from base import views as base_views
from chat import views as chat_views
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from drf_spectacular.views import SpectacularRedocView
from rest_framework.routers import SimpleRouter

router = SimpleRouter(trailing_slash=True)
router.register('users', base_views.CustomUserViewSet)
router.register('threads', chat_views.ThreadView)
router.register('messages', chat_views.MessageView)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("djoser.urls.jwt")),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path("docs/", SpectacularSwaggerView.as_view(url_name="schema")),
        path("re/docs/", SpectacularRedocView.as_view(url_name="schema")),
    ]
