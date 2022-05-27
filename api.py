from binance.client import Client
from binance import ThreadedWebsocketManager
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.helpers import round_step_size
import requests
import time
import numpy as np

client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

print("Client initialized")

# The following functions uses all the balance available (well 95%) in the ISOLATED account to open/close the corresponding balance

def go_long(pair):
    
    # Get available USDT
    qty = np.multiply(float(client.get_isolated_margin_account(symbols=pair)['assets'][0]['quoteAsset']['free']),0.95)
    # Get price
    price = float(requests.get('https://api.binance.com/api/v1/ticker/price?symbol='+pair).json()['price'])
    # Round
    qty = round_step_size(np.divide(qty,price), lotsize[pair])
    print("QTY: ", qty)
    
    order = client.create_margin_order(
        symbol=pair,
        quantity=qty,
        isIsolated='TRUE',
        side='BUY',
        sideEffectType = 'MARGIN_BUY',
        type='MARKET')
    
def close_long(pair):
    
    # Get available BASE
    qty = np.multiply(float(client.get_isolated_margin_account(symbols=pair)['assets'][0]['baseAsset']['free']),0.95)
    # Round
    qty = round_step_size(qty, lotsize[pair])
    
    order = client.create_margin_order(
        symbol=pair,
        quantity=qty,
        isIsolated='TRUE',
        side='SELL',
        sideEffectType = 'AUTO_REPAY',
        type='MARKET')
def go_short(pair):
    
    # Get available USDT
    qty = np.multiply(float(client.get_isolated_margin_account(symbols=pair)['assets'][0]['quoteAsset']['free']),0.95)
    # Get price
    price = float(requests.get('https://api.binance.com/api/v1/ticker/price?symbol='+pair).json()['price'])
    # Round
    qty = round_step_size(np.divide(qty,price), lotsize[pair])
    print("QTY: ", qty)
    
    loan = client.create_margin_loan(asset=pair[:-4], symbol=pair, isIsolated='TRUE', amount=qty)
    order = client.create_margin_order(
        symbol=pair,
        quantity=qty,
        isIsolated='TRUE',
        side='SELL',
        sideEffectType = 'MARGIN_BUY',
        type='MARKET')
    
def close_short(pair):
    
    # Get available BASE
    acc = client.get_isolated_margin_account(symbols=pair)['assets'][0]['baseAsset']
    qty = float(acc['borrowed'])+float(acc['interest'])
    print(qty)
    # Round
    qty = round_step_size(qty, lotsize[pair])
    print("QTY: ", qty)
    
    order = client.create_margin_order(
        symbol=pair,
        quantity=qty,
        isIsolated='TRUE',
        side='BUY',
        sideEffectType = 'AUTO_REPAY',
        type='MARKET')
