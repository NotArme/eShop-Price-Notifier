#file used to create executable

from Utils import GetAllFilepathsOnDir

from cx_Freeze import setup, Executable

dataFiles = ["./gameData/.404list", "./gameData/.gamedb.json"]
uiPath = "./ui"
previewImagesPath = "./gameData/preview"
iconsPath = "./icons"

def CxfreezeIncludeFilesInput(filepathList: str):
      endlist = []
      for file in filepathList:
            tupleFilePlusDir = (file, file)
            endlist.append(tupleFilePlusDir)
      return endlist

includeFiles = []
includeFiles.extend(CxfreezeIncludeFilesInput(dataFiles))
includeFiles.extend(CxfreezeIncludeFilesInput(GetAllFilepathsOnDir(uiPath)))
includeFiles.extend(CxfreezeIncludeFilesInput(GetAllFilepathsOnDir(previewImagesPath)))
includeFiles.extend(CxfreezeIncludeFilesInput(GetAllFilepathsOnDir(iconsPath)))

build_exe_options = {"excludes": ["tkinter", "unittest"],
                     "include_files": includeFiles,
                     "packages": ["multiprocessing", "requests", "lxml", "dateutil"]}

setup(name='eShop Tracker',
      version='1.0',
      description='Simple software to track prices on nintendo switch e-shop',
      author='NotArme',
      options={"build_exe": build_exe_options},
      executables= [Executable("Main.py", base = "Win32GUI", icon="icons/MainIcon.ico"),
                    Executable("GameDB.py", icon="icons/UpdateIcon.ico")],
      package_dir={"": ""})


