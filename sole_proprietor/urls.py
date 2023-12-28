from django.urls import path

from sole_proprietor.apps import SoleProprietorConfig
from sole_proprietor.views import SoleProprietorListView, SoleProprietorCreateView, SoleProprietorUpdateView, \
    SoleProprietorRetrieveView, SoleProprietorDeleteView

app_name = SoleProprietorConfig.name

urlpatterns = [
    path("", SoleProprietorListView.as_view(), name='list_sole_proprietor'),
    path("create/", SoleProprietorCreateView.as_view(), name='create_sole_proprietor'),
    path("update/<int:pk>/", SoleProprietorUpdateView.as_view(), name='update_sole_proprietor'),
    path("get/<int:pk>/", SoleProprietorRetrieveView.as_view(), name='get_sole_proprietor'),
    path("delete/<int:pk>/", SoleProprietorDeleteView.as_view(), name='delete_sole_proprietor'),
]
