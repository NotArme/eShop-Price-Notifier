import unittest
import Utils

class TestColorConversion(unittest.TestCase):
    def testRgbToHex(self):
        rgb1 = [0, 53, 134]
        rgb2 = [34, 33, 234]
        rgb3 = [255, 255, 255]

        expHex1 = "#003586"
        expHex2 = "#2221ea"
        expHex3 = "#ffffff"

        result1 = Utils.RgbToHex(rgb1)
        result2 = Utils.RgbToHex(rgb2)
        result3 = Utils.RgbToHex(rgb3)

        self.assertEqual(expHex1, result1)
        self.assertEqual(expHex2, result2)
        self.assertEqual(expHex3, result3)

    def testHexToRgb(self):
        hex1 = "#003586"
        hex2 = "#2221ea"
        hex3 = "#ffffff"

        expRgb1 = [0, 53, 134]
        expRgb2 = [34, 33, 234]
        expRgb3 = [255, 255, 255]

        result1 = Utils.HexToRgb(hex1)
        result2 = Utils.HexToRgb(hex2)
        result3 = Utils.HexToRgb(hex3)

        self.assertEqual(expRgb1, result1)
        self.assertEqual(expRgb2, result2)
        self.assertEqual(expRgb3, result3)


class TestLerps(unittest.TestCase):
    def testLerpSingleValue(self):
        a = 0
        b = 10

        self.assertEqual(Utils._lerpSingleVal(a,b, 0), 0)
        self.assertEqual(Utils._lerpSingleVal(a,b, 0.5), 5)
        self.assertEqual(Utils._lerpSingleVal(a,b, 0.78), 7.8)
        self.assertEqual(Utils._lerpSingleVal(a,b, 1), 10)

    def testSomeLerps(self):
        a = 40
        b = 3
        c = [10, 20, 30]
        d = [100, 2]

        #lerping two ints
        self.assertEqual(Utils.Lerp(a, b, 0.5), 21.5)

        #lerping int with vector3
        self.assertEqual(Utils.Lerp(b, c, 0.5), [6.5, 10, 15])

        #lerping different length vectors
        self.assertEqual(Utils.Lerp(c, d, 0.5), [55, 11, 15])

    def testHexLerps(self):
        ha = "#0000ff"
        hb = "#ffff00"
        hc = "#ff0000"

        self.assertEqual(Utils.LerpHex(ha, hb, 0.5), "#808080")
        self.assertEqual(Utils.LerpHex(hb, hc, 0.5), "#ff8000")
        self.assertEqual(Utils.LerpHex(ha, hc, 0.1), "#1a00e6")
