# -*- coding: utf-8 -*-
import os
import telebot
import time
import telebot
import random
import threading
from emoji import emojize
from telebot import types
from pymongo import MongoClient
import traceback

from requests.exceptions import ReadTimeout
from requests.exceptions import ConnectionError


token = os.environ['TELEGRAM_TOKEN']
world = os.environ['worldtoken']
bot = telebot.TeleBot(token)
world=telebot.TeleBot(world)
alisa=telebot.TeleBot(os.environ['alisa'])
miku=telebot.TeleBot(os.environ['miku'])
lena=telebot.TeleBot(os.environ['lena'])
slavya=telebot.TeleBot(os.environ['slavya'])
uliana=telebot.TeleBot(os.environ['uliana'])
electronic=telebot.TeleBot(os.environ['electronic'])
zhenya=telebot.TeleBot(os.environ['zhenya'])

client1=os.environ['database']
client=MongoClient(client1)
db=client.everlastingsummer
users=db.users

yestexts=['хорошо, ольга дмитриевна!','хорошо!','я этим займусь!','я готов!','я готова!']
notexts=['простите, но у меня уже появились дела.']

botadmins=[441399484]
el_admins=[]
al_admins=[512006137]
ul_admins=[652585389]
mi_admins=[268486177]
le_admins=[]
sl_admins=[]
od_admins=[629070350]
zh_admins=[390362465]


symbollist=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
           'а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я', ' ']


works=[
           {'name':'concertready',
              'value':0,
              'lvl':1
             },
           {'name':'sortmedicaments',
              'value':0,
              'lvl':2
             },
           {'name':'checkpionerssleeping',
              'value':0,
              'lvl':1
             },
          
           {'name':'pickberrys',
            'value':0,
            'lvl':2
            },
           {'name':'bringfoodtokitchen',
            'value':0,
            'lvl':2
            },
           {'name':'helpinmedpunkt',
            'value':0,
            'lvl':1
            },
           {'name':'helpinkitchen',
            'value':0,
            'lvl':2
            },
           
           {'name':'cleanterritory',
              'value':0,
              'lvl':3
             },
           {'name':'washgenda',
              'value':0,
              'lvl':3
             }
]

def worktoquest(work):
    if work=='concertready':
        return 'Подготовиться к вечернему концерту'
    if work=='sortmedicaments':
        return 'Отсортировать лекарства в медпункте'
    if work=='checkpionerssleeping':
        return 'На вечер - проследить за тем, чтобы в 10 часов все были в домиках'
    if work=='pickberrys':
        return 'Собрать ягоды для торта'
    if work=='bringfoodtokitchen':
        return 'Принести на кухню нужные ингридиенты'
    if work=='helpinmedpunkt':
        return 'Последить за медпунктом, пока медсестры не будет'
    if work=='helpinkitchen':
        return 'Помочь с приготовлением еды на кухне'
    if work=='cleanterritory':
        return 'Подмести территорию лагеря'
    if work=='washgenda':
        return 'Помыть памятник на главной площади'

def lvlsort(x):
   finallist=[]
   for ids in works:
      if ids['lvl']==x and ids['value']==0:
         finallist.append(ids['name'])
   return finallist
           

@bot.message_handler(content_types=['sticker'])
def stickercatch(m):
    bot.send_message(441399484,str(m.sticker.file_id))
    print(m.sticker.file_id)
           
           
           
@bot.message_handler(commands=['start'])
def start(m):
 if m.chat.id==m.from_user.id:
  x=users.find_one({'id':m.from_user.id})
  if x==None:
    users.insert_one(createuser(m.from_user.id, m.from_user.first_name, m.from_user.username))
    bot.send_chat_action(-1001351496983,'typing')
    time.sleep(4)
    bot.send_message(m.chat.id,'Здраствуй, пионер! Меня зовут Ольга Дмитриевна, я буду твоей вожатой. Впереди тебя ждёт интересная жизнь в лагере "Совёнок"! '+
                     'А сейчас скажи нам, как тебя зовут (следующим сообщением).')
  else:
   if x['setgender']==0 and x['setname']==0:
    x=users.find_one({'id':m.from_user.id})
    bot.send_chat_action(m.chat.id,'typing')
    time.sleep(4)
    if x['working']==1:
       bot.send_message(m.chat.id, 'Здраствуй, пионер! Вижу, ты занят. Молодец! Не буду отвлекать.')
    else:
       bot.send_message(m.chat.id, 'Здраствуй, пионер! Отдыхаешь? Могу найти для тебя занятие!')
  


@bot.message_handler(commands=['work'])
def work(m):
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
      if x['setgender']==0 and x['setname']==0:
        if x['working']==0:
          if x['waitforwork']==0:
           if x['relaxing']==0:
            bot.send_chat_action(m.chat.id,'typing')
            time.sleep(4)
            bot.send_message(m.chat.id, random.choice(worktexts), reply_to_message_id=m.message_id)
            users.update_one({'id':m.from_user.id},{'$set':{'waitforwork':1}})
            t=threading.Timer(random.randint(60,120),givework, args=[m.from_user.id])
            t.start()
           else:
              bot.send_chat_action(m.chat.id,'typing')
              time.sleep(4)
              bot.send_message(m.chat.id, 'Нельзя так часто работать! Хвалю, конечно, за трудолюбивость, но сначала отдохни.', reply_to_message_id=m.message_id)
           


def givework(id):
    nosend=0
    x=users.find_one({'id':id})
    if x!=None:
       text=''
       if x['gender']=='male':
          gndr=''
       if x['gender']=='female':
          gndr='а'
       quests=lvlsort(1)  
       sendto=types.ForceReply(selective=False)
     
       quest=None
       bot.send_chat_action(id,'typing')
       time.sleep(4)
       if x['OlgaDmitrievna_respect']>=75:
           quests=lvlsort(1) 
           text+='Так как ты у нас ответственный пионер, ['+x['pionername']+'](tg://user?id='+str(id)+'), у меня для тебя есть важное задание!\n'
           if len(quests)>0:
               quest=random.choice(lvl1quests)
               users.update_one({'id':id},{'$set':{'prepareto':quest}})
               print('Юзер готовится к квесту: '+quest)
               users.update_one({'id':id},{'$set':{'answering':1}})
               t=threading.Timer(60, cancelquest, args=[id])
               t.start()
           else:
               text='Важных заданий на данный момент нет, ['+x['pionername']+'](tg://user?id='+str(id)+')... Но ничего, обычная работа почти всегда найдётся!\n'
               questt=[]
               quest2=lvlsort(2)
               quest3=lvlsort(3) 
               for ids in quest2:
                   questt.append(ids)
               for ids in quest3:
                   questt.append(ids)
               if len(questt)>0:
                  quest=random.choice(questt)
                  print('Юзер готовится к квесту: '+quest)
                  users.update_one({'id':id},{'$set':{'prepareto':quest}})
                  users.update_one({'id':id},{'$set':{'answering':1}})
               else:
                   nosend=1
                   bot.send_message(-1001351496983, 'К сожалению, заданий для тебя сейчас нет, ['+x['pionername']+'](tg://user?id='+str(id)+'). Но за желание помочь лагерю хвалю!', parse_mode='markdown')
       elif x['OlgaDmitrievna_respect']>=40:
           text+='Нашла для тебя занятие, ['+x['pionername']+'](tg://user?id='+str(id)+')!\n'
           lvl2quests=lvlsort(2) 
           if len(lvl2quests)>0:
                quest=random.choice(lvl2quests)
                sendto=types.ForceReply(selective=False)
                users.update_one({'id':id},{'$set':{'prepareto':quest}})
                users.update_one({'id':id},{'$set':{'answering':1}})
                print('Юзер готовится к квесту: '+quest)
                t=threading.Timer(60, cancelquest, args=[id])
                t.start()
           else:
               lvl3quests=lvlsort(3)
               if len(lvl3quests)>0:
                   quest=random.choice(lvl3quests)
                   sendto=types.ForceReply(selective=False)
                   print('Юзер готовится к квесту: '+quest)
                   users.update_one({'id':id},{'$set':{'prepareto':quest}})
                   users.update_one({'id':id},{'$set':{'answering':1}})
                   t=threading.Timer(60, cancelquest, args=[id])
                   t.start()
               else:
                   nosend=1
                   bot.send_message(-1001351496983, 'К сожалению, заданий для тебя сейчас нет, ['+x['pionername']+'](tg://user?id='+str(id)+'). Но за желание помочь лагерю хвалю!', parse_mode='markdown')
            
       else:
           text+='Ответственные задания я тебе пока что доверить не могу, ['+x['pionername']+'](tg://user?id='+id+'). Чтобы вырастить из тебя образцового пионера, начнем с малого.\n'
           lvl3quest=lvlsort(3) 
           if len(lvl3quests)>0:
             quest=random.choice(lvl3quests)
             sendto=types.ForceReply(selective=False)
             users.update_one({'id':id},{'$set':{'prepareto':quest}})
             print('Юзер готовится к квесту: '+quest)
             users.update_one({'id':id},{'$set':{'answering':1}})
             t=threading.Timer(60, cancelquest, args=[id])
             t.start()
           else:
             nosend=1
             bot.send_message(-1001351496983, 'К сожалению, заданий для тебя сейчас нет, ['+x['pionername']+'](tg://user?id='+str(id)+'). Но за желание помочь лагерю хвалю!', parse_mode='markdown')
       if quest=='pickberrys':
                     text+='Собери-ка ягоды для вечернего торта! Ты готов, пионер?'
       if quest=='bringfoodtokitchen':
                     text+='На кухне не хватает продуктов. Посети библиотеку, кружок кибернетиков и медпункт, там должны быть некоторые ингридиенты. Справишься?'
       if quest=='washgenda':
            if x['gender']=='female':
                   gndr='ла'
            text+='Наш памятник на главной площади совсем запылился. Не мог'+gndr+' бы ты помыть его?'
       if quest=='cleanterritory':
                text+='Территория лагеря всегда должна быть в чистоте! Возьми веник и совок, и подмети здесь всё. Справишься?'    
       if quest=='concertready':
                  text+='Тебе нужно подготовить сцену для сегодняшнего выступления: принести декорации и аппаратуру, которые нужны выступающим пионерам, выровнять стулья. Приступишь?'
       if quest=='sortmedicaments':
                  text+='Тебе нужно помочь медсестре: отсортировать привезённые недавно лекарства по ящикам и полкам. Возьмёшься?'
       if quest=='checkpionerssleeping':
                  text+='Уже вечер, и все пионеры должны в это время ложиться спать. Пройдись по лагерю и поторопи гуляющих. Готов'+gndr+'?'
       if quest=='helpinmedpunkt':
                   text+='Медсестре нужна твоя помощь: ей срочно нужно в райцентр. Посидишь в медпункте за неё?'
       if quest=='helpinkitchen':
              gndr2=''
              if x['gender']=='female':
                   gndr='а'
                   gndr2='ла'
              text+='На кухне не хватает людей! Было бы хорошо, если бы ты помог'+gndr2+' им с приготовлением. Готов'+gndr+'?'
       if nosend==0:
           users.update_one({'id':id},{'$set':{'answering':1}})
           bot.send_message(-1001351496983, text, parse_mode='markdown')
           
