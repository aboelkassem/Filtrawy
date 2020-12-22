import tkinter
import tkinter.filedialog
import cv2
import PIL.Image
import PIL.ImageTk
import PIL.ImageFilter
import numpy as np
import random


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
        # check if this class has assigned/has attribute original_image
        # to know if the user choose image and don't close options window
        if hasattr(self, 'original_image'):
            gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)

            if self.all_filters['color']:
                self.update_panel(self.original_image, self.original_image)

            elif self.all_filters['gray']:
                self.update_panel(self.original_image, gray)

            elif self.all_filters['gauss']:
                self.filtered_image = cv2.GaussianBlur(gray, (21, 21), 0)
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['sobel']:
                self.filtered_image = cv2.Sobel(gray, -1, dx=1, dy=0, ksize=11, scale=1, delta=0,
                                                borderType=cv2.BORDER_DEFAULT)
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['laplace']:
                self.filtered_image = cv2.Laplacian(gray, -1, ksize=17, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['threshold']:
                self.filtered_image = cv2.threshold(cv2.absdiff(self.filtered_image, gray), 30, 255, cv2.THRESH_BINARY)[
                    1]
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['median']:
                self.filtered_image = cv2.medianBlur(self.original_image, 5)
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['average']:
                self.filtered_image = cv2.blur(self.original_image, (5, 5))
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['unsharp']:
                gaussian = cv2.GaussianBlur(self.original_image, (0, 0), 2.0)
                self.filtered_image = cv2.addWeighted(self.original_image, 4.0, gaussian, -3.0, 0)
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['logTransformation']:
                c = 255 / np.log(1 + np.max(self.original_image))
                log_image = c * (np.log(self.original_image + 1))
                log_image = np.array(log_image, dtype=np.uint8)
                self.filtered_image = log_image
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['negativeEnhancement']:
                self.filtered_image = 255 - self.original_image
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['powerLowEnhancement']:
                lookUpTable = np.empty((1, 256), np.uint8)
                gamma = 0.8
                for i in range(256):
                    lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
                self.filtered_image = cv2.LUT(self.original_image, lookUpTable)
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['increaseContrast']:
                alpha = random.uniform(1.0, 3.0)
                beta = random.uniform(0, 100)
                self.filtered_image = cv2.addWeighted(self.original_image, alpha,
                                                      np.zeros(self.original_image.shape, self.original_image.dtype), 0,
                                                      beta)
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['decreaseContrast']:
                alpha = random.uniform(1.0, 3.0)
                beta = random.uniform(-100, 0)
                self.filtered_image = cv2.addWeighted(self.original_image, alpha,
                                                      np.zeros(self.original_image.shape, self.original_image.dtype), 0,
                                                      beta)
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['min']:
                size = (3, 3)
                shape = cv2.MORPH_RECT
                kernel = cv2.getStructuringElement(shape, size)
                self.filtered_image = cv2.erode(self.original_image, kernel)
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['max']:
                size = (3, 3)
                shape = cv2.MORPH_RECT
                kernel = cv2.getStructuringElement(shape, size)
                self.filtered_image = cv2.dilate(self.original_image, kernel)
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['prewitt']:
                img_gaussian = cv2.GaussianBlur(gray, (3, 3), 0)
                kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
                kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
                img_prewittx = cv2.filter2D(img_gaussian, -1, kernelx)
                img_prewitty = cv2.filter2D(img_gaussian, -1, kernely)
                self.filtered_image = img_prewittx + img_prewitty
                self.update_panel(self.original_image, self.filtered_image)

            elif self.all_filters['histogramEqualization']:
                self.filtered_image = cv2.equalizeHist(gray)
                self.update_panel(self.original_image, self.filtered_image)