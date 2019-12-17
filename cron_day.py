#!/usr/bin/python3.7
import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'salsa.settings'
import django; django.setup()

from sell.models import Player
from salsa.settings import RPC_PASS, RPC_USER, ASSET_NAME

from ravenrpc import Ravencoin

rvn = Ravencoin(RPC_USER, RPC_PASS)

def send_salsa():
    for p in Player.objects.filter(verified=True):
        p.send_salsa()

if __name__ == '__main__':
    send_salsa()