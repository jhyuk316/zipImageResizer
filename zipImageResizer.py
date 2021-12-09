from typing import List
import zipfile
import os
from PIL import Image
import io


class ZipImageResizer:
    def __init__(self, sourceFile: str) -> None:
        self.imageExtList = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]
        self.sourceFile = sourceFile
        self.quality = 90

        if not os.path.isfile(self.sourceFile):
            raise ValueError("잘못된 경로 및 파일명.")

    def zipImageResize(self, height=1280):
        print("sourceFile : " + self.sourceFile)
        sourceFilePath = os.path.dirname(self.sourceFile)
        sourceFileName = os.path.basename(self.sourceFile)
        sourceFileName, sourceFileExt = os.path.splitext(sourceFileName)

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

            for i, file in enumerate(sourceZip.namelist()):
                print(f"{i+1:3} : {file}")
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
                    img_resize.save(
                        img_byte_arr, format=img.format, quality=self.quality
                    )
                    destinationZip.writestr(file, img_byte_arr.getvalue())
                else:
                    dateTemp = sourceZip.read(file)
                    destinationZip.writestr(file, dateTemp)

            destinationZip.close()
            print("Complete " + sourceFilePath + "\\" + destinationFile)
