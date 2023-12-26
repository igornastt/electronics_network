from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

from users.apps import UsersConfig
from users import views

app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.UserListAPIView.as_view(), name='list_users'),
    path('detail/<int:pk>/', views.UserRetrieveAPIView.as_view(), name='detail_users'),
    path('create/', views.UserCreateAPIView.as_view(), name='create_users'),
    path('update/<int:pk>/', views.UserUpdateAPIView.as_view(), name='update_users'),
    path('delete/<int:pk>/', views.UserDestroyAPIView.as_view(), name='delete_users'),
]