def cancelquest(id):
    x=users.find_one({'id':id})
    if x!=None:
        if x['answering']==1:
            users.update_one({'id':id},{'$set':{'prepareto':None}})
            users.update_one({'id':id},{'$set':{'answering':0}})
            users.update_one({'id':id},{'$set':{'waitforwork':0}})
            bot.send_message(-1001351496983, '['+x['pionername']+'](tg://user?id='+str(id)+')! Почему не отвечаешь? Неприлично, знаешь ли. Ну, раз не хочешь, найду другого пионера для этой работы.',parse_mode='markdown')
            
            


worktexts=['Ну что, пионер, скучаешь? Ничего, сейчас найду для тебя подходящее занятие! Подожди немного.',
  'Бездельничаешь? Сейчас я это исправлю! Подожди пару минут, найду тебе занятие.']


@bot.message_handler(commands=['gamestest'])
def gamestest(m):
    eveninggames()

  
####################################### OLGA ##############################################
@bot.message_handler(commands=['control'])
def odcontrol(m):
    if m.from_user.id in botadmins or m.from_user.id in od_admins:
        if odstats['controller']==None:
            odstats['controller']={'id':m.from_user.id,
                                     'name':m.from_user.first_name}
            bot.send_message(m.from_user.id, 'Здравствуй, пионер. Быть вожатым - большая ответственность! Не опозорь меня!')
        else:
            bot.send_message(m.from_user.id, 'Мной уже управляет '+odstats['controller']['name']+'!')
            
@bot.message_handler(commands=['stopcontrol'])
def odstopcontrol(m):
    if odstats['controller']!=None:
        if odstats['controller']['id']==m.from_user.id:
            odstats['controller']=None
            bot.send_message(m.from_user.id, 'Ты больше не управляешь мной!')
            
                      
                      
@bot.message_handler(content_types=['sticker'])
def stickercatchod(m):  
    if odstats['controller']!=None:
        controller=odstats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                bot.send_sticker(-1001351496983, m.sticker.file_id)



@bot.message_handler()
def messag(m):
  if m.from_user.id==m.chat.id:
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
        if x['setname']==1:
            nott=0
            for ids in m.text:
                if ids.lower() not in symbollist:
                    nott=1
            if nott==0:
                users.update_one({'id':m.from_user.id},{'$set':{'pionername':m.text}})
                users.update_one({'id':m.from_user.id},{'$set':{'setname':0}})
                bot.send_message(m.chat.id, 'Отлично! И еще одна просьба... Прости конечно, но это нужно для документа, в котором '+
                                 'хранится информация обо всех пионерах. Я, конечно, сама вижу, но это надо сделать твоей рукой. '+
                                 'Напиши вот тут свой пол (М или Д).')
            else:
                bot.send_message(m.chat.id, 'Нет-нет! Имя может содержать только буквы русского и английского алфавита!')
        else:
            if x['setgender']==1:
                  da=0
                  if m.text.lower()=='м':
                        users.update_one({'id':m.from_user.id},{'$set':{'setgender':0}})
                        users.update_one({'id':m.from_user.id},{'$set':{'gender':'male'}})
                        da=1
                  elif m.text.lower()=='д':
                        users.update_one({'id':m.from_user.id},{'$set':{'setgender':0}})
                        users.update_one({'id':m.from_user.id},{'$set':{'gender':'female'}})
                        da=1
                  if da==1:
                      bot.send_message(m.chat.id, 'Добро пожаловать в лагерь, '+x['pionername']+'! Заходи в '+
                                 '@(Ссылка на лагерь пока неизвестна, подождите немного), и знакомься с остальными пионерами!')
      
  else:
    x=users.find_one({'id':m.from_user.id})
    if x!=None:
      if x['setgender']==0 and x['setname']==0:
        if m.reply_to_message!=None:
          if m.reply_to_message.from_user.id==636658457:
             if x['answering']==1:
               if m.text.lower() in yestexts:
                 users.update_one({'id':m.from_user.id},{'$set':{'answering':0}})
                 users.update_one({'id':m.from_user.id},{'$set':{'working':1}})
                 users.update_one({'id':m.from_user.id},{'$set':{'waitforwork':0}})
                 dowork(m.from_user.id)
                 users.update_one({'id':m.from_user.id},{'$set':{'prepareto':None}})
                 bot.send_message(m.chat.id,'Молодец, пионер! Как закончишь - сообщи мне.',reply_to_message_id=m.message_id )
        lineykatexts=['я здесь, ольга дмитриевна!', 'я пришёл','я пришла','я пришёл!', 'я пришла!', 'я здесь!','я здесь','я пришел','я пришел!']        
        if odstats['waitforlineyka']==1:
                yes=0
                for ids in lineykatexts:
                    if m.text.lower() in ids:
                        yes=1
                if yes==1:
                    if x['gender']=='male':
                        g='шёл'
                    else:
                        g='шла'
                    odstats['lineyka'].append('['+x['pionername']+'](tg://user?id='+str(id)+')')
                    bot.send_message(m.chat.id,'А вот и ['+x['pionername']+'](tg://user?id='+str(id)+') при'+g+' на линейку!')
                    
                    
                    
  if odstats['controller']!=None:
        controller=odstats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                if m.text.split(' ')[0]!='/pm' and m.text.split(' ')[0]!='/r':
                    msg=bot.send_message(-1001351496983, m.text)
                    for ids in ctrls:
                        if ids['controller']!=None and ids['bot']!=bot:
                            if m.chat.id==-1001351496983:
                                x='(Общий чат)'
                            else:
                                x='(ЛС)'
                            try:
                                ids['bot'].send_message(ids['controller']['id'], x+'\n'+msg.from_user.first_name+' (`'+str(msg.from_user.id)+'`) (❓'+str(msg.message_id)+'⏹):\n'+msg.text, parse_mode='markdown')
                            except Exception as E:
                                bot.send_message(441399484, traceback.format_exc())   
                elif m.text.split(' ')[0]=='/pm':
                    try:
                        text=m.text.split(' ')
                        t=''
                        i=0
                        for ids in text:
                            if i>1:
                                t+=ids+' '
                            i+=1
                        bot.send_message(int(m.text.split(' ')[1]), t)
                    except:
                        bot.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')

            else:
                try:
                    i=0
                    cid=None
                    eid=None
                    for ids in m.reply_to_message.text:
                        print(ids)
                        if ids=='❓':
                            cid=i+1
                        if ids=='⏹':
                            eid=i
                        i+=1
                    print('cid')
                    print(cid)
                    print('eid')
                    print(eid)
                    msgid=m.reply_to_message.text[cid:eid]
                    bot.send_message(-1001351496983, m.text, reply_to_message_id=int(msgid))
                    
                except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                    bot.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')
                    
                                          
        
        else:
            if m.chat.id==-1001351496983:
                x='(Общий чат)'
            else:
                x='(ЛС)'
            try:
                bot.send_message(controller['id'], x+'\n'+m.from_user.first_name+' (`'+str(m.from_user.id)+'`) (❓'+str(m.message_id)+'⏹):\n'+m.text, parse_mode='markdown')
           
            except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())






def reloadquest(index):
    works[index]['value']=0
    print('Квест '+works[index]['name']+' обновлён!')
    
    
    
def dowork(id):
   x=users.find_one({'id':id})
   i=0
   index=None
   for ids in works:
       if x['prepareto']==ids['name']:
          work=ids
          index=i
       i+=1
   if index!=None:
    works[index]['value']=1
    hour=gettime('h')
    minute=gettime('m')
    z=None
    if works[index]['name']=='sortmedicaments':
        z=random.randint(3600,7200)
    if works[index]['name']=='pickberrys':
        z=random.randint(7200,9200)
    if works[index]['name']=='bringfoodtokitchen':
        z=random.randint(2200,3600)
    if works[index]['name']=='helpmedpunkt':
        z=random.randint(7200,10200)
    if works[index]['name']=='cleanterritory' or works[index]['name']=='washgenda':
        z=random.randint(900,2700)
    if z!=None:
        t=threading.Timer(z,reloadquest, args=[index])
        t.start()
    t=threading.Timer(300, endwork, args=[id, works[index]['name']])
    t.start()
    
       
           
