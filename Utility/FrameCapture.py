import tkinter as tk
from PIL import Image
from picamera2 import Picamera2, Preview
from io import BytesIO
import threading
import time
import os
import shutil

MAX_IMAGES = 2000

class CameraApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.resizable(False, False)

        self.camera = Picamera2()
        self.preview_config = self.camera.create_preview_configuration(main={"size": (640, 480)})
        self.camera.configure(self.preview_config)

        self.camera.start(show_preview=None)
        self.camera.start_preview(Preview.QTGL)

        self.static_text = tk.Label(window, text="Label (Catetory)")
        self.static_text.pack(side=tk.LEFT)

        self.label = tk.Entry(window)
        self.label.insert(0, "1")
        self.label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.btn_start = tk.Button(window, text="start Capture", command=self.start_capture)
        self.btn_start.pack(side=tk.TOP, fill=tk.X)

        self.btn_stop = tk.Button(window, text="Stop Capture", command=self.stop_capture, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.TOP, fill=tk.X)

        self.canvas = tk.Canvas(window, width=640, height=480)

        self.running = False
        self.capture_thread = None        

    def start_capture(self):
        folder_number = self.label.get()
        if folder_number and not self.running:
            self.running = True
            self.folder_name = folder_number
            if os.path.exists(self.folder_name):
                shutil.rmtree(self.folder_name)

            os.makedirs(self.folder_name)

            self.capture_thread = threading.Thread(target = self.capture_images)
            self.capture_thread.start()

            self.btn_start['state'] = tk.DISABLED
            self.btn_stop['state'] = tk.NORMAL
    
    def stop_capture(self):
        self.running = False
        if self.capture_thread:
            self.capture_thread.join()

        self.btn_start['state'] = tk.NORMAL
        self.btn_stop['state'] = tk.DISABLED

    def capture_images(self):
        frame_count = 0
        while self.running:
            if frame_count >= MAX_IMAGES:
                self.running = False
                self.btn_start['state'] = tk.NORMAL
                self.btn_stop['state'] = tk.DISABLED
                break
            image_path = os.path.join(self.folder_name, f'image_{frame_count}.jpg')
            self.camera.capture_file(image_path)
            frame_count += 1
            time.sleep(0.5)


root = tk.Tk()
app = CameraApp(root, "Frame Capture by Richard Zhou @rose-hulman")
root.mainloop()


