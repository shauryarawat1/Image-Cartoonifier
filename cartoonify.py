import cv2 #for image processing
import easygui #to open the file box
import numpy as np # to store the image
import imageio #to read image stored at particular path
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

# fileopenbox opens the box to choose file and help us store file path as string
def upload():
    ImagePath = easygui.fileopenbox()
    cartoonify(ImagePath)

def cartoonify(ImagePath):
    originalimage = cv2.imread(ImagePath)
    originalimage = cv2.cvtColor(originalimage, cv2.COLOR_BGR2RGB)
    # image is stored in form of numbers

    # confirm that image is chosen
    if originalimage is None:
        print("Cant find image")
        sys.exit()

    Resized1 = cv2.resize(originalimage, (960, 540))

    #converting image to grayscale
    grayScaleImage = cv2.cvtColor(originalimage, cv2.COLOR_BGR2GRAY)
    Resized2 = cv2.resize(grayScaleImage, (960, 540))

    #applying median blur to smooth the image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    Resized3 = cv2.resize(smoothGrayScale, (960, 540))


    # retrieve the edges for cartoon effect by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    Resized4 = cv2.resize(getEdge, (960, 540))

    # applying bilateral filter to remove noise and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalimage, 9, 300, 300)
    Resized5 = cv2.resize(colorImage, (960, 540))

    #masking edged image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask = getEdge)

    Resized6 = cv2.resize(cartoonImage, (960, 540))

    #Plotting the whole transaction
    images = [Resized1, Resized2, Resized3, Resized4, Resized5, Resized6]
    fig, axes = plt.subplots(3, 2, figsize=(8,8), subplot_kw = {'xticks':[], 'yticks':[]}, gridspec_kw = dict(hspace = 0.1, wspace = 0.1))

    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap = 'gray')

    plt.show()

#Making the main window
top = tk.Tk()
top.geometry('400x400')
top.title("Cartoonify the image")
top.configure(background='white')
label = Label(top, background='#CDCDCD', font=('calibri', 20, 'bold'))

#Making the cartoonify button
upload = Button(top, text="Cartoonify the image", command = upload, padx= 10, pady = 5)
upload.configure(background = '#364156', foreground='white', font=('calibri', 10, 'bold'))
upload.pack(side = TOP, pady = 50)

top.mainloop()

