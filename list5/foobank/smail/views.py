from django.shortcuts import render
from .models import SmailForm
# Create your views here.


def smail(request):
    if request.method == 'POST':
        user = SmailForm(request.POST, request.FILES)
        user.save()
        return render(request, 'smail/smail.html', {'fool': 'true'})
    return render(request, 'smail/smail.html')
