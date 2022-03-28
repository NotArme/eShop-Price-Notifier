import LocalStorage

import sys
from PySide6 import QtWidgets, QtCore, QtGui

searchBarHeight = 30

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
        self.layout.addWidget(SearchBarWidget())
        self.layout.addWidget(ListWidget())

class SearchBarWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMaximumHeight(searchBarHeight)
        
        self.setContentsMargins(0,0,0,0)
        self.layout = QtWidgets.QHBoxLayout(self)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.layout.addWidget(SearchBarTextField())
        self.layout.addWidget(SearchBarButton())

class SearchBarButton(QtWidgets.QPushButton):
    def __init__(self):
        super().__init__()
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
        

class SearchBarTextField(QtWidgets.QLineEdit):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(
            """QLineEdit{
                background-color: #ffeffc;
                border: none;
                border-top-left-radius: 5px;
                border-bottom-left-radius: 5px;
                }"""
        )

        self.setFixedHeight(searchBarHeight)
        self.setContentsMargins(0,0,0,0)


class GameItemOnList(QtWidgets.QWidget):
    def __init__(self, id, title):
        super().__init__()
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setContentsMargins(10,0,10,0)
        self.setMaximumSize(10000, 50)

        self.title = QtWidgets.QLabel(title)
        self.layout.addWidget(self.title)
        self.wishlistButton = QtWidgets.QPushButton("<3")
        self.wishlistButton.setFixedSize(20, 20)
        self.layout.addWidget(self.wishlistButton)

class ListWidget(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        self.setAlternatingRowColors(True)
        
        allGames =  LocalStorage.LoadGameList()

        for id in allGames:
            currentgamewidget = GameItemOnList(id, allGames[id])
            itemlist = QtWidgets.QListWidgetItem()
            itemlist.setSizeHint(QtCore.QSize(10, 25))
            self.addItem(itemlist)
            self.setItemWidget(itemlist, currentgamewidget)


def Main():
    app = QtWidgets.QApplication([])
    

    widget = MyWidgetH()
    widget.setWindowTitle("eShop Wishlist")
    widget.layout.addWidget(LeftHalfWidget())
    widget.layout.addWidget(MyWidgetV())
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())




    #LoadWishlist(GetWishlist())



if __name__ == "__main__":
    Main()