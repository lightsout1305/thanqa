from django.urls import path
from api import views

urlpatterns = [
    path("users/login/", views.LoginAPIView.as_view(), name='login'),
]
