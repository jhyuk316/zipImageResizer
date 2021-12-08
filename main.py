import time
from typing import List
import zipImageResizer
import sys


def main(argv: List[str]):
    if len(argv) < 2:
        print("사용법 zipImageResizer.py 압축파일명 (높이)")
        print("이미지 압축 파일을 지정된 높이(기본값 : 1280)로 리사이징 후 재압축")
        print("jpg의 경우 퀄리티 90%")
        return -1

    name = argv[0]
    targetFile = argv[1]
    targetHeight = 1280

    if len(argv) == 3 and argv[2].isdigit:
        targetHeight = int(argv[2])

    zir = zipImageResizer.ZipImageResizer(targetFile)

    startTime = time.time()
    zir.zipImageResize(targetHeight)
    endTime = time.time()

    print(f"time : {endTime- startTime:.2f}s")

    return 0


if __name__ == "__main__":
    print("zipImageResizer\n")
    # main(["test", r"C:\GitHub\zipImageResizer\sample\testImages.zip"])
    main(sys.argv)
