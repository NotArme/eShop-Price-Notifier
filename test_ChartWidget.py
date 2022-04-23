from datetime import datetime
import unittest
import ChartWidget

gameData = {
    "average price": 31.449965156794423,
    "country": "South Africa",
    "game": "ACA NEOGEO OVER TOP",
    "lowest price": "29.29",
    "price history": [
        {
            "date": "2021-04-25 00:01:25.499000+00:00",
            "value": 3488
        },
        {
            "date": "2021-04-24 00:01:07.707000+00:00",
            "value": 3490
        },
        {
            "date": "2021-04-22T00:01:11.454Z",
            "value": 3555
        },
        {
            "date": "2021-04-20T00:01:22.943Z",
            "value": 3550
        }
    ]
}
class TestDateParsing(unittest.TestCase):
    def testDateFromPriceHistory(self):
        testtime = datetime.now()
        print("todo")

    def testDateToString(self):
        print("todo")