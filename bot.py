# -*- coding: utf-8 -*-
import os
import telebot
import time
import chlenomerconfig
import telebot
import random

token = os.environ['TELEGRAM_TOKEN']


@bot.message_handler(content_types=['text'])
def chlenomer(message):
    print(message.chat.id)
    if message.text=='Член' or 'член' or 'хер' or 'Хер':
        randomvoice=random.randint(1,100)
        chlen=random.randint(1,100)
        mm=random.randint(0,9)
        randomvoice=random.randint(1,100)
        if randomvoice>90:
              chlen = random.randint(1, 2)
              if chlen == 1:
                  text = 'Как у коня'
              elif chlen==2:
                  text='5000км! Мужик!'
              bot.send_message(message.chat.id, 'Размер члена ' + message.from_user.first_name + ': ' + text)

        else:
            replytext='Размер члена '+message.from_user.first_name+': '+str(chlen)+','+str(mm)+' см'
            bot.send_message(message.chat.id, replytext)
    








if __name__ == '__main__':
  bot.polling(none_stop=True)
