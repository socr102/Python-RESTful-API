import urllib
import json
import calendar;
import time;
import pandas as pd
import dataframe_image as dfi
import requests
from datetime import datetime
import re
import numpy as np
tiempo=1
url="https://api.kraken.com/0/public/AssetPairs?"
with urllib.request.urlopen(url) as url:
    datos1=json.loads(url.read().decode())
datos7=datos1["result"]    
claves=list(datos7.keys())
n=0
listapares=[]
for i in range(len(datos7)):
    try:
        datos8=datos7[claves[n]]
        n=n+1
        par=datos8["wsname"]
        try:
            par= re.sub('XBT', 'BTC', par)
        except:
            pass
        try:
            par= re.sub('XDG', 'DOGE', par)
        except:
            pass
        listapares.append(par)
    except:
        pass
par=listapares

# for pair in par:
#     gmt = time.gmtime()
#     ts = calendar.timegm(gmt)
#     dict_train = requests.get("https://api.kraken.com/0/public/Depth?pair={}&count={}".format(pair,500)).json()
#     pair_ask_list = []
#     for i in range(len(dict_train["result"]["{}".format(pair)]["asks"])):
#         pair_ask_list.append("{}".format(pair))
#     pair_bid_list = []
#     for i in range(len(dict_train["result"]["{}".format(pair)]["bids"])):
#         pair_bid_list.append("{}".format(pair))    

#     train_ask = pd.DataFrame(dict_train["result"]["{}".format(pair)]["asks"], columns =['price','quantity','timestamp'])
#     train_ask['pair'] = pair_ask_list
#     train_bid = pd.DataFrame(dict_train["result"]["{}".format(pair)]["bids"], columns =['price','quantity','timestamp'])
#     train_bid['pair'] = pair_bid_list

#     print("*********ask**********")
#     # print(pair.split('/'))
#     print(train_ask.to_numpy())
#     with open('{}_{}{}Book(Ask).npy'.format(pair.split('/')[0],pair.split('/')[1],ts), 'wb') as f:
#         np.save(f, np.array(train_ask.to_numpy()))
#     print("********bid************")
#     print(train_bid.to_numpy())
#     with open('{}_{}{}Book(Bid).npy'.format(pair.split('/')[0],pair.split('/')[1],ts), 'wb') as f:
#         np.save(f, np.array(train_bid.to_numpy()))
    
#     print("**********trade*******")
#     pair_trade_list = []
#     dict_trade = requests.get("https://api.kraken.com/0/public/Trades?pair={}&since=0".format(pair)).json()
#     for i in range(len(dict_trade["result"]["{}".format(pair)])):
#         pair_trade_list.append("{}".format(pair)) 
#     trade = pd.DataFrame(dict_trade["result"]["{}".format(pair)],columns=['price','quantity','timestamp','type','action',''])
        
#     # for i in range(9):
#     #     dict_trade = requests.get("https://api.kraken.com/0/public/Trades?pair={}&since=0".format(pair)).json()
#     #     for i in range(len(dict_trade["result"]["{}".format(pair)])):
#     #         pair_trade_list.append("{}".format(pair)) 
#     #     trade1 = pd.DataFrame(dict_trade["result"]["{}".format(pair)],columns=['price','quantity','timestamp','type','action',''])
#     #     print(trade1)
#         # trade = np.vstack((np.array(trade.to_numpy()),np.array(trade1.to_numpy())))
#     trade['pair'] = pair_trade_list
#     with open('{}_{}_{}_{}_Trades.npy'.format(pair.split('/')[0],pair.split('/')[1],trade.loc[0][2],trade.loc[999][2]), 'wb') as f:
#         np.save(f, np.array(trade.to_numpy()))
#     break