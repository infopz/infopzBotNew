import time 
import json

import telegram
import altriCom
import sport

#BOT COMMANDS
def startCommand(chat, user):
  mess = 'Ciao *'+user['first_name']+'*\nBenvenuto su @infopzBot, ecco i comandi che puoi usare:\n*/seriea* : Ti fornisce anche in tempo reale risultati delle partite e la classifica di Serie A\n*/meteo* : Ti da le previsioni meteo orarie o giornaliere per la tua città\n*/cambio* : Effettua il cambio valuta Euro-Dollaro e viceversa\n\nPer qualsiasi informazione contatta @infopz'
  telegram.sendMess(mess, chat['id']) 
  print('@'+user['username']+' - /start')

def helpCommand(chat, user):
  mess = 'Ecco i comandi che puoi usare:\n*/seriea* : Ti fornisce (anche in tempo reale) i risultati delle partite e la classifica di Serie A\n*/meteo* : Ti da le previsioni meteo orarie o giornaliere per la tua città\n*/cambio* : Effettua il cambio valuta Euro-Dollaro e viceversa\n\nPer qualsiasi informazione contatta @infopz'
  telegram.sendMess(mess, chat['id']) 
  print('@'+user['username']+' - /help')

def helloCommand(chat, user):
  telegram.sendMess('Hello World', chat['id'])
  print('@'+user['username']+' - /hello')

def cambioCommand(chat, user):
  telegram.sendMess('/cambio: inserisci un valore seguito dal simbolo della valuta', chat['id'])
  var['comm'] = 'cambio'
  print('@'+user['username']+' - /cambio')

def serieaCommand(chat, user):
  keyb = [["\U0001F5DEPartite Giornata", "\U0001F51BPartite di Oggi"], ["\U0001F51CPartite di Domani", "\U0001F4CAClassifica"], ["\U000023F1RisultatiLive", "Ris ScorsaGiorn"]]
  keyb = telegram.createKeyboard(keyb)
  telegram.sendMess('/seriea: seleziona una opzione', chat['id'], reply_markup=keyb)
  var['comm'] = 'seriea'
  print('@'+user['username']+' - /seriea')

def meteoCommand(chat, user):
  keyb = [["\U0001F4CDModena", "\U0001F30DAltra città"]]
  keyb = telegram.createKeyboard(keyb)
  telegram.sendMess('/meteo: seleziona una opzione', chat['id'], reply_markup=keyb)
  var['comm'] = 'meteo'
  meteo['citta'] = ''
  meteo['tipoPrev'] = ''
  meteo['firstFase'] = True
  meteo['chiediCitt'] = False
  meteo['BtipoPrev'] = False
  print('@'+user['username']+' - /meteo')
  
#FUNCIONS FOR COMMANDS
def useMeteo(m):
  if meteo['BtipoPrev'] == True:
    if m == "\U0001F5DEGiornata":
      if meteo['citta'] == 'Modena':
        dat=altriCom.ottieniDati(str(44.647128),str(10.9252269))
        mess=altriCom.mOrario(dat, 10)
        telegram.sendMess(mess, chat['id'])
      else:
        cord=altriCom.trovaCord(meteo['citta'])
        dat=altriCom.ottieniDati(str(cord[0]),str(cord[1]))
        mess=altriCom.mOrario(dat, 10)
        telegram.sendMess(mess, chat['id'])
    if m == "\U0001F4C5Settimanale":
      if meteo['citta'] == 'Modena':
        dat=altriCom.ottieniDati(str(44.647128),str(10.9252269))
        mess=altriCom.mGiorni(dat)
        telegram.sendMess(mess, chat['id'])
      else:
        cord=altriCom.trovaCord(meteo['citta'])
        dat=altriCom.ottieniDati(str(cord[0]),str(cord[1]))
        mess=altriCom.mGiorni(dat)
        telegram.sendMess(mess, chat['id'])
    meteo['BtipoPrev'] = False
    var['comm'] = ''
  elif meteo['chiediCitt'] == True:
    meteo['citta'] = m
    keyb = [["\U0001F5DEGiornata", "\U0001F4C5Settimanale"]]
    keyb = telegram.createKeyboard(keyb)
    telegram.sendMess('/meteo: che previsione vuoi?', chat['id'], reply_markup=keyb)
    meteo['BtipoPrev'] = True
    meteo['chiediCitt'] = False
  elif meteo['firstFase'] == True:
    if m == "\U0001F4CDModena":
      keyb = [["\U0001F5DEGiornata", "\U0001F4C5Settimanale"]]
      keyb = telegram.createKeyboard(keyb)
      telegram.sendMess('/meteo: che previsione vuoi?', chat['id'], reply_markup=keyb)
      meteo['citta'] = 'Modena'
      meteo['BtipoPrev']=True
    else:
      Nkeyb = {'hide_keyboard':True}
      Nkeyb = json.dumps(Nkeyb)
      telegram.sendMess('/meteo: dimmi quale città', chat['id'], reply_markup=Nkeyb)
      meteo['chiediCitt'] = True
    meteo['firstFase'] = False


