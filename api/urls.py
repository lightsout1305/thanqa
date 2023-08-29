"""
Модуль с URL-адресами приложения api
"""
from django.urls import path
from api import views

urlpatterns = [
    path("users/login/", views.LoginAPIView.as_view(), name='login'),
    path("testplan/create/", views.CreateTestPlanAPIView.as_view(), name='create_test_plan'),
    path("testplan/update/", views.UpdateTestPlanApiView.as_view(), name='update_test_plan'),
    path("testplan/delete/", views.DeleteTestPlanApiView.as_view(), name='delete_test_plan'),
    path("testplan/current/", views.GetTestPlanView.as_view(), name='current_test_plan'),
]