def endwork(id, work):
    x=users.find_one({'id':id})
    users.update_one({'id':id},{'$set':{'working':0}})
    users.update_one({'id':id},{'$set':{'relaxing':1}})
    srtenght=0
    agility=0
    intelligence=0
    if x['gender']=='female':
        gndr='а'
    else:
        gndr=''
    text='Ты хорошо поработал'+gndr+'! А как известно - всё, что нас не убивает, делает нас сильнее. Улучшенные характеристики:\n'
    if work=='sortmedicaments':
        agility=random.randint(0,2)
        strenght=random.randint(1,100)
        if strenght<=15:
           strenght=1
        else:
           strenght=0
        intelligence=random.randint(1,100)
        if intelligence<=10:
            intelligence=1
        else:
            intelligence=0
    if work=='pickberrys':
        strenght=random.randint(0,2)
        agility=random.randint(1,100)
        if agility<=50:
            agility=random.randint(0,2)
        else:
            agility=0
    if work=='bringfoodtokitchen':
        strenght=random.randint(1,2)
        agility=random.randint(1,100)
        if agility<=30:
            agility=random.randint(1,2)
        else:
            agility=0
    if work=='helpmedpunkt':
        intelligence=random.randint(1,2)
        strenght=random.randint(1,100)
        if strenght<=35:
            strenght=random.randint(1,2)
        else:
            strenght=0
        agility=random.randint(1,100)
        if agility<=5:
            agility=1
        else:
            agility=0
    if work=='cleanterritory' or work=='washgenda':
        strenght=random.randint(0,2)
        agility=random.randint(0,1)
    if work=='checkpionerssleeping':
        agility=random.randint(1,2)
        intelligence=random.randint(1,100)
        if intelligence<=40:
            intelligence=random.randint(0,2)
        else:
            intelligence=0
    if work=='helpinkitchen':
        agility=random.randint(1,2)
        intelligence=1
        strenght=random.randint(0,1)
    if agility>0:
        text+='*Ловкость*\n'
    if strenght>0:
        text+='*Сила*\n'
    if intelligence>0:
        text+='*Интеллект*\n'
    if text=='':
        text='Физических улучшений не заметно, но ты заслужил'+gndr+' уважение вожатой!'
    users.update_one({'id':id},{'$inc':{'strenght':strenght}})
    users.update_one({'id':id},{'$inc':{'agility':agility}})
    users.update_one({'id':id},{'$inc':{'intelligence':intelligence}})
    bot.send_message(-1001351496983, 'Отличная работа, ['+x['pionername']+'](tg://user?id='+str(id)+')! Теперь можешь отдохнуть.', parse_mode='markdown')
    try:
        world.send_message(id, text,parse_mode='markdown')
    except:
        world.send_message(-1001351496983, '['+x['pionername']+'](tg://user?id='+str(id)+')'+random.choice(worldtexts)+text, parse_mode='markdown')
    t=threading.Timer(6,relax,args=[id])
    t.start()
    

worldtexts=[', чтобы знать, что происходит в лагере (в том числе и с вами), советую отписаться мне в личку. Можете считать меня своим внутренним голосом, потому что забивать себе голову тем, кто я на самом деле, не имеет смысла... Но а теперь к делу.\n\n',
           ', отпишись, пожалуйста, мне в личку. Ведь правильнее будет, если твоя личная информация будет оставаться при тебе, а не оглашаться на весь лагерь. Ладно, ближе к делу...\n\n']
    
    

  
           
           
def relax(id):
    users.update_one({'id':id},{'$set':{'relaxing':0}})
    
    
    
def createuser(id, name, username):
    return{'id':id,
           'name':name,
           'username':username,
           'pionername':None,
           'gender':None,
           'popularity':1,
           'strenght':3,
           'agility':3,
           'intelligence':3,
           'prepareto':None,           
           'setname':1,
           'setgender':1,
           'waitforwork':0,
           'respect':50,
           'working':0,
           'relaxing':0,
           'answering':0,
           'busy':[],
           'OlgaDmitrievna_respect':50,
           'Slavya_respect':50,
           'Uliana_respect':50,
           'Alisa_respect':50,
           'Lena_respect':50,
           'Electronic_respect':50,
           'Miku_respect':50,
           'Zhenya_respect':50,
           'helping':0
           
          }
    
    
def gettime(t):
   x=time.ctime()
   x=x.split(" ")
   for ids in x:
      for idss in ids:
         if idss==':':
            tru=ids
   x=tru
   x=x.split(":")
   minute=int(x[1])
   hour=int(x[0])+3
   if t=='h':
     return hour
   elif t=='m':
     return minute
            
def checktime():
    t=threading.Timer(60, checktime)
    t.start()
    hour=gettime('h')
    minute=gettime('m')
    if hour==17 and minute==0:
        x=findindex('concertready')
        works[x]['value']=0
    if hour==21 and minute==30:
        x=findindex('checkpionerssleeping')
        works[x]['value']=0
    if (hour==8 and minute==10) or(hour==13 and minute==0) or(hour==20 and minute==30):
        x=findindex('helpinkitchen')
        works[x]['value']=0
    if(hour==19 and minute==0):
        cardplayers=[]
        eveninggames()
    if(hour==7 and minute==0):
        bot.send_chat_action(-1001351496983,'typing')
        time.sleep(3)
        bot.send_message(-1001351496983, 'Доброе утро, пионеры! В 7:30 жду всех на линейке!')
    if(hour==7 and minute==30):
        odstats['waitforlineyka']=0
        bot.send_chat_action(-1001351496983,'typing')
        time.sleep(3)
        bot.send_message(-1001351496983, 'Здраствуйте, пионеры! Сейчас проведём перекличку...')
        bot.send_chat_action(-1001351496983,'typing')
        time.sleep(4)
        text=''
        for ids in odstats['lineyka']:
            text+=ids+'\n'
        bot.send_message(-1001351496983,text+'\nВот все, кто сегодня пришёл. Молодцы, пионеры! Так держать!'+\
                         'Сейчас расскажу о планах на день.',parse_mode='markdown')
            
        
    
def eveninggames():
    egames=['cards','football']#,'ropepulling']
    x=random.choice(egames)
    if x=='cards':
        leader='electronic'
        bot.send_chat_action(-1001351496983,'typing')
        t=threading.Timer(3.5, sendmes, args=[bot, 'Уже 7 вечера, а это значит, что пора начинать наши вечерние игры! На сегодня '+\
                         'у нас по плану придуманная Электроником карточная игра. [Электроник](https://t.me/ES_ElectronicBot), '+\
                         'дальше расскажешь ты.', 'markdown'])
        t.start()
        time.sleep(4.5)
        electronic.send_chat_action(-1001351496983,'typing')
        t=threading.Timer(2, sendmes, args=[electronic, 'Есть, Ольга Дмитриевна!', None])
        t.start()
        t=threading.Timer(2.1, sendstick, args=[electronic, 'CAADAgAD1QADgi0zDyFh2eUTYDzzAg'])
        t.start()
        time.sleep(4)
        electronic.send_chat_action(-1001351496983,'typing') 
        t=threading.Timer(10, sendmes, args=[electronic, 'Итак. Правила игры просты: надо выиграть, собрав на руке более сильную '+\
                                            'комбинацию, чем у соперника. Процесс игры заключается в том, что соперники поочереди '+\
                                            'забирают друг у друга карты. Делается это так: в свой ход вы выбираете одну из карт соперника, '+\
                                            'а он после этого может поменять любые 2 карты в своей руке местами. Вы эту перестановку '+\
                                            'видите, и после его действия можете изменить свой выбор. А можете не менять. '+\
                                            'Так повторяется 3 раза, и вы забираете последнюю карту, которую выберите. Затем '+\
                                            'такой же ход повторяется со стороны соперника. Всего каждый участник делает 3 хода, '+\
                                            'и после этого оба игрока вскрываются...', None])
        t.start()
        time.sleep(4)
        electronic.send_chat_action(-1001351496983,'typing') 
        time.sleep(4)
        electronic.send_chat_action(-1001351496983,'typing') 
        time.sleep(4)
        electronic.send_chat_action(-1001351496983,'typing') 
        t=threading.Timer(5, sendmes, args=[electronic, 'Что смешного? Ладно, неважно. Все поняли правила? Отлично! Для '+\
                                              'регистрации в турнире нужно подойти ко мне, и сказать: "`Хочу принять участие в турнире!`". '+\
                                              'Регистрация заканчивается через 20 минут!', 'markdown'])
        t.start()
        electronicstats['waitingplayers']=1
        t=threading.Timer(1200, starttournier, args=['cards'])
        t.start()

    elif x=='football':
        leader='uliana'
        bot.send_chat_action(-1001351496983,'typing')
        t=threading.Timer(3.5, sendmes, args=[bot, 'Уже 7 вечера, а это значит, что пора начинать наши вечерние игры! На сегодня '+\
                         'у нас по плану футбол! [Ульяна](https://t.me/ES_ElectronicBot), '+\
                         'расскажет вам про правила проведения турнира.', 'markdown'])
        t.start()
        time.sleep(4.5)
        uliana.send_chat_action(-1001351496983,'typing')
        t=threading.Timer(2, sendmes, args=[uliana, 'Так точно, Ольга Дмитриевна!', None])
        t.start()
        t=threading.Timer(2.1, sendstick, args=[uliana, 'CAADAgADKQADgi0zD_inNy0pZyh0Ag'])
        t.start()
        time.sleep(4)
        uliana.send_chat_action(-1001351496983,'typing') 
        t=threading.Timer(10, sendmes, args=[uliana, 'Правила просты - не жульничать! Для записи на турнир '+\
                                             'подойдите ко мне и скажите "`Хочу участвовать!`". Вроде бы всё... Жду всех!', 'markdown'])
        t.start()
        time.sleep(4)
        uliana.send_chat_action(-1001351496983,'typing') 
        time.sleep(4)
        uliana.send_chat_action(-1001351496983,'typing') 
        time.sleep(4)
        uliana.send_chat_action(-1001351496983,'typing') 
    elif x=='ropepulling':
        leader='alisa'
 
