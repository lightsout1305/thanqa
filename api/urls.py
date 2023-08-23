from django.urls import path
from api import views

urlpatterns = [
    path("users/login/", views.LoginAPIView.as_view(), name='login'),
    path("testplan/create/", views.CreateTestPlanAPIView.as_view(), name='create_test_plan'),
]
