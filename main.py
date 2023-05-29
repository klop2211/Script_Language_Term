import tkinter
from tkinter import *
import requests
import xml.etree.ElementTree as ET
import time
from openpyxl import load_workbook

# 소나무, 참나무만 4~6 데이터를 제공
# 소나무
url = 'http://apis.data.go.kr/1360000/HealthWthrIdxServiceV3/getPinePollenRiskIdxV3'
service_key = "oWT9dq/7S6E11bbGOg2qY18HrHxLHQov6dy6WglV6AzFYqnOUC0YnQt/3GblAB1ygHHoWQpDuY0Wqc8grUD5oQ=="
now = time
now = now.strftime('%Y%m%d%H') #2023052605 같은 형태로 전달해 줘야함\

# 인증키, 한 페이지 결과 수, 페이지 번호, 요청자료형식, 지점코드, 시간
# 06시를 주면 today가 나옴 06시가 아니면 글피 값이 나옴
queryParams = {'serviceKey': service_key, 'numOfRows': '3796', 'pageNo': '1', 'areaNo': '', 'time': 2023052906}

response = requests.get(url, params=queryParams)
# print(response.text)
root = ET.fromstring(response.text)

Pine_data = []
# 읽어올  값
for item in root.iter("item"):
    # code = item.findtext("code") # 지수코드
    areaNo = item.findtext("areaNo") # 지점코드
    date = item.findtext("date") # 발표시간
    today = item.findtext("today") # 오늘 예측값
    tomorrow = item.findtext("tomorrow") # 내일 예측값
    dayaftertomorrow = item.findtext("dayaftertomorrow") # 모레 예측값
    twodaysaftertomorrow = item.findtext("twodaysaftertomorrow") # 글피 예측값

    Pine_data = [areaNo, date, today, tomorrow, dayaftertomorrow, twodaysaftertomorrow]

