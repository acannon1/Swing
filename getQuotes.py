import pandas as pd
import pandas_datareader.data as web
from pandas_datareader.data import Options
import datetime as datetime
from pathlib import Path
import os
import csv
import candleStick as cs
import analyzeChart as analyze
from collections import deque
# import nasdaqOptions as options

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
        f1 = open(fn, "r")
        last_line = f1.readlines()[-1]
        f1.close()
        last = last_line.split(",")
        date = (datetime.datetime.strptime(last[0], DATE_FORMAT)).strftime(DATE_FORMAT)
        today = datetime.datetime.now().strftime(DATE_FORMAT)
        if date != today:
            with open(fn, 'a') as outFile:
                f.tail(1).to_csv(outFile, header=False)
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

def get_daily_quote(ticker):
    today = datetime.datetime.now().strftime(DATE_FORMAT)
    f = web.DataReader([ticker], "yahoo", start=today)
    return f

def get_history_quotes(ticker):
    today = datetime.now().strftime(DATE_FORMAT)
    f = web.DataReader([ticker], "yahoo", start='2018-08-01', end=today)
    return f

def get_options(ticker):
    tmp_df = Options(ticker, 'yahoo').get_all_data()
    print(tmp_df)

def make_decision(value, time):
    if value:
        print ("OPEN TRADE")
        verbage = ''
        if value & 0x1:
            print("HAMMER")
            verbage += "HAMMER "
        if value & 0x2:
            print("STAR")
            verbage += "STAR "
        if value & 0x4:
            print("MAJOR MOVE")
            verbage += "MAJOR MOVE "
        if value & 0x8:
            print("GAP UP")
            verbage += "GAP UP "
        if value & 0x10:
            print("GAP DOWN")
            verbage += "GAP DOWN "
        if value & 0x20:
            print("BEARISH ENGULFING")
            verbage += "BEARISH ENGULFING "
        if value & 0x40:
            print("BULLISH ENGULFING")
            verbage += "BULLISH ENGULFING "
        if value & 0x80:
            print("PIERCING LINE")
            verbage += "PIERCING LINE "
        if value & 0x100:
            print("BLACK MARUBOZU")
            verbage += "BLACK MARUBOZU "
        if value & 0x200:
            print("WHITE MARUBOZU")
            verbage += "WHITE MARUBOZU "
        if value & 0x400:
            print("BEARISH DOJI")
            verbage += "BEARISH DOJI "
        if value & 0x800:
            print("BULLISH DOJI")
            verbage += "BULLISH DOJI "

        with open('./quotes/results.txt', 'a') as results:
            results.write('%r OPEN TRADE %s %r\n' %(time, value, verbage))

def analyze_data(cs_0, cs_1, cs_2, atr):
    a, av = analyze.hammer(cs_0, cs_1)
    b, bv = analyze.star(cs_0, cs_1)
    c, cv = analyze.major_move(cs_0, atr)
    d, dv = analyze.gap_up(cs_0, cs_1)
    e, ev = analyze.gap_down(cs_0, cs_1)
    f, fv = analyze.bearish_engulfing(cs_0, cs_1)
    g, gv = analyze.bullish_engulfing(cs_0, cs_1)
    h, hv = analyze.piercing_line(cs_0, cs_1)
    i, iv = analyze.black_marubozu(cs_0, atr)
    j, jv = analyze.white_marubozu(cs_0, atr)
    k, kv = analyze.bearish_doji(cs_0, cs_1)
    l, lv = analyze.bullish_doji(cs_0, cs_1)
    # print(cs_0.time, "\t", a, "\t", b, "\t", c, "\t", d, "\t", e, "\t", f, "\t", g, "\t", h, "\t", i, "\t", j, "\t", k, "\t", l)
    value = av | bv | cv | dv | ev | fv | gv | hv | iv | jv | kv | lv
    make_decision(value, cs_0.time)

def get_last_three(fn):
    with open(fn) as csvDataFile:
        allData = csv.reader(csvDataFile)
        atr = analyze.get_avg_range(allData)

    with open(fn, 'r') as f:
        lines = f.readlines()
        row0 = lines[-1]
        row1 = lines[-2]
        row2 = lines[-3]

    return atr, row0, row1, row2

def daily():
    for ticker in symbols_list:
        fn = "./quotes/" + ticker + "_day.csv";
        if file_exists(fn):
            f = get_daily_quote(ticker)
            write_to_file(OLD, fn, f)
        else:
            f = get_history_quotes(ticker)
            write_to_file(NEW, fn, f)

        atr, row0, row1, row2 = get_last_three(fn)

        line = row0.split(",")
        a = float(line[3])
        b = float(line[4])
        c = float(line[1])
        d = float(line[2])
        e = line[0]
        cs_0 = cs.CandleStick(a,b,c,d,e)

        line = row1.split(",")
        a = float(line[3])
        b = float(line[4])
        c = float(line[1])
        d = float(line[2])
        e = line[0]
        cs_1 = cs.CandleStick(a,b,c,d,e)

        line = row2.split(",")
        a = float(line[3])
        b = float(line[4])
        c = float(line[1])
        d = float(line[2])
        e = line[0]
        cs_2 = cs.CandleStick(a,b,c,d,e)

        analyze_data(cs_0, cs_1, cs_2, atr)


def back_test():
    for ticker in symbols_list:
        fn = "./quotes/" + ticker + "_day.csv";
        with open(fn) as csvDataFile:
            allData = csv.reader(csvDataFile)
            atr = analyze.get_avg_range(allData)

        with open(fn) as csvDataFile:
            allData = csv.reader(csvDataFile)
            cs_0 = cs.CandleStick(0,0,0,0,"")
            cs_1 = cs.CandleStick(0,0,0,0,"")
            cs_2 = cs.CandleStick(0,0,0,0,"")
            count = 0
            for row in allData:
                if count > 2:
                    cs_2 = cs_1
                    cs_1 = cs_0
                    cs_0 = cs.CandleStick(float(row[3]),float(row[4]),float(row[1]),float(row[2]), row[0])
                    quotes = analyze_data(cs_0, cs_1, cs_2, atr)
                count += 1

daily()
back_test()
# options1 = options.NasdaqOptions('AAPL',2)
# calls, puts = options1.get_options_table()
# print(calls)
 # print('\n######\nCalls:\n######\n', calls,\
 #        '\n\n######\nPuts:\n######\n', puts)
