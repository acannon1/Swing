import datetime as datetime
import candleStick as cs
import analyzeChart as analyze
import tdAmeritradeApi as td

# symbols_list = ["FB","AAPL","NFLX","GOOG","BA","GS","BABA","TSLA"]
symbols_list = ["AAPL"]

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

        # with open('./quotes/results.txt', 'a') as results:
        #     results.write('%r OPEN TRADE %s %r\n' %(time, value, verbage))

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
    make_decision(value, cs_0.date)

def get_atr(candles):
    sum = 0
    for candle in candles:
        sum +=candle['high'] - candle['low']
    return sum/len(candles)


def analyze_using_tda():
    api = td.TDAmeritradeAPI()

    for ticker in symbols_list:
        print(ticker)
        history = api.priceHistoryJSON(ticker)
        c = history['candles']
        print(c)
        print(api.quoteJSON(ticker))
        atr = get_atr(c)
        length = len(c)
        cs_0 = cs.CandleStick(c[length - 1])
        cs_1 = cs.CandleStick(c[length - 2])
        cs_2 = cs.CandleStick(c[length - 3])
        analyze_data(cs_0, cs_1, cs_2, atr)

analyze_using_tda()
