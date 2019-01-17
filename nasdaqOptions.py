'''
Copyright (C) 2015, Edouard 'tagoma' Tallent
Class fetching options data from www.nasdaq.com
Nasdaq_option_quotes.py v0.2 (Nov15)
QuantCorner @ https://quantcorner.wordpress.com
'''
from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd

class NasdaqOptions(object):
    '''
    Class NasdaqOptions fetches options data from Nasdaq website

    User inputs:
        Ticker: ticker
            - Ticker for the underlying
        Expiry: nearby
            - 1st Nearby: 1
            - 2nd Nearby: 2
            - etc ...
        Moneyness: money
            - All moneyness: all
            - In-the-money: in
            - Out-of-the-money: out
            - Near the money: near
        Market: market
            - Composite quote: Composite
            - Chicago Board Options Exchange: CBO
            - American Options Exchange: AOE
            - New York Options Exchange: NYO
            - Philadelphia Options Exchange: PHO
            - Montreal Options Exchange: MOE
            - Boston Options Exchange: BOX
            -  International Securities Exchange: ISE
            - Bats Exchange Options Market: BTO
            - NASDAQ Options: NSO
            - C2(Chicago) Options Exchange: C2O
            - NASDAQ OMX BX Options Exchange: BXO
            - MIAX: MIAX
        Option category: expi
            - Weekly options: week
            - Monthly options: stand
            - Quarterly options: quart
            - CEBO options (Credit Event Binary Options): cebo
    '''
    def __init__(self, ticker, nearby, money='near', market='cbo', expi='stan'):
        self.ticker = ticker
        self.nearby = nearby-1  # ' refers 1st nearby on NASDAQ website
        #self.type = type   # Deprecated
        self.market = market
        self.expi = expi
        if money == 'near':
            self.money = ''
        else:
            self.money =  '&money=' + money

    def get_options_table(self):
        '''
        - Loop over as many webpages as required to get the complete option table for the
        option desired
        - Return a pandas.DataFrame() object
        '''
        # Create an empty pandas.Dataframe object. New data will be appended to
        old_df = pd.DataFrame()

        # Variables
        loop = 0        # Loop over webpages starts at 0
        page_nb = 1     # Get the top of the options table
        flag = 1        # Set a flag that will be used to call get_pager()
        old_rows_nb = 0 # Number of rows so far in the table

        # Loop over webpages
        while loop < int(page_nb):
            # Construct the URL
            '''url = 'http://www.nasdaq.com/symbol/' + self.ticker + '/option-chain?dateindex='\
               + str(self.nearby) + '&callput=' + self.type + '&money=all&expi='\
               + self.expi + '&excode=' + self.market + '&page=' + str(loop+1)'''
            url = 'http://www.nasdaq.com/symbol/' + self.ticker + '/option-chain?excode=' + self.market + self.money + '&expir=' + self.expi + '&dateindex=' + str(self.nearby) + '&page=' + str(loop+1)
            print(url)
            # Query NASDAQ website
            try:
                response = requests.get(url)#, timeout=0.1)
            # DNS lookup failure
            except requests.exceptions.ConnectionError as e:
                print('''Webpage doesn't seem to exist!\n%s''' % e)
                pass
            # Timeout failure
            except requests.exceptions.ConnectTimeout as e:
                print('''Slow connection!\n%s''' % e)
                pass
            # HTTP error
            except requests.exceptions.HTTPError as e:
                print('''HTTP error!\n%s''' % e)
                pass

            # Get webpage content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Determine actual number of pages to loop over
            if flag == 1:   # It is run only once
                # Get the number of page the option table lies on
                last_page_raw = soup.find('a', {'id': 'quotes_content_left_lb_LastPage'})
                last_page = re.findall(pattern='(?:page=)(\d+)', string=str(last_page_raw))
                page_nb = ''.join(last_page)
                flag = 0

            # Extract table containing the option data from the webpage
            table = soup.find_all('table')[4] # table #4 in the webpage is the one of interest
            print(table)
            # Extract option data from table as a list
            elems = table.find_all('td') # Python object
            lst = [elem.text for elem in elems] # Option data as a readable list
            print("aaaaaaaaaaaaaaaaa")
            print(lst)
            # Rearrange data and create a pandas.DataFrame
            arr = np.array(lst)
            reshaped = arr.reshape((len(lst)/16, 16))
            new_df = pd.DataFrame(reshaped)
            frames = [old_df, new_df]
            old_df = pd.concat(frames)
            rows_nb = old_df.shape[0]

            # Increment loop counter
            if rows_nb > old_rows_nb:
                loop+=1
                old_rows_nb = rows_nb
            elif rows_nb == old_rows_nb:
                print('Problem while catching data.\n## You must try again. ##')
                pass
            else:   # Case where rows have been deleted
                    # which shall never occur
                print('Failure!\n## You must try again. ##')
                pass

        # Name the column 'Strike'
        old_df.rename(columns={old_df.columns[8]:'Strike'}, inplace=True)

        ## Split into 2 dataframes (1 for calls and 1 for puts)
        calls = old_df.ix[:,1:7]
        puts = old_df.ix[:,10:16] # Slicing is not incluse of the last column

        # Set 'Strike' column as dataframe index
        calls = calls.set_index(old_df['Strike'])
        puts = puts.set_index(old_df['Strike'])

        ## Headers names
        headers = ['Last', 'Chg', 'Bid', 'Ask', 'Vol', 'OI']
        calls.columns = headers
        puts.columns = headers

        return calls, puts

# if __name__ == '__main__':
#     # Get data for Dec-15 SPX options, Dec-15 being the 2nd nearby
#     options = NasdaqOptions('SPX',2)
#     calls, puts = options.get_options_table()

#     # Write on the screen
#     print('\n######\nCalls:\n######\n', calls,\
#         '\n\n######\nPuts:\n######\n', puts)
