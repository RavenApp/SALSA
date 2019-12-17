from django.db import models
from salsa.settings import RPC_USER, RPC_PASS, ASSET_NAME, OWNER_ACCOUNT, UNIQUE_COST
import json
import math
from ravenrpc import Ravencoin

rvn = Ravencoin(RPC_USER, RPC_PASS)


def gen_valid_unique():
    try:
        next_num = int(rvn.listassets(
            f"{ASSET_NAME}#*")[-1].replace(ASSET_NAME + '#', ''))
    except IndexError:
        next_num = 0
    return f'{ASSET_NAME}#Pickaxe{next_num}'


def get_address():
    return rvn.getnewaddress()['result']


class Player(models.Model):
    player_address = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, default=get_address)
    verified = models.BooleanField(default=False)

    @property
    def player_salsa(self):
        for asset in rvn.getaddressbalance(self.player_address, True)['result']:
            if asset['assetName'] == ASSET_NAME:
                return int(asset['balance'] / 1e8)
        return 0

    @property
    def salsa(self):
        for asset in rvn.getaddressbalance(self.address, True)['result']:
            if asset['assetName'] == ASSET_NAME:
                return int(asset['balance'] / 1e8)
        return 0

    @property
    def rvn_sent(self):
        return rvn.getaddressbalance(self.address)['result']['balance']

    @property
    def pickaxes(self):
        assets = []
        for asset, amount in rvn.listassetbalancesbyaddress(self.player_address)['result'].items():
            if f'{ASSET_NAME}#Pickaxe' in asset:
                assets.append(asset)
        return assets

    def unique(self):
        if self.rvn_sent >= UNIQUE_COST:
            unique = gen_valid_unique()
            rvn.issueunique(ASSET_NAME, [unique])
            rvn.transfer(unique, 1, self.player_address)
            rvn.sendtoaddress(self.address, OWNER_ACCOUNT, UNIQUE_COST - 5.1)

    @property
    def pickaxe_multiplier(self):
        multiplier = 1
        for asset, amount in rvn.listassetbalancesbyaddress(self.player_address)['result'].items():
            if f'{ASSET_NAME}#Pickaxe' in asset:
                multiplier += 1
        return multiplier

    def send_salsa(self):
        salsa = round(1 / (1 + math.exp(-self.salsa / 100000))
                      * 100) * self.pickaxe_multiplier
        rvn.transfer(ASSET_NAME, salsa + 1, self.player_address)

    def verify(self):
        for asset, amount in rvn.listassetbalancesbyaddress(self.address)['result'].items():
            if asset == ASSET_NAME:
                self.verified = True
                self.save()
        rvn.setaccount(self.address, self.address)
