from datetime import datetime, timedelta
import pandas as pd
from NorenRestApiPy.NorenApi import NorenApi

from boot import *


api = ShoonyaApiPy()


class userBackend:

    def login(self, user, pwd, token, vc, app_key, imei):
        print(user,pwd,token,vc,app_key,imei)
        # user = "FA137726"
        # pwd = "Mali@13"
        # factor2 = api.generateTotp("6755I3PZ6L6GE2K7KBU2G2373Y2565H6")
        # # factor2 = "AGFPM9510L"
        # vc = "FA137726_U"
        # app_key = "632b447eada0340705dd4318db03ce5f"
        # imei = "abc1234"

        # user = "FA164238"
        # pwd = "Mali@2002"
        # factor2 = api.generateTotp("7GS74W7L7X72I2RDK26EEKC75YGMW27D")
        # # factor2 = "AGFPM9510L"
        # vc = "FA164238_U"
        # app_key = "af998eb04b0b4e63ed1b8618e6ca77af"
        # imei = "abc1234"

        user = user
        pwd = pwd
        factor2 = api.generateTotp(token)
        vc = vc
        app_key = app_key
        imei = imei
        print("TRYING LOGIN")

        ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)
        print(ret)
        print(api.get_positions())
        print(api.get_order_book())
        return api

    # def positions(self, user):
    #     positions = api.get_positions()
    #     return positions
    #
    # def orderBook(self, user):
    #     obk = api.get_order_book()
    #     return obk

    # def __init__(self):
    #     NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/',
    #                       websocket='wss://api.shoonya.com/NorenWSTP/')
    #
    #     global api
    #     api = self
    #
    # def generateTotp(self, token):
    #     totp = pyotp.TOTP(token)
    #     return totp.now()

# # Trade Book
# trdbk = api.get_trade_book()


# PnL calculation
# mtm = 0
# pnl = 0
# print(positions)
# if (positions is not None):
#     for i in positions:
#         print(i)
#         mtm += float(i['urmtom'])
#         pnl += float(i['rpnl'])
#         day_m2m = mtm + pnl


# print(f'{day_m2m} is your Daily MTM')
