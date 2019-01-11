import pandas as pd
import pandas_datareader.data as web
import datetime
from pathlib import Path
    
def create_quote_file(symbol, fn):
    start = datetime.datetime.strptime('9/1/2018', '%m/%d/%Y')
    #today = datetime.datetime.now()
    #today = datetime.datetime.strptime(today, '%m/%d/%Y')
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    f = web.DataReader([symbol], "yahoo", start, today)
    #fileName = symbol + "_day.csv";
    f.to_csv(fn)

def get_single_quote(symbol):
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    f = web.DataReader([symbol], "yahoo", start=today)    
    fileName = symbol + "_day.csv";
    with open(fileName, 'a') as outFile:
        f.to_csv(outFile, header=False)

def get_multiple_quotes(symbols_list):
    for ticker in symbols_list:
        #now = datetime.datetime.now()
        #today = now.strftime("%Y-%m-%d")
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        f = web.DataReader([ticker], "yahoo", start=today) 
        fileName = ticker + "_day.csv";
        if fileName.is_file():
            with open(fileName, 'a') as outFile:
                f.to_csv(outFile, header=False)
        else:
            create_quote_file(ticker, fileName)

symbols = ["FB","AAPL","NFLX","GOOG","BA","GS","BABA","TSLA"]
now = datetime.datetime.now()
today = now.strftime("%Y-%m-%d")
f = web.DataReader(["AAPL"], "yahoo", start=today)
print(f)
h = f.iloc[1,0]
l = f.iloc[1,1]
o = f.iloc[1,2]
c = f.iloc[1,3]
print(h)
print(l)
print(o)
print(c)
#get_single_quote("BA")

