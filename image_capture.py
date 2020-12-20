import tkinter
import tkinter.filedialog
import cv2
import PIL.Image
import PIL.ImageTk
import numpy as np
import matplotlib.pyplot as plt

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


#-----------------------------------------------------------------------------------------------------------
        elif self.all_filters['median']:
            self.filtered_image = cv2.medianBlur(self.original_image, 5)
            self.update_panel(self.original_image, self.filtered_image)
        elif self.all_filters['average']:
            m, n, _ = self.original_image.shape
            mask = np.ones([3, 3], dtype=int)
            mask = mask / 9
            img_new = np.zeros([m, n])
            img = self.original_image
            for i in range(1, m - 1):
                for j in range(1, n - 1):
                    temp = img[i - 1, j - 1] * mask[0, 0] + img[i - 1, j] * mask[0, 1] + img[i - 1, j + 1] * mask[
                        0, 2] + img[
                               i, j - 1] * mask[1, 0] + img[i, j] * mask[1, 1] + img[i, j + 1] * mask[1, 2] + img[
                               i + 1, j - 1] * mask[
                               2, 0] + img[i + 1, j] * mask[2, 1] + img[i + 1, j + 1] * mask[2, 2]

                    img_new[i, j] = temp
            img_new = img_new.astype(np.uint8)
            img_new = self.filtered_image
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
            img = self.original_image
            height, width, _ = img.shape
            for i in range(0, height - 1):
                for j in range(0, width - 1):
                    pixel = img[i, j]
                    pixel[0] = 255 - pixel[0]
                    pixel[1] = 255 - pixel[1]
                    pixel[2] = 255 - pixel[2]
                    img[i, j] = pixel
            self.filtered_image = img
            self.update_panel(self.original_image, self.filtered_image)
        elif self.all_filters['powerLowEnhancement']:
            im_power_law_transformation = cv2.pow(self.original_image/255.0, 0.6)
            self.filtered_image = im_power_law_transformation
            self.update_panel(self.original_image, self.filtered_image)

