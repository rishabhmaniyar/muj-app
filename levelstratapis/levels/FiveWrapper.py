from py5paisa import FivePaisaClient
import pyotp
from py5paisa.order import Order, OrderType, Exchange

class loginUser():

    def login_token(self):
        cred = {
            "APP_NAME": "5P52270380",
            "APP_SOURCE": "20605",
            "USER_ID": "ji0sy0DwLC1",
            "PASSWORD": "5wUqySk6qRX",
            "USER_KEY": "Cn5p1aBA7YllUrNuHiRTy1igrxOt0cWx",
            "ENCRYPTION_KEY": "wK11ACPrUEU2DlX03Wk7zFmzlVgpC7Dc"
        }

        client = FivePaisaClient(cred=cred)
        totp = pyotp.TOTP("GUZDENZQGM4DAXZVKBDUWRKZ").now()

        print("TOTP -> ", totp)
        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjUyMjcwMzgwIiwicm9sZSI6IkNuNXAxYUJBN1lsbFVyTnVIaVJUeTFpZ3J4T3QwY1d4IiwibmJmIjoxNzA1MzAzMTI0LCJleHAiOjE3MDUzMDMxNTQsImlhdCI6MTcwNTMwMzEyNH0.pbVvtrRuJttfwTDVDT57tbHeAjIO9sqA5MKkYn8efk0'
        # client.get_oauth_session(token)
        client.get_totp_session('52270380', totp, '747474')
        return client


class positions():

    def fetch_positions(self, client):
        print("Fetching positions")
        positions = (client.positions())
        return positions

class ltp():

    def fetch_underlying_ltp(self,client,underlyingName,optionName):
        print("Fetching LTP")
        requestForUnderlying = [
                  {"Exchange": "N", "ExchangeType": "C", "Symbol": underlyingName},
                  {"Exchange": "N", "ExchangeType": "D", "Symbol": optionName},
                  ]
        print("Request is ",requestForUnderlying)
        return client.fetch_market_depth_by_symbol(requestForUnderlying)
# print(client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, Price=260))

#
# req_list = [
#     {"Exch": "M", "ExchType": "D", "ScripCode": "256949"},
#     {"Exch": "N", "ExchType": "C", "ScripCode": "1660"},
# ]
#

#
# # req_list_ = [{"Exch": "N", "ExchType": "C", "ScripData": "ITC_EQ"}]
# #               {"Exch": "N", "ExchType": "C", "ScripCode": "2885"}]
#
# print(client.fetch_market_feed_scrip(req_list))
#
# print(client.fetch_market_depth(req_list_depth))
#
# req_data = client.Request_Feed('mf', 's', req_list)
#
# print("REQ DATA", req_data)
#
#
# def on_message(message):
#     print(message)
#
#
# client.connect(req_data)
#
# client.receive_data(on_message)


# print(client.get_expiry("N","NIFTY"))
