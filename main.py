import tkinter
import tkinter.filedialog
import cv2
import PIL.Image
import PIL.ImageTk
import time
import os
from video_capture import *
from image_capture import *

# create folder directory to save images
folder = r"\images"
cwd = os.getcwd()
path = cwd + folder
if not os.path.exists(path):
    os.makedirs(path)

# create a dictionary for the filters
fil = ['color', 'gray', 'gauss', 'sobel', 'laplace', 'threshold']
filter_dic = {}


def select_filter(filter, status):
    # change required filter to true
    filter_dic = {x: False for x in fil}  # change all values to false in dictionary to make only filter to true
    if filter in filter_dic:
        assert type(status) == bool
        filter_dic[filter] = status
    return filter_dic


class App:
    isImageInstantiated = False
    isVideoInstantiated = False

    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        # Labels
        label1 = tkinter.Label(window, text="Filters")
        label1.grid(row=3, column=13, columnspan=5)

        self.canvas = tkinter.Canvas(self.window, width=300, height=300)
        self.canvas.grid(row=0, column=1, rowspan=15, columnspan=5)

        # buttons of choose
        self.b_snap = tkinter.Button(window, text="Choose an image", command=self.select_image)
        self.b_snap.grid(row=3, column=2)

        self.b_snap = tkinter.Button(window, text="Open your camera", command=self.select_video)
        self.b_snap.grid(row=3, column=3)

        # Button for applying the other filters!
        self.b1 = tkinter.Button(window, text="Gauss", width=15, command=self.gauss_filter)
        self.b1.grid(row=4, column=13)

        self.b2 = tkinter.Button(window, text="Laplace", width=15, command=self.laplace_filter)
        self.b2.grid(row=4, column=17)

        self.b4 = tkinter.Button(window, text="Threshold", width=15, command=self.threshold_filter)
        self.b4.grid(row=6, column=17)

        # note, add sobel filters to the same button, multiple clicks
        self.b5 = tkinter.Button(window, text="Sobel", width=15, command=self.sobel_filter)
        self.b5.grid(row=6, column=13)

        self.b7 = tkinter.Button(window, text="Gray", width=15, command=self.gray_filter)
        self.b7.grid(row=8, column=13)

        self.b8 = tkinter.Button(window, text="Color/No Filter", width=15, command=self.no_filter)
        self.b8.grid(row=9, column=17)

        self.b9 = tkinter.Button(window, text="Snap or Save image", height=4, command=self.snapshot)
        self.b9.grid(row=11, rowspan=2, column=13, columnspan=4)

        self.b10 = tkinter.Button(window, text="Close Program", command=window.destroy)
        self.b10.grid(row=12, rowspan=2, column=17, columnspan=2)

        # After	it is called once, the update method will be automatically called every loop
        self.delay = 15
        self.window.mainloop()

    def select_video(self):
        # create instance from video capture
        self.video_source = 0
        self.vid = VideoCap(self.video_source, self.window)
        self.vid.all_filters = select_filter('color', True)
        self.vid.update()
        self.isVideoInstantiated = True

    def select_image(self):
        # create instance from image capture
        self.img = ImageCap()
        self.img.all_filters = select_filter('color', True)
        self.img.update()
        self.isImageInstantiated = True

    def snapshot(self):
        if self.isImageInstantiated:
            cv2.imwrite(path + r"\frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + '.jpg', self.img.filtered_image)
        elif self.isVideoInstantiated:
            cv2.imwrite(path + r"\frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + '.jpg', self.vid.frame)

    # all filters
    def gray_filter(self):
        if self.isImageInstantiated:
            self.img.all_filters = select_filter('gray', True)
            self.img.update()
        elif self.isVideoInstantiated:
            self.vid.all_filters = select_filter('gray', True)

    def gauss_filter(self):
        if self.isImageInstantiated:
            self.img.all_filters = select_filter('gauss', True)
            self.img.update()
        elif self.isVideoInstantiated:
            self.vid.all_filters = select_filter('gauss', True)

    def laplace_filter(self):
        if self.isImageInstantiated:
            self.img.all_filters = select_filter('laplace', True)
            self.img.update()
        elif self.isVideoInstantiated:
            self.vid.all_filters = select_filter('laplace', True)

    def threshold_filter(self):
        if self.isImageInstantiated:
            self.img.all_filters = select_filter('threshold', True)
            self.img.update()
        elif self.isVideoInstantiated:
            self.vid.all_filters = select_filter('threshold', True)

    def sobel_filter(self):
        if self.isImageInstantiated:
            self.img.all_filters = select_filter('sobel', True)
            self.img.update()
        elif self.isVideoInstantiated:
            self.vid.all_filters = select_filter('sobel', True)

    def no_filter(self):
        if self.isImageInstantiated:
            self.img.all_filters = select_filter('color', True)
            self.img.update()
        elif self.isVideoInstantiated:
            self.vid.all_filters = select_filter('color', True)

    def blue_filter(self):
        if self.isImageInstantiated:
            self.img.all_filters = select_filter('blue', True)
            self.img.update()
        elif self.isVideoInstantiated:
            self.vid.all_filters = select_filter('blue', True)


# Create a window and pass it to the Application object
App(tkinter.Tk(), 'Filterawy')
