import os
import requests
import pandas as pd
from urls import ACCOUNTS, INSTRUMENTS, QUOTES, ACCESS2, HISTORY, OPTIONCHAIN


# HOST, PORT = 'example.com', 443
#HOST = "wss://" + userPrincipalsResponse.streamerInfo.streamerSocketUrl + "/ws"
#HOST = "wss://streamer-ws.tdameritrade.com/ws"
#PORT = 8080

class TDAmeritradeAPI(object):
    def __init__(self, access_token=None, accountIds=None):
        self._token = ACCESS2
        self.accountIds = accountIds or []

    def _headers(self):
        return {'Authorization': 'Bearer ' + self._token}

    def quote(self, symbol):
        return requests.get(QUOTES,
                            headers=self._headers(),
                            params={'symbol': symbol.upper()}).json()

    def quoteDF(self, symbol):
        x = self.quote(symbol)
        return pd.DataFrame(x).T.reset_index(drop=True)

    def quoteJSON(self, symbol):
        x = self.quote(symbol)
        return x

    def options(self, symbol):
        return requests.get(OPTIONCHAIN,
                            headers=self._headers(),
                            params={'symbol': symbol.upper(),
                            'strikeCount': 2,
                            'toDate': '2019-02-22'}).json()

    def optionsDF(self, symbol):
        ret = []
        dat = self.options(symbol)
        for date in dat['callExpDateMap']:
            for strike in dat['callExpDateMap'][date]:
                ret.extend(dat['callExpDateMap'][date][strike])
        for date in dat['putExpDateMap']:
            for strike in dat['putExpDateMap'][date]:
                ret.extend(dat['putExpDateMap'][date][strike])

        df = pd.DataFrame(ret)
        for col in ('tradeTimeInLong', 'quoteTimeInLong', 'expirationDate', 'lastTradingDay'):
            df[col] = pd.to_datetime(df[col], unit='ms')
        return df

    def optionsJSON(self, symbol):
        ret = []
        dat = self.options(symbol)
        return dat
        # for date in dat['callExpDateMap']:
        # for strike in dat['callExpDateMap'][date]:
        # ret.extend(dat['callExpDateMap'][date][strike])
        # for date in dat['putExpDateMap']:
        # for strike in dat['putExpDateMap'][date]:
        # ret.extend(dat['putExpDateMap'][date][strike])
        #
        # df = pd.DataFrame(ret)
        # for col in ('tradeTimeInLong', 'quoteTimeInLong', 'expirationDate', 'lastTradingDay'):
        # df[col] = pd.to_datetime(df[col], unit='ms')
        # return df


# def connect():
#     # print(SSL._CERTICICATE_PATH_LOCATIONS)
#     # DEFINE THE SOCKET
#     sock = socket.socket(socket.AF_INET)
#     print(sock)
#     # APPLY SOCKET WRAPPER
#     context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
#     print(context)
#     #context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
#     conn = context.wrap_socket(sock, server_hostname=HOST)
#
#     # CONNECT TO SOCKET
#     try:
#         conn.connect((HOST, PORT))
#         print("Connected")
#         #handle(conn)
#     finally:
#         conn.close()
#
# #def create_socket():
#
# def close():
#     conn.close()

#def tda_get():

#def tda_quote():

def log_in():
    request = json.dumps({
      "requests": [
        {
          "service": "ADMIN",
          "command": "LOGIN",
          "requestid": 0,
          "account": userPrincipalsResponse.accounts[0].accountId,
          "source": userPrincipalsResponse.streamerInfo.appId,
          "parameters": {
              "credential": jsonToQueryString(credentials),
              "token": userPrincipalsResponse.streamerInfo.token,
              "version": "1.0"
          }
        }
      ]
    })

    # conn.send(JSON.stringify(request))

def log_out():
    request = json.dumps({
      "requests": [
        {
          "service": "ADMIN",
          "command": "LOGOUT",
          "requestid": 1,
          "account": userPrincipalsResponse.accounts[0].accountId,
          "source": userPrincipalsResponse.streamerInfo.appId,
          "parameters": {
              "credential": jsonToQueryString(credentials),
              "token": userPrincipalsResponse.streamerInfo.token,
              "version": "1.0"
          }
        }
      ]
    })

    # conn.send(JSON.stringify(request));
