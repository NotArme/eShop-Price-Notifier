from asyncio.windows_events import NULL
from sqlite3 import connect
import LocalStorage
import threading

import sys
from PySide6 import QtWidgets, QtCore, QtGui

searchBarHeight = 30

allGames =  LocalStorage.LoadGameList()
wishlistGames =  LocalStorage.LoadWishlist()

class WishlistWidgetSingleton():
    def __init__(self):
        self.instance: GameListWidget

    def Load(self):
        self.instance = GameListWidget(wishlist=True)

wishlistWidget = WishlistWidgetSingleton()



class MyWidgetV(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

class MyWidgetH(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QtWidgets.QHBoxLayout(self)

class LeftHalfWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        allListWidget = GameListWidget()

        self.layout.addWidget(allListWidget)
        self.layout.addWidget(wishlistWidget.instance)

class GameListWidget(QtWidgets.QWidget):
    def __init__(self, wishlist=False):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)


        self.listTitlesWidget = ListWidget(wishlist)
        self.listSearchBarWidget = SearchBarWidget(self.listTitlesWidget)

        self.layout.addWidget(self.listSearchBarWidget)
        self.layout.addWidget(self.listTitlesWidget)

class SearchBarWidget(QtWidgets.QWidget):
    def __init__(self, associatedList):
        super().__init__()

        self.associatedList = associatedList
        self.latestSearchedTerm = ""

        self.setMaximumHeight(searchBarHeight)
        
        self.setContentsMargins(0,0,0,0)
        self.layout = QtWidgets.QHBoxLayout(self)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.textField = SearchBarTextField(self.associatedList)
        self.button = SearchBarButton(self.associatedList, self.textField)

        self.layout.addWidget(self.textField)
        self.layout.addWidget(self.button)

class SearchBarButton(QtWidgets.QPushButton):
    def __init__(self, associatedList: QtWidgets.QListWidget, textField: QtWidgets.QLineEdit):
        super().__init__()
        self.associatedList = associatedList
        self.textField = textField

        self.setFixedSize(searchBarHeight*1.5, searchBarHeight)
        self.setStyleSheet(
            """QPushButton { 
                background-color: #fed2d2;
                border: none;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                }"""
            "QPushButton:hover { background-color: #ffd6d6 }"
            "QPushButton:pressed { background-color: #fbc1c1 }"
        )
        self.setIcon(QtGui.QIcon("./ui/search-icon.svg"))
        self.setIconSize(QtCore.QSize(searchBarHeight*0.75, searchBarHeight*0.75))

        #Signals
        self.clicked.connect(self.SearchPressed)

    def SearchPressed(self):
        searchList = SearchGameList(allGames, self.textField.text(), self.associatedList)
        UpdateListItems(self.associatedList, searchList)
        
        

class SearchBarTextField(QtWidgets.QLineEdit):
    def __init__(self, associatedList: QtWidgets.QListWidget):
        super().__init__()
        self.associatedList = associatedList

        self.setStyleSheet(
            """QLineEdit{
                background-color: #fff9fe;
                border: none;
                border-top-left-radius: 5px;
                border-bottom-left-radius: 5px;
                }"""
        )

        self.setFixedHeight(searchBarHeight)
        self.setContentsMargins(0,0,0,0)

        #Signals
        self.returnPressed.connect(self.SearchPressed)

    def SearchPressed(self):
        searchList = SearchGameList(allGames, self.text(), self.associatedList)
        UpdateListItems(self.associatedList, searchList)


class GameItemOnList(QtWidgets.QWidget):
    def __init__(self, id, title: str):
        super().__init__()
        self.id = id
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(10,0,10,0)
        self.setMaximumSize(10000, 50)

        self.title = QtWidgets.QLabel(title.encode('latin1').decode('utf8'))
        self.layout.addWidget(self.title)
        self.wishlistButton = QtWidgets.QPushButton("<3")
        self.wishlistButton.clicked.connect(self.WishlistClicked)
        self.wishlistButton.setFixedSize(20, 20)
        self.layout.addWidget(self.wishlistButton)
    
    def WishlistClicked(self):
        ToggleWishlist(self.id)

class ListWidget(QtWidgets.QListWidget):
    def __init__(self, wishlist: bool):
        super().__init__()
        self.setAlternatingRowColors(True)

        self.latestSearch = ""
        self.setUniformItemSizes(True)
        self.setBatchSize(1000)

        if wishlist:
            AddItemsToList(self, IdListToDict(wishlistGames, allGames))
        else:
            AddItemsToList(self, allGames)

def AddItemsToList(listWidg: QtWidgets.QListWidget, gameDictToShow):
    for id in gameDictToShow:
        itemlist = QtWidgets.QListWidgetItem()
        itemlist.setSizeHint(QtCore.QSize(10, 25))
        currentgamewidget = GameItemOnList(id, gameDictToShow[id])
        listWidg.addItem(itemlist)
        listWidg.setItemWidget(itemlist, currentgamewidget)

def UpdateListItems(listWidget: QtWidgets.QListWidget, updatedList: list):
    
    if "dontUpdateSearch" in updatedList:
        return
    
    

    listWidget.setVisible(False)
    listWidget.setUpdatesEnabled(False)

    listWidget.clear()
    AddItemsToList(listWidget, updatedList)

    listWidget.setUpdatesEnabled(True)
    listWidget.setVisible(True)

def SearchGameList(gameList: dict, searchTerm: str, listWidget: ListWidget):
    searchResult = {}

    #cover cases where search is being called with the same search terms as last time
    if listWidget.latestSearch == searchTerm:
        searchResult["dontUpdateSearch"] = "true"
        return searchResult
    listWidget.latestSearch = searchTerm

    #if empty, just return the original full list
    if searchTerm == "":
        return allGames

    for key in gameList:
        if searchTerm.lower() in gameList[str(key)].lower():
            searchResult[str(key)] = gameList[str(key)]
    return searchResult

def ToggleWishlist(id):
    if id in wishlistGames:
        wishlistGames.remove(id)
        LocalStorage.CacheWishlist(wishlistGames)
        wishlistDict = IdListToDict(wishlistGames, allGames)
        UpdateListItems(wishlistWidget.instance.listTitlesWidget, wishlistDict)
    else:
        wishlistGames.append(id)
        LocalStorage.CacheWishlist(wishlistGames)
        wishlistDict = IdListToDict(wishlistGames, allGames)
        UpdateListItems(wishlistWidget.instance.listTitlesWidget, wishlistDict)

def IdListToDict(idlist, allgameslist):
    idName = {}
    for id in idlist:
        idName[id] = allgameslist[id]
    return idName

def Main():
    app = QtWidgets.QApplication([])

    wishlistWidget.Load()

    widget = MyWidgetH()
    widget.setObjectName("mainwindow")

    widget.setStyleSheet(" QWidget#mainwindow{ background-color: #ffeeea;} ")
    widget.setWindowTitle("eShop Wishlist")
    widget.layout.addWidget(LeftHalfWidget())
    widget.layout.addWidget(MyWidgetV())
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())




    #LoadWishlist(GetWishlist())



if __name__ == "__main__":
    Main()