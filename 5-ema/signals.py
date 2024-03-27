import json
import math
import threading
import time
import requests

import redis
from datetime import date
from WebSocketHandler import WebSocketHandler

from main import *

# from loguru._logger import start_time

# from helper import *

historicalData = historicalData()
quote = quotes()
search = search()
# feeds=subscribeSocket()
url = "https://hooks.slack.com/services/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"

headers = {
  'Content-type': 'application/json'
}

size = 2

# orderMap={'BANKNIFTY31AUG23C44300': ('B', [44466.65000000001, 44436.000000000015, 44405.35000000002, 44374.700000000026], 44527.95,"Settlement Status")}
# orderMap = {'BANKNIFTY13SEP23P45800': ('S', [45627.9, 45579.15, 45530.4, 45481.65], 45725.4, 'NA')}

# orderMap = {'BANKNIFTY13SEP23P45700': ('S', [45530.5, 45487.65, 45444.8, 45401.950000000004], 45616.2, 'NA'),
#             'BANKNIFTY13SEP23C45200': (
#                 'B', [45495, 45502.00000000001, 45716.80000000001, 45811.60000000001], 45449.6, 'NA'),
#             'BANKNIFTY13SEP23P45600': (
#                 'S', [45401.65000000001, 45335.500000000015, 45269.35000000002, 45203.200000000026], 45533.95, 'NA')}

# sub="26009#|"
sub = "NFO|60485#NFO|60486#NFO|60479#NFO|60490#NFO|168044#NFO|60494#NFO|60481#NFO|60471#NFO|60477#NFO|60476#NFO|61539#NFO|61541#NSE|26009#"


# OMP is  {'BANKNIFTY13SEP23P45700': ('S', [45505.299999999996, 45473.899999999994, 45442.49999999999, 45411.09999999999], 45568.1, 'NA')}


# helper = helper()

# Keep Polling Historical Data for 15mins Data for Buying Signals & 5mins for Selling Signals

def sendNotification(data):
    payload = json.dumps({ "text": data})
    response = requests.request("POST", url, headers=headers, data=payload)

def fetchLatestData(token):
    # df5 = historicalData.fetchHistData(token, 5)
    df15 = historicalData.fetchHistData(token, 15)
    # print(df15)
    # EMA calculation
    # df15['ema'] = df15.ta.ema(5)
    # df5['ema'] = df5.ta.ema(5)
    # df15.dropna(inplace=True)
    # df5.dropna(inplace=True)
    return df15
    # return df5, df15


def getAtm(ltp):
    sp = math.fmod(ltp, 100)
    ce = ltp - sp - 100
    pe = ltp + (100 - sp) + 100
    # print('ITM', ltp-sp)
    # print('OTM', ltp+(100-sp))
    return (ce, pe, ltp)


def getTradeSymbol(underlying, strike, option):
    text = underlying + " " + str(strike) + " " + option
    results = search.searchSymbol(text)
    return results['values'][0]['tsym']


def clearExistingPositions():
    print("Forced EXIT hit")
    positions = api.get_positions()
    # r.set('POSTIONS', str(positions))
    sendNotification("Forced EXIT hit")
    if positions is not None:
        sendNotification("Position is not none")
        for p in positions:
            ts = p['tsym']
            order = orders()
            if ts in orderMap.keys():
                sendNotification("Trading Symbol In Orders Map")
                print("Placing square Off orders -> ")
                order = order.placeOrder(
                    tt='S',
                    qty=getRemainingQty(ts),
                    type='MKT',
                    price=0,
                    tgPrice=None,
                    tag="FORCED-EXIT",
                    symbol=ts
                )
                omp = orderMap[ts]
                ntp = omp[:-1] + ("EXIT",)
                orderMap[ts] = ntp
    return True


