import pandas as pd
import pandas_datareader.data as web
import datetime
from pathlib import Path
import os
import csv
import candleStick as cs
import analyzeCandleStick as analyze

NEW = 0
OLD = 1
DATE_FORMAT = "%Y-%m-%d"

#symbols_list = ["FB","AAPL","NFLX","GOOG","BA","GS","BABA","TSLA"]
symbols_list = ["AAPL"]

def file_exists(fn):
    exists = os.path.isfile(fn)
    if exists:
        return 1
    else:
        return 0

def write_to_file(exists, fn, f):
    if exists:
        print("old file")
        f1 = open(fn, "r")
        last_line = f1.readlines()[-1]
        f1.close()
        last = last_line.split(",")
        date = (datetime.datetime.strptime(last[0], DATE_FORMAT)).strftime(DATE_FORMAT)
        today = datetime.datetime.now().strftime(DATE_FORMAT)
        if date != today:
            print("date not found")
            with open(fn, 'a') as outFile:
                f.to_csv(outFile, header=False)
            # f2 = open(fn, "r")
            # last_line_1 = f1.readlines()[-1]
            # last_line_2 = f1.readlines()[-2]
            # f2.close()
            # if last_line_1 == last_line_2:

        # with open(fn) as csvDataFile:
        #
        #     row_count = sum(1 for line in csvDataFile)
        #     print(csvDataFile[row_count])
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
    today = datetime.datetime.now().strftime(DATE_FORMAT)
    f = web.DataReader([ticker], "yahoo", start=today)
    return f

def get_multiple_quotes(ticker):
    today = datetime.datetime.now().strftime(DATE_FORMAT)
    f = web.DataReader([ticker], "yahoo", start='2018-08-01', end=today)
    return f

def readCsvFile(fn):
    quotes = []
    with open(fn) as csvDataFile:
        allData = csv.reader(csvDataFile)
        # atr = analyze.getAvgRange(allData)
        # print(atr)

        cs_0 = cs.CandleStick(0,0,0,0,"")
        cs_1 = cs.CandleStick(0,0,0,0,"")
        cs_2 = cs.CandleStick(0,0,0,0,"")
        count = 0
        for row in allData:
            if count > 2:
                cs_2 = cs_1
                cs_1 = cs_0
                cs_0 = cs.CandleStick(float(row[3]),float(row[4]),float(row[1]),float(row[2]), row[0])
                a = analyze.hammer(cs_0, cs_1)
                b = analyze.star(cs_0, cs_1)
                c = analyze.majorMove(cs_0)
                d = analyze.gapUp(cs_0, cs_1)
                e = analyze.gapDown(cs_0, cs_1)
                ratio = abs(cs_0.body)/cs_0.range
                wr = cs_0.wick/abs(cs_0.body)
                tr = cs_0.tail/abs(cs_0.body)
                # print(cs_0.time, "\t%.2f" % cs_0.body, "\t%.2f" % cs_0.wick, "\t%.2f" % cs_0.tail, "\t%.2f" % wr, "\t%.2f" % tr)
                print(cs_0.time, "\t", a, "\t", b, "\t", c, "\t", d, "\t", e)

            count += 1

def daily():
    for ticker in symbols_list:
        fn = "./quotes/" + ticker + "_day.csv";
        if file_exists(fn):
            f = get_single_quote(ticker)
            write_to_file(OLD, fn, f)
        else:
            f = get_multiple_quotes(ticker)
            write_to_file(NEW, fn, f)

def back_test():
    for ticker in symbols_list:
        fn = "./quotes/" + ticker + "_day.csv";
        quotes = readCsvFile(fn)

daily()
# back_test()


#now = datetime.datetime.now()
#today = now.strftime("%Y-%m-%d")
# today = datetime.datetime.now().strftime("%Y-%m-%d")
# f = web.DataReader(["AAPL"], "yahoo", start=today)
# print(f)
# h = f.iloc[1,0]
# l = f.iloc[1,1]
# o = f.iloc[1,2]
# c = f.iloc[1,3]
