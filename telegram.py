import requests
import json
import time

import apiKey

key = apiKey.apiBot()

Mkey = {"keyboard": [["/meteo", "/cambio"], ["/seriea"]], "one_time_keyboard": False, "resize_keyboard": True}
Mkey = json.dumps(Mkey)
old_min = 61

def createKeyboard(arr, one=False, res=True):
  CustKeyb = {"keyboard": arr, "one_time_keyboard": False, "resize_keyboard": True}
  CustKeyb = json.dumps(CustKeyb)
  return CustKeyb

def getDataAndTimer(off):
  while True:
    m = int(time.strftime('%M'))
    global old_min
    if m != old_min:
      old_min = m
      return 'time'
    else:
      p = {'offset': off, 'limit': 1, 'timeout': 1800}
      data = requests.get("https://api.telegram.org/bot"+key+"/getUpdates", params=p)
      if data.status_code == 200:
        data = data.json()
        try:
          return data['result'][0]
        except IndexError:
          continue
      else:
        time.sleep(0.5)

def sendMess(text, chat_id, reply_to_message_id=None, reply_markup=Mkey, webPrev=False):
  par = {
    'chat_id': chat_id, 
    'text': text, 
    'parse_mode': 'Markdown', 
    'reply_to_message_id': reply_to_message_id, 
    'reply_markup' : reply_markup,
    'disable_web_page_preview': webPrev}
  a = requests.get("https://api.telegram.org/bot"+key+"/sendMessage", params=par) 