def checkForValue(highBuy, lowBuy, emaBuy15, smaBuy15):
    print("Checking for value : ", highBuy, lowBuy, emaBuy15, smaBuy15)
    totalQty = size * 15
    smaDistance = abs(lowBuy - smaBuy15)
    emaDistance = abs(lowBuy - emaBuy15)
    minDistance = min(emaDistance, smaDistance)
    diff = abs(highBuy - lowBuy)
    if minDistance < 45:
        return 0
    else:
        if diff <= 110:
            return totalQty
        elif 110 < diff < 150:
            return totalQty / 2
        # elif 150 < diff < 190:
        #     return totalQty / 3
        else:
            return 0


def getAlertCandle(df15):
    # Sell
    # prevSell = df5.iloc[-2]
    # Buy
    try:
        prevBuy = df15.iloc[-2]
    except:
        payload = json.dumps({ "text": "Error in fetching Alert Candle -2 Data"})
        response = requests.request("POST", url, headers=headers, data=payload)
    # highSell = prevSell['inth']
    # lowSell = prevSell['intl']
    # closeSell = prevSell['intc']
    # emaSell = prevSell['ema']

    highBuy = prevBuy['inth']
    lowBuy = prevBuy['intl']
    closeBuy = prevBuy['intc']
    emaBuy5 = prevBuy['5ema']
    emaBuy15 = prevBuy['15ema']
    smaBuy15 = prevBuy['15sma']

    # alert(True,"B",high,low)
    # Buy Alert
    try:
        if (highBuy < emaBuy15) & (closeBuy < emaBuy15):
            print("Buy Side ALert ")
            diff = abs(highBuy - lowBuy)
            if diff < 120:
                return (True, "B", highBuy, lowBuy)
            else:
                return False, None, None, None
        # Sell Alert
        # elif (lowSell > emaBuy15) & (closeSell > emaSell):
        elif (lowBuy > emaBuy15) & (lowBuy > smaBuy15) & (closeBuy > emaBuy15) & (closeBuy > smaBuy15):
            overRideQty = checkForValue(highBuy, lowBuy, emaBuy15, smaBuy15)
            if overRideQty > 0:
                return True, "S", highBuy, lowBuy
            else:
                return False, None, None, None
        else:
            return False, None, None, None
    except:
        payload = json.dumps({ "text": "Error in fetching Alert Candle comparison"})
        response = requests.request("POST", url, headers=headers, data=payload)


def checkEntryCondition(f1, side, token):
    quotes()
    ltp = None
    if side == "B":
        print("checkEntryCondition now in ", side)
        startTime = time.time()
        while time.time() - startTime < 900:
            # q = quote.getQuotes(token)
            td = get_next_tick()
            print("Tick data is ", td)
            if td is not None:
                ltp = float(td[1])
            # ltp = float(q['lp'])
            if ltp is not None:
                print("B ---- LTP is -> ", ltp, "Price -> ", f1, "Time Elapsed -> ", time.time() - startTime)
                if ltp > f1:
                    return "BUY"
        return "DONE"
    if side == "S":
        print("checkEntryCondition now in ", side)
        startTime = time.time()
        while time.time() - startTime < 900:
            # q = quote.getQuotes(token)
            td = get_next_tick()
            print("Tick data is ", td)
            if td is not None:
                ltp = float(td[1])
            # ltp = float(q['lp'])
            if ltp is not None:
                print("S ----  LTP is -> ", ltp, "Price -> ", f1, "Time Elapsed -> ", time.time() - startTime)
                if (ltp < f1):
                    return "SELL"
        return "DONE"


def checkIfExistingPosition(symbol):
    positions = api.get_positions()
    # r.set('POSTIONS', str(positions))
    # print(positions)
    for p in positions:
        if p['tsym'] == symbol:
            print("Active Position Found ", p['tsym'])
            return True
        else:
            continue

    print("No Active Position Found ", p['tsym'])
    return False


def getRemainingQty(ts):
    positions = api.get_positions()
    # r.set('POSTIONS', str(positions))
    # print(positions)
    for p in positions:
        if p['tsym'] == ts and p['prd'] == "I":
            print("Day Buy Qty ", int(p['daybuyqty']), "Day Sell Qty ", int(p['daysellqty']))
            remQty = int(p['daybuyqty']) - int(p['daysellqty'])
            if remQty > 0:
                return remQty
    else:
        return None


