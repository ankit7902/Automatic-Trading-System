from fyers_apiv3 import fyersModel
import pandas as pd
import datetime as dt

with open('access.txt', 'r') as a:
    access_token = a.read()
client_id = 'MYR9U8HEHU-100'

fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

data = {
    "symbol": "NSE:RELIANCE-EQ",  #yha se ham stock ka nm bhi chnge kr skte ha 
    "resolution": "1",
    "date_format": "1",
    "range_from": "2024-04-01", 
    "range_to": "2024-04-15",  
    "cont_flag": "1"
}
response = fyers.history(data=data)
print(response)
data = response['candles']
df = pd.DataFrame(data)
print(df)

df.columns=['date','open','high','low','close','volume'] #yha row and column ka naam chnge kiya ha 
df['date']=pd.to_datetime(df['date'],unit='s')
df.date=(df.date.dt.tz_localize('UTC').dt.tz_convert('Asia/kolkata')) #iska use kiya ha time zone change krne ke lie
print(df)

df['date']=df['date'].dt.tz_localize(None) #iska use kiya ha data m timezone niklne ke liye 
df=df.set_index('date') #iska use kia ha numbering htane ke liye 
print(df)
df.to_csv('data.csv')
print(dt.datetime.now()) 

import datetime as dt
from fyers_apiv3 import fyersModel
import pandas as pd

def fetchOHLC(ticker, interval, duration):#yha  pe ham 100 days tk data nikal skte ha 
    with open('access.txt','r') as a:
        access_token = a.read()
    client_id = 'MYR9U8HEHU-100'
    fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")
    instrument = ticker
    data = {
        "symbol": instrument,
        "resolution": interval,
        "date_format": "1",
        "range_from": dt.date.today() - dt.timedelta(days=duration),  
        "range_to": dt.date.today(),
        "cont_flag": "1"
    }
    response = fyers.history(data=data)
    sdata = response['candles']
    sdata = pd.DataFrame(sdata)
    sdata.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    sdata['date'] = pd.to_datetime(sdata['date'], unit='s')
    sdata['date'] = sdata['date'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
    sdata['date'] = sdata['date'].dt.tz_localize(None)  # Remove timezone information
    sdata = sdata.set_index('date')
    
    return sdata

ticker = 'NSE:NIFTYBANK-INDEX'
data = fetchOHLC(ticker, '1', 50)
print(data)


def gethistory(symbol1, type, duration): #get more than 100 days of data
    symbol = "NSE:" + symbol1 + "-" + type
    start = dt.date.today() - dt.timedelta(days=duration)
    end = dt.date.today()
    sdata = pd.DataFrame()

    while start <= end:
        end2 = start + dt.timedelta(days=60)  # Assuming each API call fetches data for up to 60 days
        data = {
            "symbol": symbol,
            "resolution": "1",
            "date_format": "1",
            "range_from": start,
            "range_to": end2
        }
        s = fyers.history(data)
        s = pd.DataFrame(s['candles'])
        sdata = pd.concat([sdata, s], ignore_index=True)
        start = end2 + dt.timedelta(days=1)

    sdata.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    sdata['date'] = pd.to_datetime(sdata['date'], unit='s')
    sdata['date'] = sdata['date'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')
    sdata['date'] = sdata['date'].dt.tz_localize(None)
    sdata = sdata.set_index('date')
    
    return sdata

data = gethistory('NIFTYBANK', 'INDEX', 5000) 
print(data)
data.to_csv('niftybank.csv') 