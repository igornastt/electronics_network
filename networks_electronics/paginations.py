from rest_framework.pagination import PageNumberPagination


class BaseNetworkPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 50
    page_query_param = 'page_size'
