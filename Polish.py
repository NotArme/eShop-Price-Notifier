from audioop import avgpp
import Utils

bestValuePercent = 0.5
worstValuePercent = 1.2
bestValue = "#5effb4"
worstValue = "#ff424f"
defaultWhite = "#f3f3f3"
defaultBlack = "#202020"

def GetTextColor(currPrice, avgPrice):
    return GetValueColor(currPrice, avgPrice, worstValue, defaultBlack, bestValue)

def GetBackgroundColor(currPrice, avgPrice):
    return GetValueColor(currPrice, avgPrice, worstValue, defaultWhite, bestValue)

def GetValueColor(currPrice, avgPrice, maxColor, avgColor, minColor):
    if currPrice == avgPrice:
        return avgColor
    
    if currPrice < avgPrice:
        t = Utils.InverseLerp(avgPrice, avgPrice * bestValuePercent, currPrice)
        return Utils.LerpHex(avgColor, minColor, min(t,1))
    
    if currPrice > avgPrice:
        t = Utils.InverseLerp(avgPrice, avgPrice * worstValuePercent, currPrice)
        return Utils.LerpHex(avgColor, maxColor, min(t,1))