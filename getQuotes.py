import pandas as pd
import pandas_datareader.data as web
import datetime
from pathlib import Path
import os
import csv
import candleStick as cs
import analyzeCandleStick as analyze

def file_exists(fn):
    exists = os.path.isfile(fn)
    if exists:
        return 1
    else:
        return 0

def write_to_file(exists, fn, f):
    if exists:
        print("old file")
        with open(fn, 'a') as outFile:
            f.to_csv(outFile, header=False)
    else:
        print("new file")
        f.to_csv(fn)
    f.close()

def create_candlestick(f):
    h = f.iloc[1,0]
    l = f.iloc[1,1]
    o = f.iloc[1,2]
    c = f.iloc[1,3]
    candlestick = cs(o,c,h,l)
    return candlestick

def get_single_quote(ticker):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    f = web.DataReader([ticker], "yahoo", start='2019-01-11')
    return f

def get_multiple_quotes(ticker):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    f = web.DataReader([ticker], "yahoo", start='2018-12-01', end='2019-01-11')
    return f

def readCsvFile(fn):
    quotes = []
    with open(fn) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        count = 0
        cs_0 = cs.CandleStick(0,0,0,0,"")
        cs_1 = cs.CandleStick(0,0,0,0,"")
        cs_2 = cs.CandleStick(0,0,0,0,"")
        for row in csvReader:
            if count > 2:
                cs_2 = cs_1
                cs_1 = cs_0
                cs_0 = cs.CandleStick(float(row[3]),float(row[4]),float(row[1]),float(row[2]), row[0])
                a = analyze.isHammer(cs_0, cs_1)
                b = analyze.isStar(cs_0, cs_1)
                ratio = abs(cs_0.body)/cs_0.range
                print(cs_0.time, b, ", h=", cs_0.h,", body=", cs_0.body,", dir=", cs_0.direction, ", wick=", cs_0.wick, ratio)

            count += 1

def process_data():
    #symbols_list = ["FB","AAPL","NFLX","GOOG","BA","GS","BABA","TSLA"]
    symbols_list = ["AAPL", "FB"]
    for ticker in symbols_list:
        fn = "./quotes/" + ticker + "_day.csv";
        if file_exists(fn):
            f = get_single_quote(ticker)
            write_to_file(1, fn, f)
            #print(f)
        else:
            f = get_multiple_quotes(ticker)
            write_to_file(0, fn, f)
            #print(f)

def back_test():
    symbols_list = ["AAPL"]
    for ticker in symbols_list:
        fn = "./quotes/" + ticker + "_day.csv";
        quotes = readCsvFile(fn)

# process_data()
back_test()


#now = datetime.datetime.now()
#today = now.strftime("%Y-%m-%d")
# today = datetime.datetime.now().strftime("%Y-%m-%d")
# f = web.DataReader(["AAPL"], "yahoo", start=today)
# print(f)
# h = f.iloc[1,0]
# l = f.iloc[1,1]
# o = f.iloc[1,2]
# c = f.iloc[1,3]
