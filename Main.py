import LocalStorage
import eShopPage
import Polish
from ChartWidget import PriceChart

from math import floor

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

class GameDataWidgetSingleton():
    def __init__(self):
        self.instance: QtWidgets

    def Load(self):
        self.instance = GameData()

gameDataWidget = GameDataWidgetSingleton()



class GameData(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setContentsMargins(0,45,0,10)

        self.image = GameImage()

        self.chart = PriceChart()

        self.lowestPrice = LowestPrice("---,-- R$")
        self.averagePrice = AveragePrice("---,-- R$")

        self.setMinimumWidth(250)

        self.priceWidgets = QtWidgets.QWidget(self)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.priceLayout = QtWidgets.QHBoxLayout()

        self.layout.addWidget(self.image)
        self.layout.addLayout(self.priceLayout)
        self.priceLayout.addWidget(self.lowestPrice)
        self.priceLayout.addWidget(self.averagePrice)
        self.layout.addWidget(self.chart.chartView)

class SmallDescriptionLabel(QtWidgets.QLabel):
    def __init__(self, text: str, size: int):
        super().__init__()

        self.setContentsMargins(0,0,0,0)
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignCenter)

        self.font = QtGui.QFont()
        self.font.setItalic(True)
        self.font.setPixelSize(size)

        self.setFont(self.font)

class LowestPrice(QtWidgets.QWidget):
    def __init__(self, lowestPriceNow):
        super().__init__()
        self.lowestPriceNow = lowestPriceNow

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)

        self.layout.addStretch(1)

        self.lowestPriceDesc = SmallDescriptionLabel("Price now:", 12)
        self.layout.addWidget(self.lowestPriceDesc)

        self.priceLabel = LowestPriceValueLabel(self.lowestPriceNow)
        self.layout.addWidget(self.priceLabel)

        self.country = SmallDescriptionLabel("n/a", 10)
        self.layout.addWidget(self.country)

        self.layout.addStretch(1)

class AveragePrice(QtWidgets.QWidget):
    def __init__(self, averagePrice):
        super().__init__()
        self.averagePrice = averagePrice

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)

        self.layout.addStretch(1)

        self.averagePriceDesc = SmallDescriptionLabel("Average price:", 12)
        self.layout.addWidget(self.averagePriceDesc)

        self.priceLabel = AveragePriceValueLabel(self.averagePrice)
        self.layout.addWidget(self.priceLabel)

        self.layout.addStretch(1)

class LowestPriceValueLabel(QtWidgets.QLabel):
    def __init__(self, lowestPriceNow):
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.lowestPriceFont = QtGui.QFont()
        self.lowestPriceFont.setBold(True)
        self.lowestPriceFont.setPixelSize(38)

        self.setAlignment(QtCore.Qt.AlignHCenter)

        self.setText(f"{lowestPriceNow}")
        self.setFont(self.lowestPriceFont)

class AveragePriceValueLabel(QtWidgets.QLabel):
    def __init__(self, averagePriceNow):
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        self.averagePriceFont = QtGui.QFont()
        self.averagePriceFont.setBold(True)
        self.averagePriceFont.setItalic(True)
        self.averagePriceFont.setPixelSize(28)

        self.setAlignment(QtCore.Qt.AlignCenter)

        self.setText(f"{averagePriceNow}")
        self.setFont(self.averagePriceFont)

class GameImage(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.previewImage = QtGui.QPixmap("./ui/eshopIcon.jpg")
        self.setPixmap(self.previewImage)

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
        ThreadedFunction(wishlistWidget.instance.listTitlesWidget.LoadWishlistData)



class ListWidget(QtWidgets.QListWidget):
    def __init__(self, wishlist: bool):
        super().__init__()
        self.setAlternatingRowColors(True)

        self.latestSearch = ""
        self.setUniformItemSizes(True)
        self.setBatchSize(1000)

        self.currentItemChanged.connect(self.GameSelected)

        if wishlist:
            AddItemsToList(self, IdListToDict(wishlistGames, allGames))
            ThreadedFunction(self.LoadWishlistData)
        else:
            AddItemsToList(self, allGames)

    def LoadWishlistData(self):
        for i in range(self.count()):
            gameData = eShopPage.GetGameData(self.item(i).id,365)
            self.item(i).setBackground(QtGui.QBrush(QtGui.QColor(Polish.GetBackgroundColor(float(gameData['lowest price'].replace('R$','')), gameData['average price']))))
    
    def GameSelected(self, itemselected):
        if itemselected != None:
            ReplaceImage(gameDataWidget.instance.image, itemselected.id, False)
            gameData = eShopPage.GetGameData(itemselected.id,365)
            ReplacePriceData(gameDataWidget.instance, gameData)
            ReplaceChart(gameDataWidget.instance.chart, gameData)

def AddItemsToList(listWidg: QtWidgets.QListWidget, gameDictToShow):
    for id in gameDictToShow:
        itemlist = QtWidgets.QListWidgetItem()
        itemlist.id = id #doing this so i can get id on ListWidget
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

def ReplaceImage(imageWidget: QtWidgets.QLabel, id, tryhd=False):
    previewFilepath = LocalStorage.GetPreviewImage(id)
    previewImage = QtGui.QPixmap(previewFilepath)
    imageWidget.setPixmap(previewImage)

def ReplacePriceData(dataWidget: GameData, gameData):
    dataWidget.lowestPrice.priceLabel.setText(f"R$ {gameData['lowest price']}")
    dataWidget.lowestPrice.priceLabel.setStyleSheet(f"color: {Polish.GetTextColor(float(gameData['lowest price'].replace('R$','')), gameData['average price'])};")

    avgPrice = gameData["average price"]
    formattedAvgPrice = str(floor(avgPrice*100)/100).replace(".",",")
    dataWidget.averagePrice.priceLabel.setText(f"R$ {formattedAvgPrice}")

    dataWidget.lowestPrice.country.setText(gameData["country"])

def ReplaceChart(chartWidget: PriceChart, gameData):
    chartWidget.removeAllSeries()
    chartWidget.PaintChart(gameData["price history"])


def ThreadedFunction(function):
    dataThread = threading.Thread(target=function)
    dataThread.start()

def Main():
    app = QtWidgets.QApplication([])

    wishlistWidget.Load()
    gameDataWidget.Load()

    widget = MyWidgetH()
    widget.setObjectName("mainwindow")

    widget.setStyleSheet(" QWidget#mainwindow{ background-color: #ffeeea;} ")
    widget.setWindowTitle("eShop Wishlist")
    lists = LeftHalfWidget()
    widget.layout.addWidget(lists)
    widget.layout.addWidget(gameDataWidget.instance)
    widget.resize(1000, 600)
    widget.show()

    sys.exit(app.exec())




    #LoadWishlist(GetWishlist())



if __name__ == "__main__":
    Main()