setka=[]

def starttournier(game):
    if game=='cards':
        global cardplayers
        global setka
        newplayers=['miku','slavya','zhenya','alisa','lena','uliana']
        specialrules=0
        i=0
        for ids in cardplayers:
            i+=1
        if i%2==0:
            if i>=10:
                prm=16
            elif i>0:
                prm=8
            else:
                prm=0
        else:
            if i==1:
                prm=4
            elif i==3 or i==5 or i==7:
                prm=8
            elif i==9:
                prm=12
                specialrules=1
        g=0
        if prm>0:
          while g<(prm-i):
            randomplayer=random.choice(newplayers)
            cardplayers.append(randomplayer)
            newplayers.remove(randomplayer)
            g+=1
          text=''
          i=0
          h=len(cardplayers)
          while i<(h/2):
            player1=random.choice(cardplayers)
            cardplayers.remove(player1)
            player2=random.choice(cardplayers)
            cardplayers.remove(player2)
            setka.append([player1, player2])
            i+=1
          for ids in setka:
            text+='\n\n'
            vs=' VS '
            for idss in ids:
                try:
                    int(idss)
                    x=users.find_one({'id':idss})
                    text+='['+x['pionername']+'](tg://user?id='+str(x['id'])+')'+vs
                except:
                    text+=nametopioner(idss)+vs
                vs=''
          electronic.send_chat_action(-1001351496983,'typing') 
          time.sleep(5)
          electronic.send_message(-1001351496983, 'Ну что, все в сборе? Тогда вот вам турнирная сетка на первый этап:\n'+text, parse_mode='markdown')
          time.sleep(1.5)
          electronic.send_chat_action(-1001351496983,'typing')
          time.sleep(3)
          electronic.send_message(-1001351496983, 'А теперь прошу к столам! Каждый садится со своим соперником. Через 2 минуты начинается '+
                                'первый этап!')
          electronicstats['cardsturn']=1
          t=threading.Timer(120, cards_nextturn)
          t.start()
          for ids in setka:
            i=0
            for idss in ids:
                try:
                    int(idss)
                    i+=1
                except:
                    if i==0:
                        index=1
                    elif i==1:
                        index=0
                    try:
                        int(ids[index])
                        talkwithplayer(ids[index], idss)
                    except:
                        pass
        else:
           electronic.send_message(-1001351496983,'К сожалению, игроков для турнира сегодня не набралось. Ну ничего, в следующий раз попробуем!')
   



def cards_nextturn():
  global setka
  global cardplayers
  for ab in setka:
      cardplayers.append(ab[0])
      cardplayers.append(ab[1])
  if len(cardplayers)>0:
    print(setka)
    print(cardplayers)
    for ids in setka:
        i=-1
        print(ids)
        for idss in ids:
            print(idss)
            i+=1
            if i<2:
              try:
                print('try1')
                int(ids[0])
                if i==0:
                    index=1
                else:
                    index=0
                try:
                    print('try2')
                    int(ids[index])
                    player1=users.find_one({'id':ids[0]})
                    player2=users.find_one({'id':ids[1]})
                    r=player1['intelligence']-player2['intelligence']
                    r=r/2
                    x=random.randint(1,100)
                    if x<=(50+r):
                        cardplayers.remove(player2['id'])
                    else:
                        cardplayers.remove(player1['id'])
                    i=10
                    print('try2complete')
                
                except:
                    if ids[index]=='miku':
                        intelligence=mikustats['intelligence']
                    if ids[index]=='alisa':
                        intelligence=alisastats['intelligence']
                    if ids[index]=='lena':
                        intelligence=lenastats['intelligence']
                    if ids[index]=='slavya':
                        intelligence=slavyastats['intelligence']
                    if ids[index]=='zhenya':
                        intelligence=zhenyastats['intelligence']
                    if ids[index]=='uliana':
                        intelligence=ulianastats['intelligence']
                    if intelligence==1:
                        x=80
                    if intelligence==2:
                        x=60
                    if intelligence==3:
                        x=40
                    if intelligence==4:
                        x=20
                    if random.randint(1,100)<=x:
                        cardplayers.remove(ids[1])
                    else:
                        cardplayers.remove(ids[0])
                    i=10
              
              except:
                try:
                    print('try3')
                    int(ids[1])
                    index=0
                    if ids[index]=='miku':
                        intelligence=mikustats['intelligence']
                    if ids[index]=='alisa':
                        intelligence=alisastats['intelligence']
                    if ids[index]=='lena':
                        intelligence=lenastats['intelligence']
                    if ids[index]=='slavya':
                        intelligence=slavyastats['intelligence']
                    if ids[index]=='zhenya':
                        intelligence=zhenyastats['intelligence']
                    if ids[index]=='uliana':
                        intelligence=ulianastats['intelligence']
                    if intelligence==1:
                        x=80
                    if intelligence==2:
                        x=60
                    if intelligence==3:
                        x=40
                    if intelligence==4:
                        x=20
                    if random.randint(1,100)<=x:
                        cardplayers.remove(ids[0])
                    else:
                        cardplayers.remove(ids[1])
                    i=10
                
                except:
                    print('try4')
                    if ids[0]=='miku':
                        intelligence1=mikustats['intelligence']
                    if ids[0]=='alisa':
                        intelligence1=alisastats['intelligence']
                    if ids[0]=='lena':
                        intelligence1=lenastats['intelligence']
                    if ids[0]=='slavya':
                        intelligence1=slavyastats['intelligence']
                    if ids[0]=='zhenya':
                        intelligence1=zhenyastats['intelligence']
                    if ids[0]=='uliana':
                        intelligence1=ulianastats['intelligence']
                    if ids[1]=='miku':
                        intelligence2=mikustats['intelligence']
                    if ids[1]=='alisa':
                        intelligence2=alisastats['intelligence']
                    if ids[1]=='lena':
                        intelligence2=lenastats['intelligence']
                    if ids[1]=='slavya':
                        intelligence2=slavyastats['intelligence']
                    if ids[1]=='zhenya':
                        intelligence2=zhenyastats['intelligence']
                    if ids[1]=='uliana':
                        intelligence2=ulianastats['intelligence']
                    z=intelligence1-intelligence2
                    if z==0:
                        x=50
                    elif z==1:
                        x=60
                    elif z==2:
                        x=75
                    elif z==3:
                        x=85
                    elif z==-1:
                      x=40
                    elif z==-2:
                      x=25
                    elif z==-3:
                      x=15
                    if random.randint(1,100)<=x:
                        cardplayers.remove(ids[1])
                    else:
                        cardplayers.remove(ids[0])
                    i=10
    text=''
    x=0
    for dd in cardplayers:
        x+=1
        try:
            int(dd)
            text+=users.find_one({'id':dd})['pionername']+'\n'
        except:
            text+=nametopioner(dd)+'\n'
    text1=''
    text3=''
    if electronicstats['cardsturn']==1:
        text1='Завершился первый этап турнира! А вот и наши победители:\n\n'
    elif electronicstats['cardsturn']==2:
        if x>1:
            text1='Второй этап турнира подошёл к концу! Встречайте победителей:\n\n'
        else:
            text1='Финал подошёл к концу! И наш победитель:\n\n'
    elif electronicstats['cardsturn']==3:
      if x==2:
        text1='Полуфинал завершён! В финале встретятся:\n\n'
      else:
        text1='Встречайте победителя турнира:\n\n'
    elif electronicstats['cardsturn']==4:
        text1='Турнир завершён! И наш победитель:\n\n'
    if x==2:
        text3='Настало время для финала! Кто же станет победителем на этот раз?'
    elif x==4:
        text3='На очереди у нас полуфинал. Кто же из четырёх оставшихся игроков попадёт в финал?'
    elif x==8:
        text3='Скоро начнётся раунд 2. Игроки, приготовьтесь!'
    electronicstats['cardsturn']+=1
    electronic.send_message(-1001351496983,text1+text+'\n'+text3, parse_mode='markdown')
    setka=[]
    i=0
    if len(cardplayers)>1:
        x=len(cardplayers)/2
        while i<x:
            player1=random.choice(cardplayers)
            cardplayers.remove(player1)
            player2=random.choice(cardplayers)
            cardplayers.remove(player2)
            lst=[player1, player2]
            setka.append(lst)
            i+=1
        t=threading.Timer(120, cards_nextturn)
        t.start()
    else:
        time.sleep(2)
        bot.send_chat_action(-1001351496983,'typing') 
        time.sleep(5)
        try:
            name=users.find_one({'id':cardplayers[0]})['pionername']
        except:
            name=nametopioner(cardplayers[0])
        bot.send_message(-1001351496983, 'Отлично! Поздравляю, '+name+'! А теперь приберитесь тут, скоро ужин.', parse_mode='markdown')
        bot.send_sticker(-1001351496983, 'CAADAgADqwADgi0zDzm_zSmMbMmiAg')
        setka=[]
        cardplayers=[]
        electronicstats['waitingplayers']=0
        electronicstats['playingcards']=0
        electronicstats['cardsturn']=0
  else:
      electronic.send_message(-1001351496983,'К сожалению, игроков для турнира сегодня не набралось. Ну ничего, в следующий раз попробуем!')
      setka=[]
      cardplayers=[]
      electronicstats['waitingplayers']=0
      electronicstats['playingcards']=0
      electronicstats['cardsturn']=0
                
    


                
