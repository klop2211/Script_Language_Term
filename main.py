from tkinter import *
import requests
import xml.etree.ElementTree as ET
import time
import urllib.request
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

# 구글 맵 API 키
MAP_API_KEY = "AIzaSyDldj_-4P3T4gKWdy6zqThReKArNFUXWAM"

class MainGUI():
    # 북마크 리스트 박스내의 아이템 더블클릭시 실행되는 함수
    def double_clickBookmark(self, event):
        # 선택된 지역에 대한 검색을 실행한다
        selected_item = self.bookmarkListbox.get(self.bookmarkListbox.curselection())
        print(f"You double-clicked: {selected_item}")

        # 이 함수의 인자로 위도, 경도 넣어주면 됌
        self.drawMap()

    # 검색 리스트 박스내의 아이템 더블클릭시 실행되는 함수
    def double_clickSearch(self, event):
        # 선택된 지역에 대한 검색을 실행한다
        selected_item = self.searchListbox.get(self.searchListbox.curselection())
        print(f"You double-clicked: {selected_item}")

        # 이 함수의 인자로 위도, 경도 넣어주면 됌
        self.drawMap()

    # 리스트 박스와 스크롤 바 길이 맞춤
    def configure_scrollbar(self, event):
        self.searchScrollbar.place_configure(height=event.height)
        self.bookmarkScrollbar.place_configure(height=event.height)

    # 검색 버튼이 눌렸을 때 작동하는 함수
    def commandSearch(self):
        # 지역검색이 이루어져야 하며 self.searchListbox.insert 함수로 리스트 박스를 채워야 한다
        pass

    # 위도, 경도를 받아 지도를 그려주는 함수
    def drawMap(self, latitude=37.541, longitude=126.986):
        size = "280x280"
        zoom = 15
        url = f"https://maps.googleapis.com/maps/api/staticmap?center={latitude},{longitude}&zoom={zoom}&size={size}&key={MAP_API_KEY}"
        urllib.request.urlretrieve(url, "map.png")
        map_image = PhotoImage(file="map.png")
        self.mapLabel.configure(image=map_image)
        self.mapLabel.image = map_image

    # UI 설정
    def setUI(self):

        # 검색 버튼과 검색창
        self.searchEntry = Entry(self.window, font=('arial', 30))
        self.searchButton = Button(self.window, text='검색', font=('arial', 20), command=self.commandSearch)
        self.searchEntry.place(x=0)
        self.searchButton.place(x=500)

        # 검색 결과창
        self.searchScrollbar = Scrollbar(self.window)
        self.searchScrollbar.place(x=200, y=50)

        self.searchListbox = Listbox(self.window, font=('arial', 15), width=12, height=7, yscrollcommand=self.searchScrollbar.set)
        self.searchListbox.place(x=50, y=50)
        self.searchListbox.bind('<Configure>', self.configure_scrollbar)
        self.searchListbox.bind("<Double-Button-1>", self.double_clickSearch)
        self.searchScrollbar.config(command=self.searchListbox.yview)

        # 리스트 박스 테스트 값
        for i in range(1, 21):
            self.searchListbox.insert(END, f"검색 {i}")

        # 북마크 목록
        self.bookmarkScrollbar = Scrollbar(self.window)
        self.bookmarkScrollbar.place(x=450, y=50)

        self.bookmarkListbox = Listbox(self.window, font=('arial', 15), width=12, height=7, yscrollcommand=self.bookmarkScrollbar.set)
        self.bookmarkListbox.place(x=300, y=50)
        self.bookmarkListbox.bind('<Configure>', self.configure_scrollbar)
        self.bookmarkListbox.bind("<Double-Button-1>", self.double_clickBookmark)

        self.bookmarkScrollbar.config(command=self.bookmarkListbox.yview)

        for i in range(1, 21):
            self.bookmarkListbox.insert(END, f"Item {i}")
        self.bookmarkButton = Button(self.window, text='즐겨찾기 추가')
        self.bookmarkButton.place(x=500, y=100)

        self.mapLabel = Label(self.window)
        self.mapLabel.place(x=20, y=250)


    def __init__(self):
        self.window = Tk()
        self.window.title("플라워타임")
        self.window.geometry("600x800")
        self.setUI()


        self.window.mainloop()

# aaaa
MainGUI()