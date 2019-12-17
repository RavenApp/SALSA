#!/usr/bin/python3.7
import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'salsa.settings'
import django; django.setup()

from sell.models import Player
from salsa.settings import RPC_PASS, RPC_USER, ASSET_NAME

from ravenrpc import Ravencoin

rvn = Ravencoin(RPC_USER, RPC_PASS)

def verify():
    for p in Player.objects.filter(verified=False):
        p.verify()

def unique():
    for p in Player.objects.filter(verified=True):
        p.unique()

def send_if_zero_bal():
    for p in Player.objects.filter(verified=True):
        if p.salsa == 0:
            rvn.transfer(ASSET_NAME, 10, p.player_address)

if __name__ == '__main__':
    verify()
    unique()