def talkwithplayer(player, pioner):
    if pioner=='miku':
        t=threading.Timer(random.randint(10,90), sayto, args=[miku, 'miku', player, cards_startround_mikutexts])
        t.start()    
    if pioner=='alisa':
        t=threading.Timer(random.randint(10,90), sayto, args=[alisa, 'alisa', player, cards_startround_alisatexts])
        t.start()    
    if pioner=='zhenya':
        t=threading.Timer(random.randint(10,90), sayto, args=[zhenya, 'zhenya', player, cards_startround_zhenyatexts])
        t.start()    
    if pioner=='uliana':
        t=threading.Timer(random.randint(10,90), sayto, args=[uliana, 'uliana', player, cards_startround_ulianatexts])
        t.start()    
    if pioner=='slavya':
        t=threading.Timer(random.randint(10,90), sayto, args=[slavya, 'slavya', player, cards_startround_slavyatexts])
        t.start()    
    if pioner=='lena':
        t=threading.Timer(random.randint(10,90), sayto, args=[lena, 'lena', player, cards_startround_lenatexts])
        t.start()    


        
cards_startround_mikutexts=['Ой, Привет! Если не помнишь, то меня Мику зовут. Мы сейчас с тобой '+\
                              'играем! Ты хорошо играешь? Я не очень...','Привет! Мы с тобой уже знакомы, если помнишь... '+\
                              'Удачи на турнире!']   
cards_startround_alisatexts=['Ну привет. Готовься проиграть!']
cards_startround_slavyatexts=['Привет! Интересно, кто победит в турнире в этот раз...']
cards_startround_ulianatexts=['Привет-привет! Я сегодня настроена на победу, так что советую сразу сдаться!']
cards_startround_lenatexts=['Привет. Удачи на сегодняшнем турнире!']
cards_startround_zhenyatexts=['Выходит, мы с тобой сегодня играем. Давай сразу к игре, без лишних разговоров!']
    
    

def sayto(pioner, pionername, id, texts):
    x=users.find_one({'id':id})
    if x['gender']=='female':
        gndr='а'
    else:
        gndr=''
    if pionername=='miku':
        textstochat=['Привет, '+x['pionername']+'! Меня Мику зовут! Мы ещё не знакомы, можем '+\
                            '[поговорить](https://t.me/ES_MikuBot) после турнира... А сейчас - удачи!']
    elif pionername=='alisa':
        textstochat=['Ну привет, '+x['pionername']+'! Думаешь победить в турнире? Даже не надейся! Меня тебе '+\
                            'точно не обыграть!']
    elif pionername=='slavya':
        textstochat=['Привет, '+x['pionername']+'! Чего-то я тебя не видела раньше... Меня Славя зовут! Можем '+\
                            '[познакомиться](https://t.me/SlavyaBot) на досуге. Ну а сейчас готовься к игре!']
    elif pionername=='uliana':
        textstochat=['Привет! Тебя ведь '+x['pionername']+' зовут? Я Ульяна! Готов'+gndr+' проиграть?']
        
    elif pionername=='lena':
        textstochat=['Привет, '+x['pionername']+'. Меня Лена зовут... Хотя ты наверняка уже знаешь, ведь в турнирной сетке написано. '+\
                    'Удачи!']
        
    elif pionername=='zhenya':
        textstochat=['Ну привет, '+x['pionername']+'. Не знаю, зачем я вообще играю, но уже поздно передумывать.']
                            
    try:
        pioner.send_chat_action(id,'typing')
        time.sleep(5)
        pioner.send_message(id, random.choice(texts))
    except:
        pioner.send_chat_action(-1001351496983,'typing')
        time.sleep(5)
        pioner.send_message(-1001351496983, random.choice(textstochat), parse_mode='markdown')
        
        

def nametopioner(pioner):
    if pioner=='miku':
        return '[Мику](https://t.me/ES_MikuBot)'
    if pioner=='alisa':
        return '[Алиса](https://t.me/ES_AlisaBot)'
    if pioner=='zhenya':
        return '[Женя](https://t.me/ES_ZhenyaBot)'
    if pioner=='uliana':
        return '[Ульяна](https://t.me/ES_UlianaBot)'
    if pioner=='slavya':
        return '[Славя](https://t.me/SlavyaBot)'
    if pioner=='lena':
        return '[Лена](https://t.me/ES_LenaBot)'
    if pioner=='electronic':
        return '[Электроник](https://t.me/ES_ElectronicBot)'

def addtogame(name,game):
    game.append(name)
                
                
def sendmes(sender, text, parse_mode):
    sender.send_message(-1001351496983,text, parse_mode=parse_mode)

def sendstick(sender, stick):
    sender.send_sticker(-1001351496983,stick)
           
      

####################################### ELECTRONIC ##############################################
@electronic.message_handler(commands=['control'])
def electroniccontrol(m):
    if m.from_user.id in botadmins or m.from_user.id in el_admins:
        if electronicstats['controller']==None:
            electronicstats['controller']={'id':m.from_user.id,
                                     'name':m.from_user.first_name}
            electronic.send_message(m.from_user.id, 'Привет! надеюсь ты знаешь, как управлять мной.')
        else:
            electronic.send_message(m.from_user.id, 'Мной уже управляет '+electronicstats['controller']['name']+'!')
            
@electronic.message_handler(commands=['stopcontrol'])
def electronicstopcontrol(m):
    if electronicstats['controller']!=None:
        if electronicstats['controller']['id']==m.from_user.id:
            electronicstats['controller']=None
            electronic.send_message(m.from_user.id, 'Ты больше не управляешь мной!')
            
                      
                      
@electronic.message_handler(content_types=['sticker'])
def stickercatchelectronic(m):  
    if electronicstats['controller']!=None:
        controller=electronicstats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                electronic.send_sticker(-1001351496983, m.sticker.file_id)


@electronic.message_handler()
def electronichandler(m):
    if electronicstats['waitingplayers']==1:
        if m.text.lower()=='хочу принять участие в турнире!':
            x=users.find_one({'id':m.from_user.id})
            if x['gender']=='female':
                gndr='а'
            else:
                gndr=''
            if x['id'] not in cardplayers:
                if m.from_user.id==m.chat.id:
                    texts=['Привет! Записал тебя в список участников. Жди начала турнира!',
                                  'Хорошо. Записал тебя!',
                                  'Рад, что тебя заинтересовала моя игра. Теперь ты тоже в списке участников!']
                    text=random.choice(texts)
                    electronic.send_message(m.chat.id, text)
                    cardplayers.append(x['id'])
                else:
                    if m.reply_to_message!=None:
                        if m.reply_to_message.from_user.id==609648686:
                            texts=['Привет, ['+x['pionername']+'](tg://user?id='+str(x['id'])+')! Записал тебя в список участников. Жди начала турнира!',
                                  'Хорошо, ['+x['pionername']+'](tg://user?id='+str(x['id'])+'). Записал тебя!',
                                  'Рад, что тебя заинтересовала моя игра. Теперь ты тоже в списке участников!']
                            text=random.choice(texts)
                            electronic.send_message(m.chat.id, text, parse_mode='markdown', reply_to_message_id=m.message_id)
                            cardplayers.append(x['id'])
            else:
                if m.from_user.id==m.chat.id:
                    reply_to_message_id=None
                else:
                    reply_to_message_id=m.message_id
                electronic.send_message(m.chat.id, '['+x['pionername']+'](tg://user?id='+str(x['id'])+\
                                        '), ты уже записан'+gndr+' на турнир!', parse_mode='markdown', reply_to_message_id=reply_to_message_id)
        else:
            if m.from_user.id==m.chat.id:
                reply_to_message_id=None
            else:
                reply_to_message_id=m.message_id
            electronic.send_message(m.chat.id, 'Привет, ['+x['pionername']+'](tg://user?id='+str(x['id'])+')! А я тут '+\
                                    'собираю участников для вечернего турнира. Не хочешь принять участие?', parse_mode='markdown', reply_to_message_id=reply_to_message_id)

    if electronicstats['controller']!=None:
        controller=electronicstats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                if m.text.split(' ')[0]!='/pm' and m.text.split(' ')[0]!='/r':
                    msg=electronic.send_message(-1001351496983, m.text)
                    for ids in ctrls:
                        if ids['controller']!=None and ids['bot']!=electronic:
                            if m.chat.id==-1001351496983:
                                x='(Общий чат)'
                            else:
                                x='(ЛС)'
                            try:
                                ids['bot'].send_message(ids['controller']['id'], x+'\n'+msg.from_user.first_name+' (`'+str(msg.from_user.id)+'`) (❓'+str(msg.message_id)+'⏹):\n'+msg.text, parse_mode='markdown')
                            except Exception as E:
                                bot.send_message(441399484, traceback.format_exc())   
                elif m.text.split(' ')[0]=='/pm':
                    try:
                        text=m.text.split(' ')
                        t=''
                        i=0
                        for ids in text:
                            if i>1:
                                t+=ids+' '
                            i+=1
                        electronic.send_message(int(m.text.split(' ')[1]), t)
                    except:
                        electronic.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')

            else:
                try:
                    i=0
                    cid=None
                    eid=None
                    for ids in m.reply_to_message.text:
                        print(ids)
                        if ids=='❓':
                            cid=i+1
                        if ids=='⏹':
                            eid=i
                        i+=1
                    print('cid')
                    print(cid)
                    print('eid')
                    print(eid)
                    msgid=m.reply_to_message.text[cid:eid]
                    electronic.send_message(-1001351496983, m.text, reply_to_message_id=int(msgid))
                    
                except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                    electronic.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')
                    
                                          
        
        else:
            if m.chat.id==-1001351496983:
                x='(Общий чат)'
            else:
                x='(ЛС)'
            try:
                electronic.send_message(controller['id'], x+'\n'+m.from_user.first_name+' (`'+str(m.from_user.id)+'`) (❓'+str(m.message_id)+'⏹):\n'+m.text, parse_mode='markdown')
           
            except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())                  
                      
                      
                      
                      
