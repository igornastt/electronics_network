from django.views.generic import ListView
from rest_framework.permissions import IsAdminUser

from users.permissions import IsUserActive
from products.models import Product
from products.paginations import ProductPagination
from products.serializers import ProductSmallSerializer


class ProductListView(ListView):
    model = Product
    serializer_class = ProductSmallSerializer
    permission_classes = [IsUserActive, IsAdminUser]
    pagination_class = ProductPagination
