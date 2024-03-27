from NorenRestApiPy.NorenApi import NorenApi
import pyotp
from threading import Timer
import pandas as pd
import time
import concurrent.futures

api = None

#
# class Order:
#     def __init__(self, buy_or_sell: str = None, product_type: str = None,
#                  exchange: str = None, tradingsymbol: str = None,
#                  price_type: str = None, quantity: int = None,
#                  price: float = None, trigger_price: float = None, discloseqty: int = 0,
#                  retention: str = 'DAY', remarks: str = "tag",
#                  order_id: str = None):
#         self.buy_or_sell = buy_or_sell
#         self.product_type = product_type
#         self.exchange = exchange
#         self.tradingsymbol = tradingsymbol
#         self.quantity = quantity
#         self.discloseqty = discloseqty
#         self.price_type = price_type
#         self.price = price
#         self.trigger_price = trigger_price
#         self.retention = retention
#         self.remarks = remarks
#         self.order_id = None
#
#
# # print(ret)
#
#
# def get_time(time_string):
#     data = time.strptime(time_string, '%d-%m-%Y %H:%M:%S')
#
#     return time.mktime(data)


class ShoonyaApiPy(NorenApi):
    def __init__(self):
        NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/',
                          websocket='wss://api.shoonya.com/NorenWSTP/')

        global api
        api = self

    def generateTotp(self,token):
        totp = pyotp.TOTP(token)
        return totp.now()
