import tkinter
import tkinter.filedialog
import cv2
import PIL.Image
import PIL.ImageTk
import numpy as np
import random

class VideoCap:
    def __init__(self, video_source=0, window=None):
        self.window = window
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        global_frame1 = None
        self.frame1 = global_frame1

        # initialize the filters
        self.all_filters = None
        self.frame_delta_plus = None

        # Create a canvas that can fit the above  video	source size
        self.canvas = tkinter.Canvas(self.window, width=self.width, height=self.width)
        self.canvas.grid(row=0, column=1, rowspan=15, columnspan=5)

    def get_frame(self):
        ret, frame = self.vid.read()

        if self.vid.isOpened():
            if self.frame1 is None:
                self.frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if ret:
                return ret, frame, self.frame1
            else:
                return ret, None
        else:
            return ret, None

    # clear the video when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def update(self):
        ret, frame, frame1 = self.get_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        color = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if self.all_filters['color']:
            pass
        elif self.all_filters['gray']:
            frame = gray

        elif self.all_filters['gauss']:
            frame = cv2.GaussianBlur(gray, (21, 21), 0)

        elif self.all_filters['sobel']:
            frame = cv2.Sobel(gray, -1, dx=1, dy=0, ksize=11, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

        elif self.all_filters['laplace']:
            frame = cv2.Laplacian(gray, -1, ksize=17, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)

        elif self.all_filters['threshold']:
            frame = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]

        elif self.all_filters['median']:
            frame = cv2.medianBlur(frame, 5)

        elif self.all_filters['average']:
            frame = cv2.blur(frame, (5, 5))

        elif self.all_filters['unsharp']:
            gaussian = cv2.GaussianBlur(color, (0, 0), 2.0)
            frame = cv2.addWeighted(color, 1.0 + 3.0, gaussian, -3.0, 0)

        elif self.all_filters['logTransformation']:
            c = 255 / np.log(1 + np.max(color))
            log_image = c * (np.log(color + 1))
            frame = np.array(log_image, dtype=np.uint8)

        elif self.all_filters['negativeEnhancement']:
            frame = 255 - color

        elif self.all_filters['powerLowEnhancement']:
            lookUpTable = np.empty((1, 256), np.uint8)
            gamma = 0.8
            for i in range(256):
                lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
            frame = cv2.LUT(frame, lookUpTable)

        elif self.all_filters['increaseContrast']:
            frame = cv2.addWeighted(frame, 1.9, frame, 0, 20)

        elif self.all_filters['decreaseContrast']:
            frame = cv2.addWeighted(frame, 0.8, frame, 0, -10)

        if ret:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.window.after(15, self.update)

        # update frames for snapshot
        self.frame = frame