def serieaOutput(m, chat, user):
  a=["",""]
  oggi=var['giornata']
  if m=="\U0001F5DEPartite Giornata":
    a=sport.partiteGior(oggi)
  elif m=="\U000023F1RisultatiLive":
    a[0] = sport.live(oggi, var['contLive'])
    var['contLive']+=1
  elif m=="\U0001F4CAClassifica":
    a[1]=sport.classifica()
    a[0]="Ecco la classifica di Serie A"
  elif m=='\U0001F51BPartite di Oggi':
    a[0]='Ecco le partite di oggi'
    a[1]=sport.partiteOggiDom(oggi, 'oggi')
    if a[1]=='':
      a[0]='Non ci sono parite oggi'
  elif m=="Ris ScorsaGiorn":
    a = sport.partiteGior((oggi-1))
  elif m=='\U0001F51CPartite di Domani':
    a[0]='Ecco le partite di domani'
    a[1]=sport.partiteOggiDom(oggi, 'dom')
    if a[1]=='':
      a[0]='Non sono previste partite per domani'
  if a[0]!='':
    telegram.sendMess(a[0], chat['id'])
  if a[1]!='':
    telegram.sendMess(a[1], chat['id'])
  var['comm'] = ''


def execChange(chat, user):
  cambio=altriCom.ottieniCambio()
  n=message['text']
  ris = ''
  if (n[-1:])=='€':
     n=float(n[:-1])
     ris=round(float(n/cambio), 3)
     ris=str(n)+"€ sono "+str(ris)+"$"
  elif (n[-1:])=='$':
     n=float(n[:-1])
     ris=round(float(n*cambio), 3)
     ris=str(n)+"$ sono "+str(ris)+"€"
  else:
     ris = 'Valuta inserita non corretta o non fornita'
  telegram.sendMess(ris, chat['id'])
  var['comm'] = ''


def mess_received(chat, message, user):
  if message['text'][0] == '/':
    if message['text'].startswith('/start'):
      startCommand(chat, user)
    elif message['text'].startswith('/help'):
      helpCommand(chat, user)
    elif message['text'].startswith('/hello'):
      helloCommand(chat, user)
    elif message['text'].startswith('/cambio'):
      cambioCommand(chat, user)
    elif message['text'].startswith('/seriea'):
      serieaCommand(chat, user)
    elif message['text'].startswith('/meteo'):
      meteoCommand(chat, user)
  else:
    if var['comm'] == 'cambio':
      execChange(chat, user)
    elif var['comm'] == 'seriea':
      serieaOutput(message['text'], chat, user)
    elif var['comm'] == 'meteo':
      useMeteo(message['text'])
    print('@'+user['username']+' - '+message['text'])

def fmeteoDom(num, nome):
   cord=altriCom.trovaCord('Modena')
   dat=altriCom.ottieniDati(str(cord[0]),str(cord[1]))
   mess=altriCom.mOrario(dat, 12)
   telegram.sendMess(('Ciao '+nome+'!\nEcco le previsioni meteo per la giornata di domani'), num)
   telegram.sendMess(mess, num)

def timers():
  m = int(time.strftime('%M'))
  h = int(time.strftime('%H'))
  if h == 21 and m == 0:
    listMeteo = open('listMeteo', 'r')
    for lines in listMeteo.readlines():
        l = lines.split(' ', 2)
        fmeteoDom(l[0], l[1][:-1])
    listMeteo.close()
  if (h == 24 or h == 12) and m == 0:
    var['giornata'] = sport.trovaGiornata()
  if h == 24 and m == 0:
    print('ContLive utilizzati oggi: '+var['contLive'])
    var['contLive'] = 0 

def startAction():
  var['giornata'] = sport.trovaGiornata()
    

var = {'off': 0, 'comm': '', 'contLive': 0}
meteo = {'citta' : '', 'tipoPrev': ''}
print("Bot Started")
while True:
  d = telegram.getDataAndTimer(var['off'])
  try:
    if var['off'] == 0:
      startAction()
    if d == 'time':
      timers()
    else:
      var['off'] = d['update_id'] + 1
      user = d['message']['from']
      message = {'message_id': d['message']['message_id'], 'text': d['message']['text'], 'date': d['message']['date']}
      chat = d['message']['chat']
      mess_received(chat, message, user)
  except Exception as e:
    telegram.sendMess('Errore Interno\n'+str(e), 20403805)
    print('Errore Interno - '+str(e))
