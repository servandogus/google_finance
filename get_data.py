# -*- coding: utf-8 -*-

import pandas as pd
import requests
from datetime import datetime, timedelta

# sources : http://www.theodor.io/scraping-google-finance-data-using-pandas/
# https://gist.github.com/lebedov/f09030b865c4cb142af1#file-google_finance_intraday-py-L29
# https://mktstk.com/2014/12/31/how-to-get-free-intraday-stock-data-with-python/
# http://www.networkerror.org/component/content/article/1-technical-wootness/44-googles-undocumented-finance-api.html

def get_googlefinance_data(symbol, interval=30, days=1, end_time=datetime.timestamp(datetime.now())):
    """
    Retrieve intraday stock data from Google Finance.
    Parameters
    ----------
    symbol : str
        Stock symbol.
    interval : int
        Interval between stock values in seconds.
    days : int
        Number of days of data to retrieve.
    end_time : float
        End time to retrieve. In second with UNIX format 
        (nb of seconds from 01/01/1970 UTC).
    Returns
    -------
    df : pandas.DataFrame
        DataFrame containing the "Datetime", "Close","High","Low","Open","Volume".
    """
    
    url_web = "http://www.google.com/finance/getprices"
    
    params = {   
        'q': symbol,
        'i': str(interval),
        'p': str(days) + 'd',
        'ts': str(int(end_time * 1000)),
        'f': 'd,o,h,l,c,v'
    }
    
    # retrieve data from url :
    r = requests.get(url_web,params=params)
    # split each line :    
    r = r.text.split()
    # remove 7 first line :
    r = r[7:]
    # split each line. r will be lists in a list :
    r = [l.split(",") for l in r] 
    # convert to a pandas DataFrame :
    DF = pd.DataFrame(r, columns=["Datetime","Close","High","Low","Open","Volume"])
    # remove the "a" character for the first timestamp :
    DF["Datetime"][0] = DF["Datetime"][0][1:]
    # convert the time stamp. It's presented in UNIX format.
    # Which represents the seconds from 1st January 1970 UTC.
    DF["Datetime"][0] = datetime.fromtimestamp(float(DF["Datetime"][0]))
    # convert the next timestamp :
    #DF["Datetime"][1:] = [DF["Datetime"][0] + int(x) * timedelta(seconds=interval) for x in DF["Datetime"][1:]]
    
    # return :
    return DF