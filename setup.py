#file used to create executable

from Utils import GetAllFilepathsOnDir

from distutils.core import setup
import py2exe

dataFiles = ["./gameData/.404list", "./gameData/.gamedb.json"]
uiPath = "./ui"
previewImagesPath = "./gameData/preview"

py2exe_options = dict(
                 bundle_files=2,
                 )

setup(name='eShop Tracker',
      version='1.0',
      description='Simple software to track prices on nintendo switch e-shop',
      author='NotArme',
      windows=['Main.py'],
      data_files=[("gameData", dataFiles), ("ui", GetAllFilepathsOnDir(uiPath)), ("gameData/preview", GetAllFilepathsOnDir(previewImagesPath))],
      options={'py2exe': py2exe_options})


