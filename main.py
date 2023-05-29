from tkinter import *
import requests
import xml.etree.ElementTree as ET
import time
from urllib.request import Request, urlopen
from urllib import parse
from urllib.parse import urlencode, quote_plus

# 소나무, 참나무만 4~6 데이터를 제공
# 소나무
url = 'http://apis.data.go.kr/1360000/HealthWthrIdxServiceV3/getPinePollenRiskIdxV3'
service_key = "oWT9dq/7S6E11bbGOg2qY18HrHxLHQov6dy6WglV6AzFYqnOUC0YnQt/3GblAB1ygHHoWQpDuY0Wqc8grUD5oQ=="
now = time
now = now.strftime('%Y%m%d06') #2023052605 같은 형태로 전달해 줘야함
queryParams = {'serviceKey': service_key, 'pageNo': '1', 'numOfRows': '10', 'dataType': 'XML', 'areaNo': '', 'time': now}

response = requests.get(url, params=queryParams)
print(response.text)
root = ET.fromstring(response.text)

# 읽어올  값
for item in root.iter("item"):
    code = item.findtext("code") # 지수코드
    areaNo = item.findtext("areaNo") # 지점코드
    date = item.findtext("date") # 발표시간
    today = item.findtext("today") # 오늘 예측값
    tomorrow = item.findtext("tomorrow") # 내일 예측값
    dayaftertomorrow = item.findtext("dayaftertomorrow") # 모레 예측값
    todaysaftertomorrow = item.findtext("todaysaftertomorrow") # 글피 예측값

    data = [code, areaNo, date, today, tomorrow, dayaftertomorrow, todaysaftertomorrow]

class MainGUI():
    def setUI(self):
        frame = Frame(self.window)
        frame.pack()
        # 검색 버튼과 검색창
        self.searchEntry = Entry(frame, font = ('arial',30))
        self.searchButton = Button(frame, text='검색', font = ('arial',20))
        self.searchEntry.pack(side=LEFT)
        self.searchButton.pack(side=LEFT)

        # 검색 결과창
        frame = Frame(self.window)
        frame.pack()

        self.searchListbox = Listbox(frame)
        self.searchListbox.pack(side=LEFT, fill=Y)

        self.searchScrollbar = Scrollbar(frame, orient=VERTICAL)
        self.searchScrollbar.config(command=self.searchListbox.yview)
        self.searchScrollbar.pack(side=LEFT, fill=Y)

        self.searchListbox.config(yscrollcommand=self.searchScrollbar.set)
        for i in range(1, 21):
            self.searchListbox.insert(END, f"검색 {i}")

        # 북마크 목록

        self.bookmarkListbox = Listbox(frame)
        self.bookmarkListbox.pack(side=LEFT, fill=Y)

        self.bookmarkScrollbar = Scrollbar(frame, orient=VERTICAL)
        self.bookmarkScrollbar.pack(side=LEFT, fill=Y)
        self.bookmarkScrollbar.config(command=self.bookmarkListbox.yview)

        self.bookmarkListbox.config(yscrollcommand=self.bookmarkScrollbar.set)

        for i in range(1, 21):
            self.bookmarkListbox.insert(END, f"Item {i}")
        self.bookmarkButton = Button(frame, text='즐겨찾기 추가')
        self.bookmarkButton.pack(side=RIGHT)





    def __init__(self):
        self.window = Tk()
        self.window.title("플라워타임")
        self.window.geometry("600x800")
        self.setUI()


        self.window.mainloop()

# aaaa
MainGUI()