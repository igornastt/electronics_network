from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from networks_electronics.models.retail_network_models import RetailNetwork
from networks_electronics.paginations import BaseNetworkPagination
from networks_electronics.serializers.retail_network_serializers import RetailNetSerializer, RetailNetCreateSerializer,\
    RetailNetUpdateSerializer
from users.permissions import IsUserActive


class RetailNetCreateAPIView(generics.CreateAPIView):
    serializer_class = RetailNetCreateSerializer
    permission_classes = [IsUserActive]


class RetailNetListAPIView(generics.ListAPIView):
    serializer_class = RetailNetSerializer
    queryset = RetailNetwork.objects.filter(is_active=True)
    permission_classes = [IsUserActive]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact_city', ]
    pagination_class = BaseNetworkPagination


class RetailNetRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = RetailNetSerializer
    queryset = RetailNetwork.objects.all()
    permission_classes = [IsUserActive]


class RetailNetUpdateAPIView(generics.UpdateAPIView):
    serializer_class = RetailNetUpdateSerializer
    queryset = RetailNetwork.objects.all()
    permission_classes = [IsUserActive]


class RetailNetDeleteAPIView(generics.DestroyAPIView):
    serializer_class = RetailNetSerializer
    queryset = RetailNetwork.objects.all()
    permission_classes = [IsUserActive]
