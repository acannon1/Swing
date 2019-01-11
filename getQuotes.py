import pandas as pd
import pandas_datareader.data as web
import datetime
from pathlib import Path
import CandleStick as cs
import analyzeCandleStick as analyze

def write_to_file(ticker, f):
    fn = ticker + "_day.csv";
    if fn.is_file():
        with open(fn, 'a') as outFile:
            f.to_csv(outFile, header=False)
    else:
        f.to_csv(fn)

def create_candlestick(f):
    h = f.iloc[1,0]
    l = f.iloc[1,1]
    o = f.iloc[1,2]
    c = f.iloc[1,3]
    candlestick = cs(o,c,h,l)
    return candlestick

def get_single_quote(ticker):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    f = web.DataReader([ticker], "yahoo", start=today)
    return f

#symbols = ["FB","AAPL","NFLX","GOOG","BA","GS","BABA","TSLA"]
symbols = ["FB"]
for ticker in symbols_list:
    f =get_single_quote(ticker)
    write_to_file(ticker, f)
    #cs = create_candlestick(f)
    #a = analyze.isHammer(cs)
    #b = analyze.isStar(cs)
    #print(a)
    #print(b)

#now = datetime.datetime.now()
#today = now.strftime("%Y-%m-%d")
# today = datetime.datetime.now().strftime("%Y-%m-%d")
# f = web.DataReader(["AAPL"], "yahoo", start=today)
# print(f)
# h = f.iloc[1,0]
# l = f.iloc[1,1]
# o = f.iloc[1,2]
# c = f.iloc[1,3]
# print(h)
# print(l)
# print(o)
# print(c)
#get_single_quote("BA")