def getTuneTime(current_time):
    seconds_elapsed = current_time.second + 60 * current_time.minute
    seconds_remaining = 900 - (seconds_elapsed % 900)
    return seconds_remaining


def getCurrentMaPrice():
    maxMa = 0
    df = None
    try:
        df = fetchLatestData("Nifty Bank")
        maxMa = max(df.iloc[-2]['15ema'], df.iloc[-2]['15sma'])
    except:
        print("Exception occured in getCurrentMaPrice -- ", df)
    return maxMa


class Core():
    pos = "NA"

    def getOrderMap(self):
        return orderMap

    def checkForSlTp(self):
        while not stop_event.is_set():
            # r.set('OMP', str(orderMap))
            while True:
                res = get_next_tick()
                if res is not None:
                    print("Current value in queue ", res)
                    ltp = float(res[1])
                    for ts in orderMap.keys():
                        omp = orderMap[ts]
                        if (omp[3] != "SL" or omp[3] != "T"):  # can evaluate =="NA" condition
                            omp = orderMap[ts]
                            tList = omp[1]
                            remQty = getRemainingQty(ts)
                            if remQty is None:
                                remQty = 0
                            print("Rem Qty", remQty, "Length ", len(tList))
                            if checkIfExistingPosition(ts) and remQty > 0 and len(tList) != 0:
                                tResponse = self.singleTargetHit(ltp, tList[0], omp[0])
                                # tResponse = self.targetHit(ltp, tList, omp[0])
                                slResponse = self.stopLossHit(ltp, omp[2], omp[0])
                                print("Target Response ", tResponse)
                                print("SL Response ", slResponse)
                                order = orders()
                                if tResponse is not None:
                                    # if len(tResponse) != 0:
                                    if tResponse:
                                        print("Target hit")
                                        payload = json.dumps({ "text": "Target hit"})
                                        response = requests.request("POST", url, headers=headers, data=payload)
                                        # l = len(tResponse)
                                        # print("Length ", l, "Target changed")
                                        # pQty = self.getPartialQty(l, 15 * size)
                                        # pQty = self.getPartialQty(0, 15 * size)
                                        # tpQty = pQty - (pQty % 15)
                                        ntp = omp[:-1] + ("T",)
                                        # if l == 0:
                                        #     ntp = omp[:-1] + ("T",)
                                        # else:
                                        #     ntp = omp[:-1] + ("PT",)
                                        order = order.placeOrder(
                                            tt='S',
                                            qty=15 * size,
                                            type='MKT',
                                            price=0,
                                            tgPrice=None,
                                            tag="T",
                                            symbol=ts
                                        )
                                        self.pos = "NA"
                                        print(order)
                                        print("New tuple is ", ntp)
                                        orderMap[ts] = ntp
                                order = orders()
                                if slResponse:
                                    print("SL hit")
                                    payload = json.dumps({ "text": "SL hit"})
                                    response = requests.request("POST", url, headers=headers, data=payload)
                                    ntp = omp[:-1] + ("SL",)
                                    orderMap[ts] = ntp
                                    order = order.placeOrder(
                                        tt='S',
                                        qty=getRemainingQty(ts),
                                        type='MKT',
                                        price=0,
                                        tgPrice=None,
                                        tag="SL",
                                        symbol=ts
                                    )
                                    self.pos = "NA"
                                    print(order)

    def targetHit(self, p, targetList, type):
        tp = targetList[0]
        if (type == "S"):
            if (len(targetList) != 0):
                if (p <= tp):
                    print("Target List is ", targetList, "Price ->>> ", p)
                    targetList.pop(0)
                    if len(targetList) > 0:
                        self.targetHit(p, targetList, type)
                        return targetList
                    elif len(targetList) == 0:
                        return None
                    else:
                        return []
                else:
                    return []

        elif (type == "B"):
            if (len(targetList) != 0):
                if (p >= tp):
                    print("Target List is ", targetList, "Price ->>> ", p, "Target is ->>", tp)
                    targetList.pop(0)
                    if (len(targetList) > 0):
                        self.targetHit(p, targetList, type)
                        return targetList
                    elif (len(targetList) == 0):
                        return None
                    else:
                        return []
                else:
                    return []


    def singleTargetHit(self, p, tg, type):
        if type == "S":
            if (p <= tg):
                return True
            else:
                return False
        elif type == "B":
            if (p >= tg):
                return True
            else:
                return False

    def stopLossHit(self, p, sl, type):
        if type == "S":
            if (p >= sl):
                return True
            else:
                return False
        elif type == "B":
            if (p <= sl):
                return True
            else:
                return False

    def getPartialQty(self, s, qty):
        # match s:
        #     # case 0:
        #     #     return math.floor(qty * 0.15)
        #     # case 1:
        #     #     return math.floor(qty * 0.15)
        #     # case 2:
        #     #     return math.floor(qty * 0.4)
        #     # case 3:
        #     #     return math.floor(qty * 0.3)
        #     case 0:
        #         return 15
        #     case 1:
        #         return 15
        #     case 2:
        #         return 30
        #     case 3:
        #         return 30
        return size * 15
        # positions = api.get_positions()
        # print("Positions is --->>> ", positions)
        # if positions is not None:
        #     for p in positions:
        #         sym = p['tsym']
        #         if (sym in orderMap.keys()):
        #             print("Symbol in Map ", sym)
        #             print("Track values in Map ", orderMap[sym])
        #             # checkForSl(orderMap[sym][2])
        #             # checkForTarget(orderMap[sym][1])
        return True

    def process(self):
        print("SE", stop_event)
        while not stop_event.is_set():
            print("Event tabs -----")
            current_time = datetime.now()
            if current_time.minute != 0 and current_time.second != 0:
                #tuneTime = getTuneTime(current_time)
                tuneTime = 3
                print("Time to wait", tuneTime)
                time.sleep(tuneTime)
            payload = json.dumps({ "text": "Starttttt"})
            response = requests.request("POST", url, headers=headers, data=payload)
            while True:
                # feeds.feedsSocket(sub)
                time.sleep(10)
                # OMP is  {'BANKNIFTY31AUG23C44300': ('B', [44466.65000000001, 44436.000000000015, 44405.35000000002, 44374.700000000026], 44527.95)}
                # orderMap={'BANKNIFTY07FEB24C45600': ('B', [45957.09999999999], 45740.3, 'NA')}
                print("OMP is ", orderMap)
                token = "Nifty Bank"
                underlying = "BANKNIFTY"
                # self.checkForSlTp()
                df15 = fetchLatestData(token)
                # df5 = resp[0]
                # df15 = resp[1]
                q = quote.getQuotes(token)
                q = json.dumps(q)
                q = json.loads(q)
                ltp = q['lp']
                # alert(True,"B",high,low)
                strikes = getAtm(float(ltp))
                # tradeSymbol = getTradeSymbol(underlying=underlying, strike=strikes[0], option="CE")
                symbolCe = getTradeSymbol(underlying=underlying, strike=strikes[0], option="CE")
                symbolPe = getTradeSymbol(underlying=underlying, strike=strikes[1], option="PE")

                alert = getAlertCandle(df15)
                # alert = getAlertCandle(df5, df15)
                # alert=(True,"B",45441,45383.75)
                # alert=(True,"B",High,Low)
                print("ALERT is ", alert, "@", time.time())
                print("POS is -- --  ",self.pos)
                if alert[0]:
                    if alert[1] == "B" and (self.pos == "NA" or self.pos == "SHORT"):
                        print("checkEntryCondition now for BUY", alert)
                        # signal=(BUY,SL,Entry)
                        payload = json.dumps({ "text": "Buy Signal"})
                        response = requests.request("POST", url, headers=headers, data=payload)
                        signal = (checkEntryCondition(alert[2], "B", "Nifty Bank"), alert[3], alert[2])
                    if alert[1] == "S" and (self.pos == "NA" or self.pos == "LONG"):
                        payload = json.dumps({ "text": "Sell Signal"})
                        response = requests.request("POST", url, headers=headers, data=payload)
                        print("checkEntryCondition now for SELL", alert)
                        signal = (checkEntryCondition(alert[3], "S", "Nifty Bank"), alert[2], alert[3])
                else:
                    continue
                # signal = "BUY"
                # Buy Signal
                order = orders()
                if signal[0] == "BUY":
                    if self.pos == "NA" or self.pos == "SHORT":
                        print("Strikes Are -> ", strikes)
                        print("Positions flag -> ",self.pos)
                        # Buy Call Option
                        if clearExistingPositions():
                            tag = "LONG"
                            print("Tag -> ", tag)
                            order = order.placeOrder(
                                tt='B',
                                qty=15 * size,
                                type='MKT',
                                price=0,
                                tgPrice=None,
                                tag=str(tag),
                                symbol=symbolCe
                            )
                            self. pos = "LONG"
                            print(order)
                            sl = signal[1]
                            entry = signal[2]
                            diff = abs(entry - sl)
                            # target = [entry + diff, entry + diff * 2, entry + diff * 3, entry + diff * 4]
                            target = [entry + diff]
                            orderMap[symbolCe] = ("B", target, sl, "NA")
                    # Short setup
                    # Buy Put Option
                if signal[0] == "SELL":
                    order = orders()
                    if self.pos == "NA" or self.pos == "LONG":
                        if clearExistingPositions():
                            # tag = "Enter Put Buy @ " + str(date.today())
                            tag = "SHORT"
                            print("Tag -> ", tag)
                            print("Positions flag -> ", self.pos)
                            order = order.placeOrder(
                                tt='B',
                                qty=15 * size,
                                type='MKT',
                                price=0,
                                tgPrice=None,
                               tag=str(tag),
                                symbol=symbolPe
                            )
                            self. pos = "SHORT"
                            print("Order status ---- > ", order)
                            sl = signal[1]
                            entry = signal[2]
                            # diff = abs(entry - sl)
                            maPrice = getCurrentMaPrice()
                            diff = abs(maPrice-entry)
                            print("Current MA price ", diff)
                            # target = [entry - diff, entry - diff * 2, entry - diff * 3, entry - diff * 4]
                            target = [entry - diff]
                            print("Revised target ", target)
                            orderMap[symbolPe] = ("S", target, sl, "NA")

                alert = (False, None, None, None)
                if signal[0] == "DONE":
                    continue

    def killSwitch(self):
        self.stop_event.set()
        clearExistingPositions()

    def restartThreads(self):
        self.stop_event.clear()


if __name__ == "__main__":
    # r = redis.Redis(host='redis-17728.c309.us-east-2-1.ec2.cloud.redislabs.com', port=17728, db=0, username="default",
    #                 password="BwHDPU5abipLL8rvsRY8uFXaZmrlT4ji")
    print("Init ")
    orderMap = {}
    stop_event = threading.Event()
    print("INvoking threads")
    stop_event.clear()

    # Start the WebSocket handler in parallel
    # ws_handler = WebSocketHandler()
    # ws_handler.run()
    # When you want to subscribe to feeds, call the subscribe method
    # instruments_to_subscribe = ["NSE|Nifty Bank"]
    # ws_handler.subscribe(instruments_to_subscribe)

    # Perform other tasks while WebSocket handler runs
    other_task = Core()
    payload = json.dumps({ "text": "Algo runnning"})
    response = requests.request("POST", url, headers=headers, data=payload)
    # Create threads for the two functions
    print(other_task.pos)
    thread1 = threading.Thread(target=other_task.process)
    thread2 = threading.Thread(target=other_task.checkForSlTp)

    # Start the threads
    thread1.start()
    thread2.start()

    # thread1.join()
    # thread2.join()
    #
    # print("Both threads have finished.")
