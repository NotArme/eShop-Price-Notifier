from PySide6 import QtGui, QtCharts, QtCore

class PriceChart(QtCharts.QChart):
    def __init__(self):
        super().__init__()

        self.createDefaultAxes()
        self.legend().hide()
        self.PaintChart(None)

        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor("#fff9fb")))
        self.setBackgroundPen(QtGui.QPen(QtGui.QColor("#f05555")))
        self.setMargins(QtCore.QMargins(0,0,0,0))

        #both of these doesnt seem to do anything in this theme, just keeping here for reference later
        #self.setPlotAreaBackgroundBrush(QtGui.QBrush(QtGui.QColor("#00fbff")))
        #self.setPlotAreaBackgroundPen(QtGui.QPen(QtGui.QColor("#00ff00")))


        #chartView is the widget that is actually added to layout, chart just represents data pretty much
        self.chartView = QtCharts.QChartView(self)

        #self.chartView.mouseMoveEvent will need this later for tooltip

        self.chartView.setRenderHint(QtGui.QPainter.Antialiasing)
        self.chartView.setRubberBand(QtCharts.QChartView.RubberBand.HorizontalRubberBand)
        self.chartView.setStyleSheet(f"background-color: transparent;")

    def PaintChart(self, priceHistory: list[dict]):
        self.series = QtCharts.QLineSeries()

        if priceHistory == None:
            self.setTitle("Price history not found")
            return

        i = 0
        while i < len(priceHistory):
            self.series.append(i, priceHistory[i]["value"]/100)
            i += 1

        self.addSeries(self.series)
        self.createDefaultAxes()
        self.setTitle("Price in the last x days")
