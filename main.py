from tkinter import *

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
        self.window.title("에취")
        self.window.geometry("600x800")
        self.setUI()


        self.window.mainloop()

# aaaa
MainGUI()