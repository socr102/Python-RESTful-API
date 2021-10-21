# Import WebSocket client library (and others)
import websocket
import _thread
import time
import urllib
import json
import calendar;
import pandas as pd
import dataframe_image as dfi
import requests
from datetime import datetime
import re
import numpy as np
trade={}
send_data=''
def ws_message(ws, message):
    if "trade" in message and '[' not in message:
        print(message)
    if "trade" in message and '[' in message:
        start=message.index("[[")
        end=message.index("]]")
        # print("************************")
        trade_type_start = message.index("trade")
        trade_type = message[trade_type_start+8:-2]
        # print(trade_type)
        result = message[start+2:end+1].replace("[","").replace("],","]").split(']')
        for item  in result:
            mid = []
            if item!='':
                for piece in item.replace('"','').split(','):
                    if piece=='':
                        continue
                    mid.append(piece)
                trade['{}'.format(trade_type)].append(mid)
        # print(trade['{}'.format(trade_type)])  
        for key in trade.keys():
            index = len(trade['{}'.format(key)])
            if index>=30:
                start_timestamp = trade['{}'.format(key)][0][2].split('.')[0]
                end_timestamp = trade['{}'.format(key)][index-1][2].split('.')[0]
                # print(start_timestamp,end_timestamp)
                with open('{}_{}_{}_{}trade.npy'.format(key.split('/')[0],key.split('/')[1],start_timestamp,end_timestamp), 'wb') as f:
                    print(np.array(trade['{}'.format(key)]))
                    np.save(f, np.array(trade['{}'.format(key)])) 
                    trade['{}'.format(key)] = []


def ws_open(ws):
    global send_data
    print(send_data)
    ws.send(send_data)
    # ws.send('{"event":"subscribe", "subscription":{"name":"trade"}, "pair":["XBT/USD","XRP/USD"]}')
def ws_thread(*args):
    try:
        ws = websocket.WebSocketApp("wss://ws.kraken.com/", on_open = ws_open, on_message = ws_message)
    except Exception as error:
        ws = websocket.WebSocketApp("wss://ws.kraken.com/", on_open = ws_open, on_message = ws_message)
    ws.run_forever()


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

for pair in par:
    trade.update({pair:[]})

send_data_header='{"event":"subscribe", "subscription":{"name":"trade"}, "pair":['
send_data_footer=']}'
count=0
for item in par:
    send_data_body=('"{}"'.format(par[count])+',')
    send_data = send_data_header+send_data_body[:-1]+send_data_footer
    _thread.start_new_thread(ws_thread, ())
    time.sleep(10)
    count+=1
    # break

# Continue other (non WebSocket) tasks in the main thread
while True:
    time.sleep(5)
    print("Main thread: %d" % time.time())