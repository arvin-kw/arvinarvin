import requests
import pandas as pd  
import os
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

with open("trades_{}.txt".format(symbol), "w") as out_f:
    
    lendata =len(data.text)
    Remove_2last = data.text[158:]
    Remove_3last = Remove_2last.replace("},{", "\n")
    Remove_4last = Remove_3last.replace(":",",")
    out_fs = Remove_4last
    out_f.write(out_fs)
# dump resulting text to file
#with open("trades_{}.txt".format(symbol), "w") as out_f:
 #   out_f.write(data.text)

 

datapd = pd.read_csv(namefiletxt,delimiter=",",header=None)

datapd.to_csv(namefilecsv,index = None)
df = pd.read_csv(namefilecsv)
df.drop(df.columns[[0,2,4,6,8,10,12,14,15,16,17]], axis=1, inplace=True)
df.rename(columns={'1':'time','3':'high','5':'low','7':'open','9':'volfrom','11':'volto','13':'close'},inplace=True)
print(df)