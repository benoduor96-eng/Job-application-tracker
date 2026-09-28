from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import JobApplicationViewSet, health, register
router=DefaultRouter(); router.register('applications',JobApplicationViewSet,basename='applications')
urlpatterns=[path('health/',health),path('auth/register/',register),path('auth/token/',TokenObtainPairView.as_view()),path('auth/token/refresh/',TokenRefreshView.as_view()),path('',include(router.urls))]