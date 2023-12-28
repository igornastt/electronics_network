from django.urls import path

from factory.apps import FactoryConfig
from factory.views import FactoryListAPIView, FactoryCreateAPIView, FactoryUpdateAPIView, FactoryRetrieveAPIView, \
    FactoryDeleteAPIView

app_name = FactoryConfig.name

urlpatterns = [
    path("factories/", FactoryListAPIView.as_view(), name='list_factories'),
    path("factories/create/", FactoryCreateAPIView.as_view(), name='create_factory'),
    path("factories/update/<int:pk>/", FactoryUpdateAPIView.as_view(), name='update_factory'),
    path("factories/get/<int:pk>/", FactoryRetrieveAPIView.as_view(), name='get_factory'),
    path("factories/delete/<int:pk>/", FactoryDeleteAPIView.as_view(), name='delete_factory'),

]
