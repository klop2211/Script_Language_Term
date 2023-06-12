#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback

import noti


def replyAptData(user, si, do, gun, what):
    search_data = noti.getData(si, do, gun, what)
    print(search_data)
    msg = ''
    msg = si + ' ' + do + ' ' + gun + '의 현재' + what + '꽃가루 현황은' + '\n' \
            + '오늘' + search_data[0] + ' 내일' + search_data[1]+ ' 모레' + search_data[2] + '입니다.'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '%s 기간에 해당하는 데이터가 없습니다.')

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('검색') and len(args) >= 5:
        replyAptData(chat_id, args[1], args[2], args[3], args[4])
    elif text.startswith('사용방법'):
        noti.sendMessage(chat_id, '검색 지역과 원하시는 꽃가루 종류를 입력해주세요.')
    else:
        noti.sendMessage(chat_id, '검색 내용을 확인 해 주세요.')


today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', noti.TOKEN )

bot = telepot.Bot(noti.TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)