class MainGUI():
    def setUI(self):
        frame = Frame(self.window)
        frame.pack()
        # 검색 버튼과 검색창
        self.searchEntry = Entry(frame, font = ('arial',30))
        self.searchButton = Button(frame, text='검색', font = ('arial',15), command=self.search)
        self.searchEntry.pack(side=LEFT)
        self.searchButton.pack(side=LEFT)
        data = []

        # 검색 결과창
        frame = Frame(self.window)
        frame.pack()

        self.searchListbox = Listbox(frame)
        self.searchListbox.pack(side=LEFT, fill=Y)
        self.searchListbox.bind('<<ListboxSelect>>', self.clickEvent) # 클릭 이벤트 위해 추가

        self.searchScrollbar = Scrollbar(frame, orient=VERTICAL)
        self.searchScrollbar.config(command=self.searchListbox.yview)
        self.searchScrollbar.pack(side=LEFT, fill=Y)

        self.searchListbox.config(yscrollcommand=self.searchScrollbar.set)
        workbook = load_workbook('지역별 지점코드(20230330).xlsx', data_only=True)
        sheet = workbook['최종 업데이트 파일_20230330']

        ck = True
        for row in sheet.iter_rows(values_only=True):
            if row[2] != None and row[3] != None and row[4] != None:
                t = row[2] + ' ' + row[3] + ' ' + row[4]
                data.append(t)
            if ck: # 맨 처음 데이터 버리기
                data.clear()
                ck = False

        workbook.close()

        for i in data:
            self.searchListbox.insert(END, f"{i}")

        # 북마크 목록

        self.bookmarkListbox = Listbox(frame)
        self.bookmarkListbox.pack(side=LEFT, fill=Y)

        self.bookmarkScrollbar = Scrollbar(frame, orient=VERTICAL)
        self.bookmarkScrollbar.pack(side=LEFT, fill=Y)
        self.bookmarkScrollbar.config(command=self.bookmarkListbox.yview)

        self.bookmarkListbox.config(yscrollcommand=self.bookmarkScrollbar.set)
        self.bookmarkButton = Button(frame, text='즐겨찾기 추가')
        self.bookmarkButton.pack(side=RIGHT)

    def search(self):
        word = self.searchEntry.get()
        print(word)
        workbook = load_workbook('지역별 지점코드(20230330).xlsx', data_only=True)
        sheet = workbook['최종 업데이트 파일_20230330']

        data = []
        ck = True
        for row in sheet.iter_rows(values_only=True):
            if row[2] != None and row[3] != None and row[4] != None:
                t = row[2] + ' ' + row[3] + ' ' + row[4]
                data.append(t)
            if ck: # 맨 처음 데이터 버리기
                data.clear()
                ck = False
        for row in sheet.iter_rows(values_only=True):
            if row[2] != None and row[3] != None and row[4] != None:
                t = row[2] + ' ' + row[3] + ' ' + row[4]
                if word == t:
                    Code = row[1]

        for item in root.iter("item"):
            # code = item.findtext("code") # 지수코드
            areaNo = item.findtext("areaNo")  # 지점코드
            date = item.findtext("date")  # 발표시간
            today = item.findtext("today")  # 오늘 예측값
            tomorrow = item.findtext("tomorrow")  # 내일 예측값
            dayaftertomorrow = item.findtext("dayaftertomorrow")  # 모레 예측값
            twodaysaftertomorrow = item.findtext("twodaysaftertomorrow")  # 글피 예측값

            fPine_data = [areaNo, date, today, tomorrow, dayaftertomorrow, twodaysaftertomorrow]
            if fPine_data[0] == Code:
                print("찾았다")
                self.bottomLabel = Label(self.window, anchor= "w", text= word + "의 현재 꽃가루 현황 : " + fPine_data[2] + " 내일 : " + fPine_data[3] + " 모레 : "+ fPine_data[4],\
                                         width= 150, font = 'arial')
                # self.bottomLabel.grid(row = 16, column= 0)
                self.bottomLabel.place(x = 50, y = 400)
                break

        workbook.close()

    def clickEvent(self, event):
        selected_item = self.searchListbox.get(self.searchListbox.curselection())
        workbook = load_workbook('지역별 지점코드(20230330).xlsx', data_only=True)
        sheet = workbook['최종 업데이트 파일_20230330']

        data = []
        ck = True
        for row in sheet.iter_rows(values_only=True):
            if row[2] != None and row[3] != None and row[4] != None:
                t = row[2] + ' ' + row[3] + ' ' + row[4]
                data.append(t)
            if ck: # 맨 처음 데이터 버리기
                data.clear()
                ck = False
        for row in sheet.iter_rows(values_only=True):
            if row[2] != None and row[3] != None and row[4] != None:
                t = row[2] + ' ' + row[3] + ' ' + row[4]
                if selected_item == t:
                    Code = row[1]

        for item in root.iter("item"):
            # code = item.findtext("code") # 지수코드
            areaNo = item.findtext("areaNo")  # 지점코드
            date = item.findtext("date")  # 발표시간
            today = item.findtext("today")  # 오늘 예측값
            tomorrow = item.findtext("tomorrow")  # 내일 예측값
            dayaftertomorrow = item.findtext("dayaftertomorrow")  # 모레 예측값
            twodaysaftertomorrow = item.findtext("twodaysaftertomorrow")  # 글피 예측값

            fPine_data = [areaNo, date, today, tomorrow, dayaftertomorrow, twodaysaftertomorrow]
            if fPine_data[0] == Code:
                print("찾았다")
                self.bottomLabel = Label(self.window, anchor= "w", text= selected_item + "의 현재 꽃가루 현황 : " + fPine_data[2] + " 내일 : " + fPine_data[3] + " 모레 : "+ fPine_data[4],\
                                         width= 150, font = 'arial')
                # self.bottomLabel.grid(row = 16, column= 0)
                self.bottomLabel.place(x = 50, y = 400)
                break



    def __init__(self):
        self.window = Tk()
        self.window.title("플라워타임")
        self.window.geometry("600x800")
        self.setUI()

        self.window.mainloop()

# aaaa
MainGUI()