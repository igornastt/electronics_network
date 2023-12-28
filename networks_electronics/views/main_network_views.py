from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from networks_electronics.models.main_network_models import MainNetwork
from networks_electronics.paginations import BaseNetworkPagination
from networks_electronics.serializers.main_network_serializers import MainNetworkSerializer, MainNetworkCreateSerializer, \
    MainNetworkUpdateSerializer
from users.permissions import IsUserActive


class MainNetCreateAPIView(generics.CreateAPIView):
    serializer_class = MainNetworkCreateSerializer
    queryset = MainNetwork.objects.all()
    permission_classes = [IsUserActive]


class MainNetListView(generics.ListAPIView):
    serializer_class = MainNetworkSerializer
    queryset = MainNetwork.objects.filter(is_active=True)
    permission_classes = [IsUserActive]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact_city', ]
    pagination_class = BaseNetworkPagination


class MainNetUpdateAPIView(generics.UpdateAPIView):
    serializer_class = MainNetworkUpdateSerializer
    queryset = MainNetwork.objects.all()
    permission_classes = [IsUserActive]


class MainNetRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = MainNetworkSerializer
    queryset = MainNetwork.objects.all()
    permission_classes = [IsUserActive]


class MainNetDeleteAPIView(generics.DestroyAPIView):
    serializer_class = MainNetworkSerializer
    queryset = MainNetwork.objects.all()
    permission_classes = [IsUserActive]