@lena.message_handler(commands=['control'])
def lenacontrol(m):
    if m.from_user.id in botadmins or m.from_user.id in le_admins:
        if lenastats['controller']==None:
            lenastats['controller']={'id':m.from_user.id,
                                     'name':m.from_user.first_name}
            lena.send_message(m.from_user.id, 'Теперь ты управляешь мной! Я буду присылать тебе все сообщения, которые вижу!')
        else:
            lena.send_message(m.from_user.id, 'Мной уже управляет '+lenastats['controller']['name']+'!')
            
@lena.message_handler(commands=['stopcontrol'])
def lenastopcontrol(m):
    if lenastats['controller']!=None:
        if lenastats['controller']['id']==m.from_user.id:
            lenastats['controller']=None
            lena.send_message(m.from_user.id, 'Ты больше не управляешь мной!')
            
@lena.message_handler()
def lenamessages(m):
    print('1')
    yes=['да!','конечно!','да','да, могу.','могу','могу.','конечно могу!','да']
    if lenastats['whohelps']!=None:
        print('2')
        y=0
        if m.from_user.id==lenastats['whohelps']:
          print('3')
          for ids in yes:
              if ids in m.text.lower():
                  y=1
          if y==1:
            pioner=users.find_one({'id':m.from_user.id})
            print('4')
            try:
                lenastats['timer'].cancel()
            except:
                pass
            allhelps=['Спасибо! Тогда пошли, мне нужно отсортировать лекарства в медпункте.', 'Спасибо! Пойдём, надо разобрать склад и принести несколько комплектов пионерской формы для Слави.']
            lenastats['whohelps']=None
            helpp=random.choice(allhelps)
            lena.send_chat_action(m.chat.id,'typing')
            time.sleep(4)
            lena.send_message(m.chat.id, helpp)
            sendstick(lena,'CAADAgADZwADgi0zD-vRcG90IHeAAg')
            t=threading.Timer(300,helpend,args=[m.from_user.id])
            t.start()
            users.update_one({'id':m.from_user.id},{'$set':{'helping':1}})
    if lenastats['controller']!=None:
        controller=lenastats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                if m.text.split(' ')[0]!='/pm' and m.text.split(' ')[0]!='/r':
                    msg=lena.send_message(-1001351496983, m.text)
                    for ids in ctrls:
                        if ids['controller']!=None and ids['bot']!=lena:
                            if m.chat.id==-1001351496983:
                                x='(Общий чат)'
                            else:
                                x='(ЛС)'
                            try:
                                ids['bot'].send_message(ids['controller']['id'], x+'\n'+msg.from_user.first_name+' (`'+str(msg.from_user.id)+'`) (❓'+str(msg.message_id)+'⏹):\n'+msg.text, parse_mode='markdown')
                            except Exception as E:
                                bot.send_message(441399484, traceback.format_exc())   
                elif m.text.split(' ')[0]=='/pm':
                    try:
                        text=m.text.split(' ')
                        t=''
                        i=0
                        for ids in text:
                            if i>1:
                                t+=ids+' '
                            i+=1
                        lena.send_message(int(m.text.split(' ')[1]), t)
                    except:
                        lena.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')
                        
                elif m.text.split(' ')[0]=='/r':
                    try:
                        text=m.text.split(' ')
                        t=''
                        i=0
                        for ids in text:
                            if i>1:
                                t+=ids+' '
                            i+=1
                        lena.send_message(-1001351496983, t, reply_to_message_id=int(m.text.split(' ')[1]))
                    except:
                        lena.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')
            else:
                try:
                    i=0
                    cid=None
                    eid=None
                    for ids in m.reply_to_message.text:
                        print(ids)
                        if ids=='❓':
                            cid=i+1
                        if ids=='⏹':
                            eid=i
                        i+=1
                    print('cid')
                    print(cid)
                    print('eid')
                    print(eid)
                    msgid=m.reply_to_message.text[cid:eid]
                    lena.send_message(-1001351496983, m.text, reply_to_message_id=int(msgid))
                    
                except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                    lena.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')
                    
                                          
        
        else:
            if m.chat.id==-1001351496983:
                x='(Общий чат)'
            else:
                x='(ЛС)'
            try:
                lena.send_message(controller['id'], x+'\n'+m.from_user.first_name+' (`'+str(m.from_user.id)+'`) (❓'+str(m.message_id)+'⏹):\n'+m.text, parse_mode='markdown')
           
            except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                      
                      
@lena.message_handler(content_types=['sticker'])
def stickercatchlena(m):  
    if lenastats['controller']!=None:
        controller=lenastats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                lena.send_sticker(-1001351496983, m.sticker.file_id)
           
           
           
           
####################################### ALICE ##############################################
@alisa.message_handler(commands=['control'])
def alisacontrol(m):
    if m.from_user.id in botadmins or m.from_user.id in al_admins:
        if alisastats['controller']==None:
            alisastats['controller']={'id':m.from_user.id,
                                     'name':m.from_user.first_name}
            alisa.send_message(m.from_user.id, 'Ну ты вроде теперь мной управляешь. Я буду присылать тебе все сообщения, которые вижу, но если мне что-то не понравится - буду злиться!')
        else:
            alisa.send_message(m.from_user.id, 'Мной уже управляет '+alisastats['controller']['name']+'!')
            
@alisa.message_handler(commands=['stopcontrol'])
def alisastopcontrol(m):
    if alisastats['controller']!=None:
        if alisastats['controller']['id']==m.from_user.id:
            alisastats['controller']=None
            alisa.send_message(m.from_user.id, 'Ты больше не управляешь мной!')
            
@alisa.message_handler()
def alisamessages(m):
    
    if alisastats['controller']!=None:
        controller=alisastats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                if m.text.split(' ')[0]!='/pm' and m.text.split(' ')[0]!='/r':
                    msg=alisa.send_message(-1001351496983, m.text)
                    for ids in ctrls:
                        if ids['controller']!=None and ids['bot']!=alisa:
                            if m.chat.id==-1001351496983:
                                x='(Общий чат)'
                            else:
                                x='(ЛС)'
                            try:
                                ids['bot'].send_message(ids['controller']['id'], x+'\n'+msg.from_user.first_name+' (`'+str(msg.from_user.id)+'`) (❓'+str(msg.message_id)+'⏹):\n'+msg.text, parse_mode='markdown')
                            except Exception as E:
                                bot.send_message(441399484, traceback.format_exc())   
                elif m.text.split(' ')[0]=='/pm':
                    try:
                        text=m.text.split(' ')
                        t=''
                        i=0
                        for ids in text:
                            if i>1:
                                t+=ids+' '
                            i+=1
                        alisa.send_message(int(m.text.split(' ')[1]), t)
                    except:
                        alisa.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')

            else:
                try:
                    i=0
                    cid=None
                    eid=None
                    for ids in m.reply_to_message.text:
                        print(ids)
                        if ids=='❓':
                            cid=i+1
                        if ids=='⏹':
                            eid=i
                        i+=1
                    print('cid')
                    print(cid)
                    print('eid')
                    print(eid)
                    msgid=m.reply_to_message.text[cid:eid]
                    alisa.send_message(-1001351496983, m.text, reply_to_message_id=int(msgid))
                    
                except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                    alisa.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')
                    
                                          
        
        else:
            if m.chat.id==-1001351496983:
                x='(Общий чат)'
            else:
                x='(ЛС)'
            try:
                alisa.send_message(controller['id'], x+'\n'+m.from_user.first_name+' (`'+str(m.from_user.id)+'`) (❓'+str(m.message_id)+'⏹):\n'+m.text, parse_mode='markdown')
           
            except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                      
                      
@alisa.message_handler(content_types=['sticker'])
def stickercatchalisa(m):  
    if alisastats['controller']!=None:
        controller=alisastats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                alisa.send_sticker(-1001351496983, m.sticker.file_id)
           
           
           
           
####################################### ULIANA ##############################################
@uliana.message_handler(commands=['control'])
def ulianaacontrol(m):
    if m.from_user.id in botadmins or m.from_user.id in ul_admins:
        if ulianastats['controller']==None:
            ulianastats['controller']={'id':m.from_user.id,
                                     'name':m.from_user.first_name}
            uliana.send_message(m.from_user.id, 'Привет! Теперь ты мной управляешь, прикольно!')
        else:
            uliana.send_message(m.from_user.id, 'Мной уже управляет '+ulianastats['controller']['name']+'!')
            
@uliana.message_handler(commands=['stopcontrol'])
def ulianastopcontrol(m):
    if ulianastats['controller']!=None:
        if ulianastats['controller']['id']==m.from_user.id:
            ulianastats['controller']=None
            uliana.send_message(m.from_user.id, 'Ты больше не управляешь мной!')
            
