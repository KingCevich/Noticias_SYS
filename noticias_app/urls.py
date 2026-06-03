from django.urls import path, include
from .views import lista_noticias, NoticiasViewSet
from . import views 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'noticias', NoticiasViewSet)


urlpatterns = [
    path('noticias/', lista_noticias, name='lista_noticias'),
    path('api/', include(router.urls)),
]