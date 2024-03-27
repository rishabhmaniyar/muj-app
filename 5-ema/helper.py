import math


class helper:
    def checkNextCandle(self, t1_low, t_low):
        if (t1_low > t_low):
            return True
        else:
            return False

    def stopLossHit(self, t1_high, sl):
        if (t1_high >= sl):
            return True
        else:
            return False

    def targetHit(self, p, targetList, type):
        tp = targetList[0]
        if (type == "S"):
            if (len(targetList) != 0):
                if (p <= tp):
                    print("Target List is ", targetList, "Price ->>> ", p)
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
        # return targetList

    def targetHitSingle(self, t_low, t):
        if (t_low <= t):
            return True
        else:
            return False

    def getPartialQty(self, s, qty):
        match (s):
            case 0:
                return math.floor(qty * 0.15)
            case 1:
                return math.floor(qty * 0.15)
            case 2:
                return math.floor(qty * 0.4)
            case 3:
                return math.floor(qty * 0.3)
        return s

    def getSettlementTradesForOrder(self, orderId, df):
        trades = df.loc[df['Order_Id'] == orderId]
        trades['Value'] = trades["Price"] * trades["Qty"]
        return (trades)
