#每日一进二
import akshare as ak
import datetime
import json

def stock_zt_pool_previous(date:datetime.date):
    stocks = ak.stock_zt_pool_em(date.strftime("%Y%m%d"))
    print(stocks)
    codes = []
    for item in stocks.itertuples():
        if item[-2] != 1 :
            continue
        if "st" in item[3] or "ST" in item[3]:
            continue
        print(item[2])
        codes.append(item[2])
    print(codes, len(codes))
    # 获取今天首板和最大成交量
    stockDict = {}
    for code in codes:
        # 获取涨停那天的全天追高的分时成交量
        startTime = date.strftime("%Y-%m-%d 09:30:00")
        endTime = date.strftime("%Y-%m-%d 15:00:00")
        stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(symbol=code, start_date=startTime, end_date=endTime, period="1", adjust="")
        print(stock_zh_a_hist_min_em_df)
        maxAmt = stock_zh_a_hist_min_em_df['成交量'].max()
        print(maxAmt)
        print(stock_zh_a_hist_min_em_df.iloc[-1]['收盘'])
        stockDict[code] = {
            "maxMtAmt": int(maxAmt),
            "close": round(stock_zh_a_hist_min_em_df.iloc[-1]['收盘'], 2)
        }
    with open("zt_pool_previous.json", "w") as f:
        json.dump(stockDict, f)

def check_today_1_to_2():
    date = datetime.date.today()
    startTime = date.strftime("%Y-%m-%d 09:15:00")
    endTime = date.strftime("%Y-%m-%d 09:30:00")
    stockDict = {}
    with open("zt_pool_previous.json", "r") as f:
        stockDict = json.load(f)
    print(stockDict)
    # 获取今天竞价结果
    hasPrice = []
    highPrice = []
    superPrice = []
    easy_2ban = []
    for code, info in stockDict.items():
        preClose = info.get("close") or 0
        if not preClose:
            continue
        maxMtAmt = info.get("maxMtAmt") or 0
        if not maxMtAmt:
            continue
        print(code, "close:", preClose, " maxMtAmt:", maxMtAmt)
        stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(symbol=code, start_date=startTime, end_date=endTime, period="1", adjust="")
        price = stock_zh_a_hist_min_em_df.loc[0]["开盘"]
        amt = stock_zh_a_hist_min_em_df.loc[0]["成交额"]
        print("开盘:", price)
        print("成交额:", amt)
        jjb = amt / maxMtAmt
        if jjb > 1.2:
            superPrice.append(code)
        elif jjb > 1:
            highPrice.append(code)
        elif jjb > 0.5:
            hasPrice.append(code)
        chg = (price - preClose) / preClose
        if chg < 0.5:
            if jjb > 0.4:
                easy_2ban.append(code)
        else:  
             if jjb > 1:
                easy_2ban.append(code)
    print("容易晋级:", ",".join(easy_2ban))
    print("超高价值:", ",".join(superPrice))
    print("高价值:", highPrice)
    print("有价值:", hasPrice)
    with open("容易晋级1进2.txt", "w") as f:
        f.writelines(",".join(easy_2ban))

if __name__ == '__main__':
    current_time = datetime.datetime.now()
    if current_time.hour > 16 :
        print("当前时间已经超过中午12点")
        date = datetime.date.today()
        stock_zt_pool_previous(date)
    else:
        check_today_1_to_2()