@uliana.message_handler()
def ulianamessages(m):
    print('uliana')
    if ulianastats['controller']!=None:
        controller=ulianastats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                if m.text.split(' ')[0]!='/pm' and m.text.split(' ')[0]!='/r':
                    msg=uliana.send_message(-1001351496983, m.text)
                    for ids in ctrls:
                        if ids['controller']!=None and ids['bot']!=uliana:
                            if m.chat.id==-1001351496983:
                                x='(Общий чат)'
                            else:
                                x='(ЛС)'
                            try:
                                ids['bot'].send_message(ids['controller']['id'], x+'\n'+msg.from_user.first_name+' (`'+str(msg.from_user.id)+'`) (❓'+str(msg.message_id)+'⏹):\n'+msg.text, parse_mode='markdown')
                            except Exception as E:
                                bot.send_message(441399484, traceback.format_exc())   
                elif m.text.split(' ')[0]=='/pm':
                    try:
                        text=m.text.split(' ')
                        t=''
                        i=0
                        for ids in text:
                            if i>1:
                                t+=ids+' '
                            i+=1
                        uliana.send_message(int(m.text.split(' ')[1]), t)
                    except:
                        uliana.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')

            else:
                try:
                    i=0
                    cid=None
                    eid=None
                    for ids in m.reply_to_message.text:
                        print(ids)
                        if ids=='❓':
                            cid=i+1
                        if ids=='⏹':
                            eid=i
                        i+=1
                    print('cid')
                    print(cid)
                    print('eid')
                    print(eid)
                    msgid=m.reply_to_message.text[cid:eid]
                    uliana.send_message(-1001351496983, m.text, reply_to_message_id=int(msgid))
                    
                except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                    uliana.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')
                    
                                          
        
        else:
            if m.chat.id==-1001351496983:
                x='(Общий чат)'
            else:
                x='(ЛС)'
            try:
                uliana.send_message(controller['id'], x+'\n'+m.from_user.first_name+' (`'+str(m.from_user.id)+'`) (❓'+str(m.message_id)+'⏹):\n'+m.text, parse_mode='markdown')
           
            except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                      
                      
@uliana.message_handler(content_types=['sticker'])
def stickercatchalisa(m):  
    if ulianastats['controller']!=None:
        controller=ulianastats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                uliana.send_sticker(-1001351496983, m.sticker.file_id)
           
           
           
           
####################################### SLAVYA ##############################################
@slavya.message_handler(commands=['control'])
def slavyacontrol(m):
    if m.from_user.id in botadmins or m.from_user.id in sl_admins:
        if slavyastats['controller']==None:
            slavyastats['controller']={'id':m.from_user.id,
                                     'name':m.from_user.first_name}
            slavya.send_message(m.from_user.id, 'Привет! Теперь ты мной управляешь! Только аккуратнее!')
        else:
            slavya.send_message(m.from_user.id, 'Мной уже управляет '+slavyastats['controller']['name']+'!')
            
@slavya.message_handler(commands=['stopcontrol'])
def slavyastopcontrol(m):
    if slavyastats['controller']!=None:
        if slavyastats['controller']['id']==m.from_user.id:
            slavyastats['controller']=None
            slavya.send_message(m.from_user.id, 'Ты больше не управляешь мной!')
            
@slavya.message_handler()
def slavyamessages(m):
    
    if slavyastats['controller']!=None:
        controller=slavyastats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                if m.text.split(' ')[0]!='/pm' and m.text.split(' ')[0]!='/r':
                    msg=slavya.send_message(-1001351496983, m.text)
                    for ids in ctrls:
                        if ids['controller']!=None and ids['bot']!=slavya:
                            if m.chat.id==-1001351496983:
                                x='(Общий чат)'
                            else:
                                x='(ЛС)'
                            try:
                                ids['bot'].send_message(ids['controller']['id'], x+'\n'+msg.from_user.first_name+' (`'+str(msg.from_user.id)+'`) (❓'+str(msg.message_id)+'⏹):\n'+msg.text, parse_mode='markdown')
                            except Exception as E:
                                bot.send_message(441399484, traceback.format_exc())   
                elif m.text.split(' ')[0]=='/pm':
                    try:
                        text=m.text.split(' ')
                        t=''
                        i=0
                        for ids in text:
                            if i>1:
                                t+=ids+' '
                            i+=1
                        slavya.send_message(int(m.text.split(' ')[1]), t)
                    except:
                        slavya.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')

            else:
                try:
                    i=0
                    cid=None
                    eid=None
                    for ids in m.reply_to_message.text:
                        print(ids)
                        if ids=='❓':
                            cid=i+1
                        if ids=='⏹':
                            eid=i
                        i+=1
                    print('cid')
                    print(cid)
                    print('eid')
                    print(eid)
                    msgid=m.reply_to_message.text[cid:eid]
                    slavya.send_message(-1001351496983, m.text, reply_to_message_id=int(msgid))
                    
                except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                    slavya.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')
                    
                                          
        
        else:
            if m.chat.id==-1001351496983:
                x='(Общий чат)'
            else:
                x='(ЛС)'
            try:
                slavya.send_message(controller['id'], x+'\n'+m.from_user.first_name+' (`'+str(m.from_user.id)+'`) (❓'+str(m.message_id)+'⏹):\n'+m.text, parse_mode='markdown')
           
            except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                      
                      
@slavya.message_handler(content_types=['sticker'])
def stickercatchslavya(m):  
    if slavyastats['controller']!=None:
        controller=slavyastats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                slavya.send_sticker(-1001351496983, m.sticker.file_id)
           
           
           
           
           
####################################### MIKU ##############################################
@miku.message_handler(commands=['control'])
def mikucontrol(m):
    if m.from_user.id in botadmins or m.from_user.id in mi_admins:
        if mikustats['controller']==None:
            mikustats['controller']={'id':m.from_user.id,
                                     'name':m.from_user.first_name}
            miku.send_message(m.from_user.id, 'Привет! Теперь ты управляешь мной, как здорово! Ой, а я однажды в школе пыталась управлять музыкальным клубом, но ничего не вышло... Надеюсь, у тебя получится лучше!')
        else:
            miku.send_message(m.from_user.id, 'Мной уже управляет '+slavyastats['controller']['name']+'!')
            
@miku.message_handler(commands=['stopcontrol'])
def mikustopcontrol(m):
    if mikustats['controller']!=None:
        if mikustats['controller']['id']==m.from_user.id:
            mikustats['controller']=None
            miku.send_message(m.from_user.id, 'Ты больше не управляешь мной!')
            
@miku.message_handler()
def mikumessages(m):
    
    if mikustats['controller']!=None:
        controller=mikustats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                if m.text.split(' ')[0]!='/pm' and m.text.split(' ')[0]!='/r':
                    msg=miku.send_message(-1001351496983, m.text)
                    for ids in ctrls:
                        if ids['controller']!=None and ids['bot']!=miku:
                            if m.chat.id==-1001351496983:
                                x='(Общий чат)'
                            else:
                                x='(ЛС)'
                            try:
                                ids['bot'].send_message(ids['controller']['id'], x+'\n'+msg.from_user.first_name+' (`'+str(msg.from_user.id)+'`) (❓'+str(msg.message_id)+'⏹):\n'+msg.text, parse_mode='markdown')
                            except Exception as E:
                                bot.send_message(441399484, traceback.format_exc())   
                elif m.text.split(' ')[0]=='/pm':
                    try:
                        text=m.text.split(' ')
                        t=''
                        i=0
                        for ids in text:
                            if i>1:
                                t+=ids+' '
                            i+=1
                        miku.send_message(int(m.text.split(' ')[1]), t)
                    except:
                        miku.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')

            else:
                try:
                    i=0
                    cid=None
                    eid=None
                    for ids in m.reply_to_message.text:
                        print(ids)
                        if ids=='❓':
                            cid=i+1
                        if ids=='⏹':
                            eid=i
                        i+=1
                    print('cid')
                    print(cid)
                    print('eid')
                    print(eid)
                    msgid=m.reply_to_message.text[cid:eid]
                    miku.send_message(-1001351496983, m.text, reply_to_message_id=int(msgid))
                    
                except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                    miku.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')
                    
                                          
        
        else:
            if m.chat.id==-1001351496983:
                x='(Общий чат)'
            else:
                x='(ЛС)'
            try:
                miku.send_message(controller['id'], x+'\n'+m.from_user.first_name+' (`'+str(m.from_user.id)+'`) (❓'+str(m.message_id)+'⏹):\n'+m.text, parse_mode='markdown')
           
            except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                      
                      
@miku.message_handler(content_types=['sticker'])
def stickercatchmiku(m):  
    if mikustats['controller']!=None:
        controller=mikustats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                miku.send_sticker(-1001351496983, m.sticker.file_id)
                
                
                
                
                
           
####################################### ZHENYA ##############################################
@zhenya.message_handler(commands=['control'])
def zhenyacontrol(m):
    if m.from_user.id in botadmins or m.from_user.id in zh_admins:
        if zhenyastats['controller']==None:
            zhenyastats['controller']={'id':m.from_user.id,
                                     'name':m.from_user.first_name}
            zhenya.send_message(m.from_user.id, 'Привет, ты теперь управляешь мной... А я пока пойду почитаю.')
        else:
            zhenya.send_message(m.from_user.id, 'Мной уже управляет '+zhenyastats['controller']['name']+'!')
            
@zhenya.message_handler(commands=['stopcontrol'])
def zhenyastopcontrol(m):
    if zhenyastats['controller']!=None:
        if zhenyastats['controller']['id']==m.from_user.id:
            zhenyastats['controller']=None
            zhenya.send_message(m.from_user.id, 'Ты больше не управляешь мной!')
            
