from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (index, MenuItemView, SingleMenuItemView, BookingViewSet)


router = DefaultRouter()
router.register(r'tables', BookingViewSet)


urlpatterns = [
    path('', index, name="home"),
    path('menu/', MenuItemView.as_view(), name="menu"),
    path('menu/<int:pk>', SingleMenuItemView.as_view()),
    path('booking/', include(router.urls)),
    
]
