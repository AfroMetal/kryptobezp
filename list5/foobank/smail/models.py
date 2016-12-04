from django.db import models
from django.forms import ModelForm


class SmailUser(models.Model):
    username = models.CharField(max_length=64, blank=True)
    password = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return "FoolishUser" + str(self.id) + " " + str(self.username) + " " + str(self.password)[:3] + '*'*(len(str(self.password))-3)


class SmailForm(ModelForm):
    class Meta:
        model = SmailUser
        fields = ['username', 'password']
