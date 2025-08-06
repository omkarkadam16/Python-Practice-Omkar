from django.urls import path, include
from rest_framework import routers
from .views import HomeChefViewSet, MenuItemViewSet

router = routers.DefaultRouter()
router.register(r'chefs', HomeChefViewSet)
router.register(r'menu', MenuItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
