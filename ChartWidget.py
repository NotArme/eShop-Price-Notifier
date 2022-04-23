from xmlrpc.client import DateTime
from PySide6 import QtGui, QtCharts, QtCore

from dateutil import parser
import datetime

class PriceChart(QtCharts.QChart):
    def __init__(self):
        super().__init__()

        self.priceHistory = None
        self.daysEvaluated = "---"
        self.priceSelected = "--.--"
        self.dateSelected = "--/--/----"

        self.createDefaultAxes()
        self.legend().hide()
        self.PaintChart(None)

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("#fff9fb")))
        self.setBackgroundPen(QtGui.QPen(QtGui.QColor("#f05555")))
        self.setMargins(QtCore.QMargins(5,5,5,5))

        #both of these doesnt seem to do anything in this theme, just keeping here for reference later
        #self.setPlotAreaBackgroundBrush(QtGui.QBrush(QtGui.QColor("#00fbff")))
        #self.setPlotAreaBackgroundPen(QtGui.QPen(QtGui.QColor("#00ff00")))


        #chartView is the widget that is actually added to layout, chart just represents data pretty much
        self.chartView = QtCharts.QChartView(self)

        self.chartView.mouseMoveEvent = self.mouseMove

        self.chartView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.chartView.setRubberBand(QtCharts.QChartView.RubberBand.HorizontalRubberBand)
        self.chartView.setStyleSheet(f"background-color: transparent;")

    def mouseMove(self, event):
        pos: QtCore.QPointF
        pos = self.mapToValue(event.position().toPoint())

        series : QtCharts.QLineSeries
        series = self.series

        xpos = round(pos.x())
        xpos = max(min(xpos, len(series.points()) - 1), 0)
        self.priceSelected = series.at(xpos).y()
        
        self.dateSelected = DateToString(DateFromPriceHistory(xpos, self.priceHistory))

        self.setTitle(f"R$ {self.priceSelected} ------ {self.dateSelected}")

    def PaintChart(self, priceHistory: list[dict]):
        self.series = QtCharts.QLineSeries()
        self.priceHistory = priceHistory

        if self.priceHistory == None:
            self.setTitle("Price history not found")
            return

        i = 0
        while i < len(self.priceHistory):
            self.series.append(i, self.priceHistory[len(self.priceHistory)-i-1]["value"]/100)
            i += 1

        self.addSeries(self.series)
        self.createDefaultAxes()
        self.setTitle(f"R$ {self.priceSelected}      {self.dateSelected}")

def DateFromPriceHistory(dateIndex, priceHistory):
    date = priceHistory[len(priceHistory) - dateIndex - 1]["date"]
    return date

def DateToString(receivedDate):
    if not isinstance(receivedDate, datetime.datetime):
        receivedDate = parser.parse(receivedDate)
    return receivedDate.date().strftime("%d/%m/%Y")