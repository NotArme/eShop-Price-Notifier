from typing import Union

def Lerp(valA: Union[list, float, int], valB: Union[list, float, int], t: float) -> Union[list, float]:
    if (not isinstance(valA, list)) and (not isinstance(valB, list)):
        #if no lists were passed, just return the single value lerp
        return _lerpSingleVal(valA, valB, t)

    if not isinstance(valA, list):
        valA = [valA]
    if not isinstance(valB, list):
        valB = [valB]

    i = 0
    resultVector = []
    while i < len(valA) or i < len(valB):
        if i >= len(valA):
            a = 0 #if input vectors have different sizes, just assume a value of 0 for non existent indexes
        else:
            a = valA[i]

        if i >= len(valB):
            b = 0 #if input vectors have different sizes, just assume a value of 0 for non existent indexes
        else:
            b = valB[i]

        r = _lerpSingleVal(a, b, t)
        resultVector.append(r)
        i += 1

    return resultVector

def _lerpSingleVal(valA: float, valB: float, t: float) -> float:
    return round(valA + (valB - valA) * t, 6)

def InverseLerp(valA: float, valB: float, valX: float):
    return round((valX - valA) / (valB - valA), 6)

def LerpHex(valA: str, valB: str, t: float) -> str:
    return RgbToHex(Lerp(HexToRgb(valA), HexToRgb(valB), t))

def HexToRgb(hexcode: str) -> list[int]:
    hexcode = hexcode.replace("#","")
    r = hexcode[0:2]
    g = hexcode[2:4]
    b = hexcode[4:6]

    rgb = [int(r, base= 16), int(g, base= 16), int(b, base= 16)]
    return rgb

def RgbToHex(rgbcode: list[int]) -> str:
    hex = "#"
    for col in rgbcode:
        col = round(col)
        hex += f"{col:02x}"
    return hex

