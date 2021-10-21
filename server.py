# Import WebSocket client library (and others)
import websocket
import _thread
import time
import calendar;
import sys
import json
import signal
from websocket import create_connection
import numpy as np
import urllib
import json
import calendar;
import time;
import pandas as pd
import dataframe_image as dfi
import requests
from datetime import datetime
import re


def alarmfunction(signalnumber, frame):
	signal.alarm(1)
	api_output_book()

def api_output_book():
	global api_book
	bid = sorted(api_book["bid"].items(), reverse=True)
	ask = sorted(api_book["ask"].items())

	bid_list = []
	ask_list=[]
	for item in bid:
		bid_list.append([item[0],item[1][0],item[1][1]])
	gmt = time.gmtime()
	ts = calendar.timegm(gmt)	
	with open('{}_{}{}Book(Bid).npy'.format(api_symbol.split('/')[0],api_symbol.split('/')[1],ts), 'wb') as f:
			np.save(f, np.array(bid_list))	

	for item in ask:
		ask_list.append([item[0],item[1][0],item[1][1]])
	gmt = time.gmtime()
	ts = calendar.timegm(gmt)	
	with open('{}_{}{}Book(Ask).npy'.format(api_symbol.split('/')[0],api_symbol.split('/')[1],ts), 'wb') as f:
			np.save(f, np.array(ask_list))	
			

def api_update_book(side, data):
	global api_book,seg
	for x in data:
		price_level = x[0]

		if float(x[1]) != 0.0:
			api_book[side].update({price_level:[float(x[1]),float(x[2])]})
		else:
			if price_level in api_book[side]:
				api_book[side].pop(price_level)
	if side == "bid":
		api_book["bid"] = dict(sorted(api_book["bid"].items(), reverse=True)[:int(api_depth)])
	elif side == "ask":
		api_book["ask"] = dict(sorted(api_book["ask"].items())[:int(api_depth)])

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


api_feed = "book"
api_symbol = ""
api_depth = 1000
api_domain = "wss://ws.kraken.com/"
api_book = {"bid":{}, "ask":{}}
seg = 1
start_time = time.time()
end_time = time.time()
next_time = time.time()
pair=''


while True:
	for pair in par:
		api_symbol = pair
		# print(api_symbol)
		time.sleep(1)

		try:
			ws = create_connection(api_domain)
		except Exception as error:
			ws = create_connection(api_domain)

		api_data = '{"event":"subscribe", "subscription":{"name":"%(feed)s", "depth":%(depth)s}, "pair":["%(symbol)s"]}' % {"feed":api_feed, "depth":api_depth, "symbol":api_symbol}
		try:
			ws.send(api_data)
		except Exception as error:
			ws.send(api_data)

		while True:
			end_time = time.time()
			if end_time-start_time>10:
				start_time = time.time()
				api_output_book()
			if end_time-next_time>11:
				next_time = time.time()
				start_time = time.time()
				break	
			try:
				api_data = ws.recv()
			except KeyboardInterrupt:
				ws.close()
				sys.exit(0)
			except Exception as error:
				print("WebSocket message failed (%s)" % error)
				ws.close()
				sys.exit(1)
			api_data = json.loads(api_data)
			if type(api_data) == list:
				if "as" in api_data[1]:
					# print("api_data->",api_data[1])
					api_update_book("ask", api_data[1]["as"])
					api_update_book("bid", api_data[1]["bs"])
					time.sleep(1)
				elif "a" in api_data[1] or "b" in api_data[1]:
					key = api_data[1].keys()
					for x in api_data[1:]:
						if "a" in x and type(x)==dict:
							api_update_book("ask", x["a"])
						elif "b" in x and type(x)==dict:
							api_update_book("bid", x["b"])			
		ws.close()
sys.exit(1)