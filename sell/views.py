from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from .models import Player
from salsa.settings import RPC_USER, RPC_PASS
from ravenrpc import Ravencoin

rvn = Ravencoin(RPC_USER, RPC_PASS)

def index(request):
    return render(request, 'index.html', {'players': Player.objects.order_by('-salsa')})

def create(request):
    if request.method == 'POST':
        try:
            p = Player(player_address=request.POST['address'])
            if Player.objects.filter(player_address=p.player_address):
                return HttpResponseRedirect('/dashboard/?addr=' + p.player_address)
            p.save()
        except IndexError:
            return
        return render(request, 'verify.html', {'player': p})
    return render(request, 'create.html')

def dashboard(request, pk):
    try:
        p = Player.objects.get(pk=pk)
    except Player.DoesNotExist:
        raise Http404
    if p.verified:
        return render(request, 'dashboard.html', {'p': p})
    else:
        return render(request, 'notverified.html', {'player': p})

def howto(request):
    return render(request, 'how-to.html')

def find_dash(request):
    addr = request.GET.get('addr', False)
    if addr:
        pk = Player.objects.filter(player_address=addr)[0].pk
        return HttpResponseRedirect(f'/dashboard/{pk}/')
    return render(request, 'find.html')
