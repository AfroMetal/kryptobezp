from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^transfer/transfer', views.transfer),
    url(r'^transfer/verify', views.verify),
    url(r'^transfer/confirmation', views.confirmation),
    url(r'^history', views.history),
    url(r'^admin/confirm_all', views.confirm_all),
    url(r'^$', views.index),
]
