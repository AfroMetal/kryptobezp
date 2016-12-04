from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Transfer, TransferForm


@login_required
def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST, request.FILES)
    else:
        form = TransferForm()
    return render(request, 'bank/transfer.html', {'form': form})


@login_required
def verify(request):
    if request.method == 'GET':
        form = TransferForm(request.GET, request.FILES)
        return render(request, 'bank/verify.html', {'form': form})
    elif request.method == 'POST':
        form = TransferForm(request.POST, request.FILES)
        if form.is_valid():
            valid_form = form.save(commit=False)
            valid_form.user = request.user
            valid_form.save()
            return HttpResponseRedirect('/bank/transfer/confirmation')
    else:
        form = TransferForm()
        return render(request, 'bank/transfer.html', {'form': form})


@login_required
def confirmation(request):
    transfers = Transfer.objects.filter(user=request.user).order_by('post_time').reverse()[0:1]
    for t in transfers:
        t.post_time = t.post_time.strftime('%c')
    return render(request, 'bank/history.html', {'transfers': transfers})


@login_required
def history(request):
    user_transfers = Transfer.objects.all().filter(user=request.user)[:10]
    for t in user_transfers:
        t.post_time = t.post_time.strftime('%c')
    return render(request, 'bank/history.html', {'transfers': user_transfers})


@login_required
def index(request):
    return render(request, 'bank/index.html', {'user': request.user})
