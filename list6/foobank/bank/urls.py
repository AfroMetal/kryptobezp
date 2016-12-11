from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^transfer/transfer', views.transfer),
    url(r'^transfer/verify', views.verify),
    url(r'^transfer/confirmation', views.confirmation),
    url(r'^history', views.history),
    url(r'^admin/confirm_all', views.confirm_all),
    url(r'^admin/confirm_low', views.confirm_low),
    url(r'^$', views.index),
]
