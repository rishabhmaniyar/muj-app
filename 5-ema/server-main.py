from collections import deque
from datetime import datetime, timedelta
import pandas_ta as ta
import pandas as pd
import queue

from boot import *

api = ShoonyaApiPy()
tick_queue = queue.Queue()


class login:
    user = "FA137726"
    pwd = "Mali@01"
    factor2 = api.generateTotp()
    # factor2 = "AGFPM9510L"
    vc = "FA137726_U"
    app_key = "632b447eada0340705dd4318db03ce5f"
    imei = "abc1234"

    ret = api.login(userid=user, password=pwd, twoFA=factor2, vendor_code=vc, api_secret=app_key, imei=imei)


# print(ret)

# class subscribeSocket:
#     def feedsSocket(self, token):
#         print("Token is ", token)


feed_opened = False
tick_queue_new = deque(maxlen=10)

def event_handler_feed_update(tick_data):
    # print(f"feed update ", tick_data)
    # print(f"Queue is ", tick_queue.get())
    # tick_queue.put((tick_data['tk'], tick_data['lp']))
    tick_queue_new.append((tick_data['tk'], tick_data['lp']))
    # get_next_tick((tick_data['tk'], tick_data['lp']))


def event_handler_order_update(tick_data):
    print(f"order update {tick_data}")


def open_callback():
    global feed_opened
    feed_opened = True


api.start_websocket(order_update_callback=event_handler_order_update,
                    subscribe_callback=event_handler_feed_update,
                    socket_open_callback=open_callback)

while feed_opened == False:
    pass

api.subscribe(["NFO|60485#NFO|60486#NFO|60479#NFO|60490#NFO|168044#NFO|60494#NFO|60481#NFO|60471#NFO|60477#NFO|60476"
               "#NFO|61539#NFO|61541#NSE|26009#"])


# api.subscribe(["NSE|Nifty Bank"])

def get_next_tick():
    # try:
        # return tick_queue.get_nowait()
    if len(tick_queue_new)>0:
        latestTick=tick_queue_new.pop()
        return latestTick
    # except queue.Empty:
    #     return None


# Get Historical Data
class search:
    def searchSymbol(self, text):
        r = api.searchscrip(exchange='NFO', searchtext=text)
        return (r)

class orders:
    # Place Order
    def placeOrder(self, tt, qty, type, price, tgPrice, tag, symbol):
        print("Placing order ------")
        order = api.place_order(buy_or_sell=tt, product_type='I',
                                exchange='NFO', tradingsymbol=symbol,
                                quantity=qty, discloseqty=0, price_type=type, price=price, trigger_price=tgPrice,
                                retention='DAY', remarks="LONG")
        return (order)

    # Modify Order

    # orderno = ret['norenordno'] #from placeorder return value
    # ret = api.modify_order(exchange='NSE', tradingsymbol='CANBK-EQ', orderno=orderno,
    #                                    newquantity=2, newprice_type='MKT', newprice=0.00)
    # ## sl modification
    # ret = api.modify_order(exchange='NSE', tradingsymbol='CANBK-EQ', orderno=orderno,
    #                                    newquantity=2, newprice_type='SL-LMT', newprice=201.00, newtrigger_price=200.00)

    # Cancel Order
    # orderno = ret['norenordno']
    # ret = api.cancel_order(orderno=23082100498139)


# Get Positions
positions = api.get_positions()


#
# # Order Book
# obk = api.get_order_book()
#
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

class quotes:
    def getQuotes(self, token):
        # Quotes
        if (token == "Nifty Bank"):
            exch = 'NSE'
        else:
            exch = 'NFO'
        # print("TOKEN is", token)
        quote = api.get_quotes(exchange=exch, token=token)
        return quote


# quotes.getQuotes("")


class historicalData:
    def fetchHistData(self, token, tf):
        lastBusDay = datetime.today() - timedelta(days=4)
        lastBusDay = lastBusDay.replace(hour=9, minute=15, second=0, microsecond=0)
        dailyPrice = api.get_time_price_series(exchange='NSE', token=token, starttime=lastBusDay.timestamp(),
                                               interval=tf)

        df = pd.DataFrame(dailyPrice)

        columns_to_convert = ["into", "inth", "intl", "intc", "intvwap"]
        for column in columns_to_convert:
            df[column] = pd.to_numeric(df[column])
        df = df.loc[::-1]
        df['5ema'] = df.ta.ema(close=df['intc'], length=5)
        df['15ema'] = df.ta.ema(close=df['intc'], length=15)
        df['15sma'] = df.ta.sma(close=df['intc'], length=15)
        df = df.dropna()
        return df