@zhenya.message_handler()
def zhenyamessages(m):
    
    if zhenyastats['controller']!=None:
        controller=zhenyastats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                if m.text.split(' ')[0]!='/pm' and m.text.split(' ')[0]!='/r':
                    msg=zhenya.send_message(-1001351496983, m.text)
                    for ids in ctrls:
                        if ids['controller']!=None and ids['bot']!=zhenya:
                            if m.chat.id==-1001351496983:
                                x='(Общий чат)'
                            else:
                                x='(ЛС)'
                            try:
                                ids['bot'].send_message(ids['controller']['id'], x+'\n'+msg.from_user.first_name+' (`'+str(msg.from_user.id)+'`) (❓'+str(msg.message_id)+'⏹):\n'+msg.text, parse_mode='markdown')
                            except Exception as E:
                                bot.send_message(441399484, traceback.format_exc())   
                elif m.text.split(' ')[0]=='/pm':
                    try:
                        text=m.text.split(' ')
                        t=''
                        i=0
                        for ids in text:
                            if i>1:
                                t+=ids+' '
                            i+=1
                        zhenya.send_message(int(m.text.split(' ')[1]), t)
                    except:
                        zhenya.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')

            else:
                try:
                    i=0
                    cid=None
                    eid=None
                    for ids in m.reply_to_message.text:
                        print(ids)
                        if ids=='❓':
                            cid=i+1
                        if ids=='⏹':
                            eid=i
                        i+=1
                    print('cid')
                    print(cid)
                    print('eid')
                    print(eid)
                    msgid=m.reply_to_message.text[cid:eid]
                    zhenya.send_message(-1001351496983, m.text, reply_to_message_id=int(msgid))
                    
                except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                    zhenya.send_message(m.from_user.id, 'Что-то пошло не так. Возможны следующие варианты:\n'+
                                          '1. Неправильный формат отправки сообщения в ЛС юзера (пример: _/pm 441399484 Привет!_)\n'+
                                          '2. Юзер не написал этому пионеру/пионерке в ЛС.\nМожно реплайнуть на сообщение от меня, и я реплайну на оригинальное сообщение в чате!', parse_mode='markdown')
                    
                                          
        
        else:
            if m.chat.id==-1001351496983:
                x='(Общий чат)'
            else:
                x='(ЛС)'
            try:
                zhenya.send_message(controller['id'], x+'\n'+m.from_user.first_name+' (`'+str(m.from_user.id)+'`) (❓'+str(m.message_id)+'⏹):\n'+m.text, parse_mode='markdown')
           
            except Exception as E:
                    bot.send_message(441399484, traceback.format_exc())
                      
                      
@zhenya.message_handler(content_types=['sticker'])
def stickercatchzhenya(m):  
    if zhenyastats['controller']!=None:
        controller=zhenyastats['controller']
        if m.chat.id==controller['id']:
            if m.reply_to_message==None:
                zhenya.send_sticker(-1001351496983, m.sticker.file_id)




           
        
def helpend(id):
    x=users.find_one({'id':id})
    users.update_one({'id':id},{'$set':{'helping':0}})
    lena.send_chat_action(id,'typing')
    time.sleep(4)
    lena.send_message(-1001351496983, 'Спасибо за помощь, ['+x['pionername']+'](tg://user?id='+str(x['id'])+')! '+\
                     'Без тебя ушло бы гораздо больше времени. Ну, я пойду...',parse_mode='markdown')
    


            
cardplayers=[]
        
        
alisastats={
    'strenght':1,
    'agility':2,
    'intelligence':3,
    'controller':None,
    'bot':alisa
}
lenastats={
    'strenght':2,
    'agility':2,
    'intelligence':2,
    'whohelps':None,
    'timer':None,
    'controller':None,
    'bot':lena
}
mikustats={
    'strenght':2,
    'agility':2,
    'intelligence':2,
    'controller':None,
    'bot':miku
}
ulianastats={
    'strenght':1,
    'agility':4,
    'intelligence':1,
    'controller':None,
    'bot':uliana
}
slavyastats={
    'strenght':1,
    'agility':1,
    'intelligence':4,
    'controller':None,
    'bot':slavya
}
electronicstats={
    'strenght':3,
    'agility':1,
    'intelligence':4,
    'waitingplayers':0,
    'playingcards':0,
    'cardsturn':0,
    'controller':None,
    'bot':electronic
           
}
zhenyastats={
    'strenght':2,
    'agility':1,
    'intelligence':3,
    'controller':None,
    'bot':zhenya
           
}

odstats={
    'lineyka':[],
    'waitforlineyka':0,
    'controller':None,
    'bot':bot
}


ctrls=[]
ctrls.append(odstats)
ctrls.append(electronicstats)
ctrls.append(slavyastats)
ctrls.append(zhenyastats)
ctrls.append(ulianastats)
ctrls.append(mikustats)
ctrls.append(lenastats)
ctrls.append(alisastats)


zavtrak='9:00'
obed='14:00'
uzhin='21:00'
            
def findindex(x):
    i=0
    for ids in works:
            if ids['name']==x:
                index=i
            i+=1
    return index
            
 
def randomhelp():
   t=threading.Timer(random.randint(7200,17000),randomhelp)
   t.start()
   spisok=[]
   pioners=['lena']
   x=users.find({})
   for ids in x:
       spisok.append(ids)
   if len(spisok)>0:
       pioner=random.choice(spisok)
       z=random.choice(pioners)
       if z=='lena':
           helpto(pioner,'lena')

def helpto(pioner,x):
    if pioner['gender']=='male':
        g=''
    else:
        g='ла'
    if x=='lena':
        try:
            lena.send_chat_action(-1001351496983,'typing')
            time.sleep(4)
            m=lena.send_message(-1001351496983,'['+pioner['pionername']+'](tg://user?id='+str(pioner['id'])+'), привет. Не мог'+g+' бы ты мне помочь?', parse_mode='markdown')
            lenastats['whohelps']=pioner['id']
            t=threading.Timer(300,helpcancel,args=['lena',m])
            t.start()
            lenastats['timer']=t
            sendstick(lena,'CAADAgADaQADgi0zD9ZBO-mNcLuBAg')
        except:
            pass
            
        
def helpcancel(pioner,m):
    if pioner=='lena':
        lenastats['whohelps']=None
        lena.send_chat_action(-1001351496983,'typing')
        time.sleep(4)
        lena.send_message(-1001351496983,'Ты, наверное, сейчас занят... Прости, что побеспокоила.',reply_to_message_id=m.message_id)
        
    
    

def randomact():
    t=threading.Timer(random.randint(4900,18000),randomact)
    t.start()
    lisst=['talk_uliana+olgadmitrievna','talk_uliana+alisa']
    x=random.choice(lisst)
    if x=='talk_uliana+olgadmitrievna':
        bot.send_chat_action(-1001351496983,'typing')
        time.sleep(4)
        bot.send_message(-1001351496983,nametopioner('uliana')+', а ну стой! Ты эти конфеты где взяла?', parse_mode='markdown')
        sendstick(bot,'CAADAgADtwADgi0zD-9trZ_s35yQAg')
        time.sleep(1)
        uliana.send_chat_action(-1001351496983,'typing')
        time.sleep(2)
        uliana.send_message(-1001351496983, 'Какие конфеты?')
        sendstick(uliana,'CAADAgADHQADgi0zD1aFI93sTseZAg')
        time.sleep(2)
        bot.send_chat_action(-1001351496983,'typing')
        time.sleep(3)
        bot.send_message(-1001351496983,'Те, что ты за спиной держишь! Быстро верни их в столовую!')
        time.sleep(1)
        uliana.send_chat_action(-1001351496983,'typing')
        time.sleep(2)
        uliana.send_message(-1001351496983, 'Хорошо, Ольга Дмитриевна...')
        sendstick(uliana,'CAADAgADJQADgi0zD1PW7dDuU5hCAg')
    if x=='talk_uliana+alisa':
        alisa.send_chat_action(-1001351496983,'typing')
        time.sleep(3)
        alisa.send_message(-1001351496983,nametopioner('uliana')+', не боишься, что Ольга Дмитриевна спалит?', parse_mode='markdown')
        time.sleep(1)
        uliana.send_chat_action(-1001351496983,'typing')
        time.sleep(2)
        uliana.send_message(-1001351496983, 'Ты о чём?')
        time.sleep(2)
        alisa.send_chat_action(-1001351496983,'typing')
        time.sleep(2)
        alisa.send_message(-1001351496983,'О конфетах, которые ты украла!')
        sendstick(alisa,'CAADAgADOwADgi0zDzD8ZNZXu5LHAg')
        time.sleep(1)
        uliana.send_chat_action(-1001351496983,'typing')
        time.sleep(2)
        uliana.send_message(-1001351496983, 'Да не, не спалит! Я так уже много раз делала!')
        sendstick(uliana,'CAADAgADKQADgi0zD_inNy0pZyh0Ag')
        time.sleep(2)
        alisa.send_chat_action(-1001351496983,'typing')
        time.sleep(2)
        alisa.send_message(-1001351496983,'Тогда делись!')
        time.sleep(1)
        uliana.send_chat_action(-1001351496983,'typing')
        time.sleep(2)
        uliana.send_message(-1001351496983, 'Тогда пошли в домик!')


        
        
        
if True:
    checktime()
                   
if True:
    randomhelp()


def polling(pollingbot):
    pollingbot.polling(none_stop=True,timeout=600)


if True:
    randomact()
    
if True:
   print('7777')
   users.update_many({},{'$set':{'working':0}})
   users.update_many({},{'$set':{'waitforwork':0}})
   users.update_many({},{'$set':{'relaxing':0}})
   t=threading.Timer(1, polling, args=[uliana])
   t.start()
   uliana.send_message(441399484, 'Я могу принимать сообщения!')
   t=threading.Timer(1, polling, args=[bot])
   t.start()
   t=threading.Timer(1, polling, args=[lena])
   t.start()
   t=threading.Timer(1, polling, args=[electronic])
   t.start()
   t=threading.Timer(1, polling, args=[zhenya])
   t.start()
   t=threading.Timer(1, polling, args=[alisa])
   t.start()
   t=threading.Timer(1, polling, args=[slavya])
   t.start()
   t=threading.Timer(1, polling, args=[miku])
   t.start()
   t=threading.Timer(1, polling, args=[shurik])
   t.start()
   bot.send_message(-1001351496983, 'Все пионеры в норме!')
   

