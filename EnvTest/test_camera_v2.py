import time
from picamera2 import Picamera2, Preview

wait = 5
buffer = 1

def main():
    picam2 = Picamera2()
    preview = picam2.create_preview_configuration()
    picam2.configure(preview)

    picam2.start(show_preview=None)

    qtgl1 = time.monotonic()
    print("QT GL Preview")
    time.sleep(buffer)
    picam2.start_preview(Preview.QTGL)
    time.sleep(wait)
    picam2.stop_preview()
    qtgl2 = time.monotonic()

    null1 = time.monotonic()
    print("Null Preview")
    time.sleep(buffer)
    picam2.start_preview(Preview.NULL)
    time.sleep(wait)
    picam2.stop_preview()
    null2 = time.monotonic()

    qt1 = time.monotonic()
    print("QT Preview")
    time.sleep(buffer)
    picam2.start_preview(Preview.QT)
    time.sleep(wait)
    picam2.stop_preview()
    qt2 = time.monotonic()

    picam2.close()

    print(f"QT GL Cycle Result: {qtgl2-qtgl2-wait-buffer} s")
    print(f"NULL Cycle Result: {null2-null1-wait-buffer} s")
    print(f"QT Cycle Result: {qt2-qt1-wait-buffer} s")




if __name__ == '__main__':
    Picamera2.set_logging()
    main()
