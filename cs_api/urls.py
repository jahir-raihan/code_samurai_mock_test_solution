from django.urls import path
from .views import UsersApiView, StationsApiView, TrainsApiView, TicketsApiView

urlpatterns = [
    path('users', UsersApiView.as_view(), name='users_api'),
    path('stations', StationsApiView.as_view(), name='stations_api'),
    path('trains', TrainsApiView.as_view(), name='trains_api'),
    path('stations/<int:station_id>/trains', TrainsApiView.as_view(), name='list_train_api'),
    path('wallets/<int:wallet_id>', UsersApiView.as_view(), name='users_api'),
    path('tickets', TicketsApiView.as_view(), name='tickets_api')
]