from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from networks_electronics.paginations import BaseNetworkPagination
from sole_proprietor.models import SoleProprietor
from sole_proprietor.serializers import SoleProprietorSerializer, SoleProprietorCreateSerializer, \
    SoleProprietorUpdateSerializer
from users.permissions import IsUserActive


class SoleProprietorCreateView(generics.CreateAPIView):
    serializer_class = SoleProprietorCreateSerializer
    permission_classes = [IsUserActive]


class SoleProprietorListView(generics.ListAPIView):
    serializer_class = SoleProprietorSerializer
    queryset = SoleProprietor.objects.filter(is_active=True)
    permission_classes = [IsUserActive]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact_city', ]
    pagination_class = BaseNetworkPagination


class SoleProprietorUpdateView(generics.UpdateAPIView):
    serializer_class = SoleProprietorUpdateSerializer
    queryset = SoleProprietor.objects.all()
    permission_classes = [IsUserActive]


class SoleProprietorRetrieveView(generics.RetrieveAPIView):
    serializer_class = SoleProprietorSerializer
    queryset = SoleProprietor.objects.all()
    permission_classes = [IsUserActive]


class SoleProprietorDeleteView(generics.DestroyAPIView):
    serializer_class = SoleProprietorSerializer
    queryset = SoleProprietor.objects.all()
    permission_classes = [IsUserActive]
