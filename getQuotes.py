import pandas as pd
import pandas_datareader.data as web
import datetime
from pathlib import Path
import os

#import CandleStick as cs
#import analyzeCandleStick as analyze

def file_exists(fn):
    exists = os.path.isfile(fn)
    if exists:
        return 1
    else:
        return 0

def write_to_file(ticker, f):
    fn = "./quotes/" + ticker + "_day.csv";
    exists = os.path.isfile(fn)
    if exists:
        print("old file")
        with open(fn, 'a') as outFile:
            f.to_csv(outFile, header=False)
    else:
        print("new file")
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

#symbols_list = ["FB","AAPL","NFLX","GOOG","BA","GS","BABA","TSLA"]
symbols_list = ["FB", "AAPL"]
for ticker in symbols_list:
    fn = "./quotes/" + ticker + "_day.csv";
    f = get_single_quote(ticker)
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
