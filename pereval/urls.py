from django.urls import path
from .views import PerevalDetail, PerevalList, PerevalAdd, PerevalUpdate

urlpatterns = [
    path('submitData/', PerevalAdd.as_view(), name='pereval-add'),
    path('submitData/<int:id>/', PerevalDetail.as_view(), name='pereval-detail'),
    path('submitData/<int:id>', PerevalUpdate.as_view(), name='pereval-update'),
    path('submitData/<str:email>/', PerevalList.as_view(), name='pereval-list'),
]