from djmoney.models import fields as moneymodels
from django.db import models
from django.conf import settings
from django.forms import ModelForm


class Transfer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False)
    acc_num_from = models.CharField('from account number', max_length=28)
    amount = moneymodels.MoneyField('transfer amount', max_digits=12, decimal_places=2, default_currency='PLN')
    acc_num_to = models.CharField('to account number', max_length=28)
    rec_name = models.CharField('receiver name', max_length=120)
    rec_street = models.CharField('street', max_length=64)
    rec_pcode = models.CharField('postcode', max_length=6)
    rec_city = models.CharField('city', max_length=32)
    title = models.TextField('title', max_length=140)
    post_time = models.DateTimeField('transfer date', auto_now=False, auto_now_add=True, editable=False)


class TransferForm(ModelForm):
    class Meta:
        model = Transfer
        fields = ['acc_num_from', 'amount', 'acc_num_to', 'rec_name', 'rec_street', 'rec_pcode', 'rec_city', 'title']
