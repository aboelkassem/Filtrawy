import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
import time
import os

# create folder directory to save images
folder = r"\images"
cwd = os.getcwd()
path = cwd + folder
if not os.path.exists(path):
    os.makedirs(path)

# create a dictionary for the filters
fil = ['color', 'gray', 'gauss', 'delta', 'sobel', 'laplace', 'threshold', 'delta_plus', 'blue', 'sobelxy']
filter_dic = {}


def select_filter(filter, status):
    # change required filter to true
    filter_dic = {x: False for x in fil}  # change all values to false in dictionary to make only filter to true
    if filter in filter_dic:
        assert type(status) == bool
        filter_dic[filter] = status
    return filter_dic


# Begin the app
class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source)
        # initialize the filters
        self.all_filters = select_filter('color', True)
        self.frame_delta_plus = None

        # Labels
        label1 = tkinter.Label(window, text="Filters")
        label1.grid(row=0, column=13, columnspan=5)

        label2 = tkinter.Label(window, text="Saving")
        label2.grid(row=8, column=13, columnspan=5)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height)
        self.canvas.grid(row=0, column=1, rowspan=15, columnspan=5)

        # Button that lets the user	take a snapshot
        self.b_snap = tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.b_snap.grid(row=12, column=3, rowspan=7)

        # Button for applying the other filters!
        self.b1 = tkinter.Button(window, text="Gauss", width=15, command=self.gauss_filter)
        self.b1.grid(row=1, column=13)

        self.b2 = tkinter.Button(window, text="Laplace", width=15, command=self.laplace_filter)
        self.b2.grid(row=1, column=17)

        self.b3 = tkinter.Button(window, text="Delta", width=15, command=self.delta_filter)
        self.b3.grid(row=3, column=13)

        self.b3_2 = tkinter.Button(window, text="Delta +", width=10, command=self.delta_filter_plus)
        self.b3_2.grid(row=4, column=13)

        self.b4 = tkinter.Button(window, text="Threshold", width=15, command=self.threshold_filter)
        self.b4.grid(row=3, column=17)

        # note, add sobel filters to the same button, multiple clicks
        self.b5 = tkinter.Button(window, text="Sobel-x, y, xy", width=15, command=self.sobel_filter)
        self.b5.grid(row=5, column=13)

        self.b6 = tkinter.Button(window, text="I'm Blue!", width=15, command=self.blue_filter)
        self.b6.grid(row=5, column=17)

        self.b7 = tkinter.Button(window, text="Gray", width=15, command=self.gray_filter)
        self.b7.grid(row=7, column=13)

        self.b8 = tkinter.Button(window, text="Color/No Filter", width=15, command=self.no_filter)
        self.b8.grid(row=7, column=17)

        self.b9 = tkinter.Button(window, text="Snap Dat!", command=self.snapshot)
        self.b9.grid(row=9, rowspan=2, column=13, columnspan=4)

        self.b10 = tkinter.Button(window, text="Close Program", command=window.destroy)
        self.b10.grid(row=9, rowspan=2, column=17, columnspan=2)

        # After	it is called once, the update method will be automatically called every loop
        self.delay = 15
        self.update()
        self.window.mainloop()

    def snapshot(self):
        cv2.imwrite(path + r"\frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + '.jpg', self.frame)

    def update(self):
        ret, frame, frame1 = self.vid.get_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.all_filters['color'] == True:
            pass
        elif self.all_filters['gray'] == True:
            frame = gray
        elif self.all_filters['gauss'] == True:
            frame = cv2.GaussianBlur(gray, (21, 21), 0)
        elif self.all_filters['delta'] == True:
            frame = cv2.absdiff(frame1, gray)
            # self.frame_delta = frame
        elif self.all_filters['sobel'] == True:
            frame = cv2.Sobel(gray, -1, dx=1, dy=0, ksize=11, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        elif self.all_filters['sobelxy'] == True:
            sobelx = cv2.Sobel(gray, -1, dx=1, dy=0, ksize=11, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
            sobely = cv2.Sobel(gray, -1, dy=1, dx=0, ksize=11, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
            frame = sobelx + sobely
        elif self.all_filters['laplace'] == True:
            frame = cv2.Laplacian(gray, -1, ksize=17, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
        elif self.all_filters['threshold'] == True:
            frame = cv2.threshold(cv2.absdiff(frame1, gray), 30, 255, cv2.THRESH_BINARY)[1]
        elif self.all_filters['delta_plus'] == True:
            if self.frame_delta_plus is None:
                self.frame_delta_plus = cv2.absdiff(frame1, gray)
            frame = cv2.absdiff(self.frame_delta_plus, gray)
        elif self.all_filters['blue'] == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if ret:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.window.after(self.delay, self.update)

        # update frames for snapshot
        self.frame = frame

    # all filters
    def gray_filter(self):
        self.all_filters = select_filter('gray', True)

    def delta_filter_plus(self):
        self.frame_delta_plus = None
        self.all_filters = select_filter('delta_plus', True)

    def gauss_filter(self):
        self.all_filters = select_filter('gauss', True)

    def delta_filter(self):
        self.all_filters = select_filter('delta', True)

    def laplace_filter(self):
        self.all_filters = select_filter('laplace', True)

    def threshold_filter(self):
        self.all_filters = select_filter('threshold', True)

    def sobel_filter(self):
        if self.all_filters['sobel'] == True:
            # means, second click on sobel
            self.all_filters = select_filter('sobelxy', True)
        else:
            self.all_filters = select_filter('sobel', True)

    def no_filter(self):
        self.all_filters = select_filter('color', True)

    def blue_filter(self):
        self.all_filters = select_filter('blue', True)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable	to open	video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        global_frame1 = None
        self.frame1 = global_frame1

    def get_frame(self):
        ret, frame = self.vid.read()

        if self.vid.isOpened():
            if self.frame1 is None:
                self.frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if ret:
                return (ret, frame, self.frame1)
            else:
                return ret, None
        else:
            return ret, None

    # clear the video when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


# Create a window and pass it to the Application object
App(tkinter.Tk(), 'Filterawy')
