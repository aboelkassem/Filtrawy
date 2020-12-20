import tkinter
import tkinter.filedialog
import cv2
import PIL.Image
import PIL.ImageTk


class ImageCap:
    def __init__(self, window=None):
        self.window = window
        # open a file chooser dialog and allow the user to select an input image
        img_path = tkinter.filedialog.askopenfilename()
        if len(img_path) > 0:
            # read image
            self.original_image = cv2.imread(img_path)
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.filtered_image = None
            self.panelA = None
            self.panelB = None

            # initialize the filters
            self.all_filters = None

            self.update_panel(self.original_image, self.original_image)

    def update_panel(self, original_image, filtered_image):

        # convert the images to PIL and ImageTK format
        original_image = PIL.Image.fromarray(original_image)
        filtered_image = PIL.Image.fromarray(filtered_image)

        original_image = original_image.resize((400, 400), PIL.Image.ANTIALIAS)
        filtered_image = filtered_image.resize((400, 400), PIL.Image.ANTIALIAS)

        original_image = PIL.ImageTk.PhotoImage(original_image)
        filtered_image = PIL.ImageTk.PhotoImage(filtered_image)

        # if the panels are None, initialize them
        if self.panelA is None or self.panelB is None:
            # the first panel will store our original image
            self.panelA = tkinter.Label(image=original_image)
            self.panelA.image = original_image
            self.panelA.grid(row=3, column=2, sticky="nsew")
            # while the second panel will store the edge map
            self.panelB = tkinter.Label(image=filtered_image)
            self.panelB.image = filtered_image
            self.panelB.grid(row=3, column=3, sticky="nsew")
        # otherwise, update the image panels
        else:
            # update the pannels
            self.panelA.configure(image=original_image)
            self.panelB.configure(image=filtered_image)
            self.panelA.image = original_image
            self.panelB.image = filtered_image

    def update(self):
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)

        if self.all_filters['color']:
            self.update_panel(self.original_image, self.original_image)
        elif self.all_filters['gray']:
            self.update_panel(self.original_image, gray)
        elif self.all_filters['gauss']:
            self.filtered_image = cv2.GaussianBlur(gray, (21, 21), 0)
            self.update_panel(self.original_image, self.filtered_image)
        elif self.all_filters['sobel']:
            self.filtered_image = cv2.Sobel(gray, -1, dx=1, dy=0, ksize=11, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
            self.update_panel(self.original_image, self.filtered_image)
        elif self.all_filters['laplace']:
            self.filtered_image = cv2.Laplacian(gray, -1, ksize=17, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
            self.update_panel(self.original_image, self.filtered_image)
        elif self.all_filters['threshold']:
            self.filtered_image = cv2.threshold(cv2.absdiff(self.filtered_image, gray), 30, 255, cv2.THRESH_BINARY)[1]
            self.update_panel(self.original_image, self.filtered_image)
