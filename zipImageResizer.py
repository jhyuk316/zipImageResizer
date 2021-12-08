from typing import List
import zipfile
import os
from PIL import Image
import io


class ZipImageResizer:
    def __init__(self, sourceFile: str) -> None:
        self.imageExtList = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]
        self.sourceFile = sourceFile

    def zipImageResize(self, height=1280):
        print("self.sourceFile " + self.sourceFile)
        sourceFilePath = os.path.dirname(self.sourceFile)
        sourceFileName = os.path.basename(self.sourceFile)
        sourceFileName, sourceFileExt = os.path.splitext(sourceFileName)

        print(sourceFilePath)
        print(sourceFileName)
        print(sourceFileExt)

        destinationFile = "(resize)" + sourceFileName + sourceFileExt
        destinationFileName = "(resize)" + sourceFileName
        destinationFileExt = sourceFileExt

        targetHeight = height

        with zipfile.ZipFile(self.sourceFile, "r") as sourceZip:
            # set destinationFile name
            count = 1
            if os.path.isfile(sourceFilePath + "\\" + destinationFile):
                destinationFile = (
                    destinationFileName + "(" + str(count) + ")" + destinationFileExt
                )
            while os.path.isfile(sourceFilePath + "\\" + destinationFile):
                destinationFile = (
                    destinationFileName + "(" + str(count) + ")" + destinationFileExt
                )
                count += 1

            print("Making " + sourceFilePath + "\\" + destinationFile)

            # image read and resize
            destinationZip = zipfile.ZipFile(
                sourceFilePath + "\\" + destinationFile, "x"
            )

            for file in sourceZip.namelist():
                print(file)
                fileName, fileExt = os.path.splitext(file)

                if fileExt in self.imageExtList:
                    tempData = sourceZip.read(file)
                    img = Image.open(io.BytesIO(tempData))

                    factor = img.height / targetHeight

                    img_resize = img.resize(
                        (
                            int(round(img.width / factor)),
                            int(round(img.height / factor)),
                        ),
                        Image.LANCZOS,
                    )
                    img_byte_arr = io.BytesIO()
                    img_resize.save(img_byte_arr, format=img.format)
                    destinationZip.writestr(file, img_byte_arr.getvalue())
                else:
                    dateTemp = sourceZip.read(file)
                    destinationZip.writestr(file, dateTemp)

            destinationZip.close()
            print("Complete " + sourceFilePath + "\\" + destinationFile)
