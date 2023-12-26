from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .paginations import UserPagination

from users.models import User
from users.permissions import IsUserActive, IsStaffOrSuperuser
from users.serializers import UserSerializer, UserCRUDSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]
    pagination_class = UserPagination


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCRUDSerializer
    permission_classes = [IsUserActive, IsAdminUser]
    pagination_class = UserPagination


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserCRUDSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]
    pagination_class = UserPagination


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserCRUDSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]
    pagination_class = UserPagination


class UserDestroyAPIView(generics.DestroyAPIView):
    serializer_class = UserCRUDSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]
    pagination_class = UserPagination
