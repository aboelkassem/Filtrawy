import tkinter
import tkinter.filedialog
import cv2
import PIL.Image
import PIL.ImageTk


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
            frame = cv2.threshold(cv2.absdiff(frame1, gray), 30, 255, cv2.THRESH_BINARY)[1]

        if ret:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.window.after(15, self.update)

        # update frames for snapshot
        self.frame = frame
