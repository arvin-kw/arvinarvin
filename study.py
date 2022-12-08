import requests
import pandas as pd 
import pandas_ta as ta 
import os
import mplfinance as mpf
import matplotlib
namefiletxt = "trades_btcUSD.txt"
namefilecsv = 'trades_btcUSD.csv'

myfile="/Users/ARVIN/Desktop/pythonthings/trades_btcUSD.txt"
    ## If file exists, delete it ##
if os.path.isfile(myfile):
    os.remove(myfile)
myfilec="/Users/ARVIN/Desktop/pythonthings/trades_btcUSD.csv"
    ## If file exists, delete it ##
if os.path.isfile(myfilec):
    os.remove(myfilec)
symbol = "btcUSD"
url = 'https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USDT&limit=2000&toTs=-1&api_key=YOURKEYHERE'
data = requests.get(url)


#data cleaning :-)
with open("trades_{}.txt".format(symbol), "w") as out_f:
    
    lendata =len(data.text)
    Remove_2last = data.text[158:]
    Remove_3last = Remove_2last.replace("},{", "\n")
    Remove_4last = Remove_3last.replace(":",",")
    out_fs = Remove_4last
    out_f.write(out_fs)

 

datapd = pd.read_csv(namefiletxt,delimiter=",",header=None)
datapd.to_csv(namefilecsv,index = None)

df = pd.read_csv(namefilecsv)
df.drop(df.columns[[0,2,4,6,8,10,12,14,15,16,17]], axis=1, inplace=True)
df.rename(columns={'1':'dates','3':'highs','5':'lows','7':'opens','9':'volfrom','11':'volumes','13':'closes'},inplace=True)
df.to_csv(namefilecsv,index=True)

#####  add indicators #####
dfshow = pd.read_csv(namefilecsv,index_col=0,parse_dates=True)
dfshow.index.name = 'Date'
dfshow.shape

#calculate the MACD via pandas_ta
dfshow.ta.macd(close='close', append=True)
dfshow['MACD_12_26_9']= (dfshow['MACD_12_26_9'])/50
dfshow['MACDh_12_26_9']= (dfshow['MACDh_12_26_9'])/20
dfshow['MACDs_12_26_9']= (dfshow['MACDs_12_26_9'])/50
# Calculate the RSI via pandas_ta
dfshow.ta.rsi(close='close', append=True)
dfshow['RSI_14']= (dfshow['RSI_14']-50)/50


# Calculate the Aroon via pandas_ta
dfshow.ta.aroon( append=True)
dfshow['AROOND_14']= (dfshow['AROOND_14']-50)/50
dfshow['AROONU_14']= (dfshow['AROONU_14']-50)/50
dfshow['AROONOSC_14']= (dfshow['AROONOSC_14'])/100

# Calculate the ADX via pandas_ta
dfshow.ta.adx(append=True)
dfshow['DMN_14']= (dfshow['DMN_14']-30)/35
dfshow['DMP_14']= (dfshow['DMP_14']-30)/35
dfshow['ADX_14']= (dfshow['ADX_14']-40)/40
#calculate the TSI via pandas_ta
dfshow.ta.tsi(close='close',long=25,short=13,signal=13,append=True)
dfshow['TSIs_13_25_13']= dfshow['TSIs_13_25_13']/70
dfshow['TSI_13_25_13']= dfshow['TSI_13_25_13']/70

#######division#######
n= 0
while n<1994:
    dfshow.loc[n,'division']= dfshow.loc[n+5,"closes"]/dfshow.loc[n,"closes"]
    n +=1
dfshow.dropna(subset=['MACDh_12_26_9'],inplace = True)

dfshow.to_csv(namefilecsv,index=True)
print(dfshow)


