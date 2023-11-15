import sys
import tkinter as tk
import Scratchtoolv2 as scratch
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os
import csv
import numpy as np
from tkinter.messagebox import showerror


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image

    resized = cv2.resize(image, dim, interpolation=inter)
    return resized

    # return the resized image


def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    Scratch.imageset = None
    console.config(text="")
    global folder_path
    filename = filedialog.askdirectory(initialdir=os.getcwd())
    print(filename)
    folder_path.set(filename)
    Scratch.set_datapath(filename)
    Scratch.set_dict(Scratch.create_imagedict(Scratch.datapath, mode=str(Scratch.variant)))
    if len(Scratch.dict) == 0:
        img_raw.config(text="Cant show a preview!", image="")
    if len(Scratch.dict) == 1:
        Scratch.get_imageset(Scratch.datapath)
        show_raw_img(Scratch.imageset)
        img_raw.bind('<Configure>', lambda event: show_raw_img(Scratch.imageset, index=imgindex))
    else:

        Scratch.get_imageset(list(Scratch.dict.values())[0])
        show_raw_img(Scratch.imageset)
        img_raw.bind('<Configure>', lambda event: show_raw_img(Scratch.imageset, index=imgindex))
    console.config(
        text="The folder contains " + str(len(Scratch.dict)) + " different " + str(
            Scratch.variant) + " datasets, the first set is displayed.",
        image="")


def saveconfig(path=None):
    if path is None:
        filename = filedialog.askdirectory(initialdir=os.getcwd())
    else:
        filename = path
    labellist = list()
    valuelist = list()

    labellist.append(morphlabel.cget("text"))
    # labellist.append(threshold1label1['text'])
    # labellist.append(threshold1label2['text'])
    labellist.append(erolabel['text'])
    labellist.append(blurlabel['text'])
    # labellist.append(threshold2label1['text'])
    labellist.append(threshold2label2['text'])
    labellist.append(transformationlabel['text'])
    # labellist.append(threshold3label1['text'])
    labellist.append(threshold3label2['text'])

    valuelist.append(morphslider.get())
    # valuelist.append(threshold1entry1.get())
    # valuelist.append(threshold1slider.get())
    valuelist.append(eroslider.get())
    valuelist.append(blurslider.get())
    # valuelist.append(threshold2entry1.get())
    valuelist.append(threshold2slider.get())
    valuelist.append(transformationslider.get())
    # valuelist.append(threshold3entry1.get())
    valuelist.append(threshold3slider.get())

    np.savetxt(filename + "/" + "config.txt", [p for p in zip(labellist, valuelist)], delimiter='=', fmt='%s')


def loadconfig(path=None):
    if path is None:
        filename = filedialog.askopenfilename(initialdir=os.getcwd())
    else:
        filename = path

    settings = np.genfromtxt(filename, delimiter="=", dtype=str)

    a = np.where(settings == "MorphEx-impact")
    value = settings[a[0][0]][a[1][0] + 1]
    morphslider.set(value)
    '''
    a = np.where(settings == "Threshold 1 Type")
    value = settings[a[0][0]][a[1][0] + 1]
    threshold1entry1.config(text = value)
    
    a = np.where(settings == "Threshold 1 Min-value")
    value = settings[a[0][0]][a[1][0] + 1]
    threshold1slider.set(value)
    '''
    a = np.where(settings == "Dilation(only DAPI)")
    value = settings[a[0][0]][a[1][0] + 1]
    eroslider.set(value)

    a = np.where(settings == "Blurring")
    value = settings[a[0][0]][a[1][0] + 1]
    blurslider.set(value)
    '''
    a = np.where(settings == "Threshold 2 Type")
    value = settings[a[0][0]][a[1][0] + 1]
    threshold2entry1.config(text = value)
    '''
    a = np.where(settings == "Threshold 2 Min-value")
    value = settings[a[0][0]][a[1][0] + 1]
    threshold2slider.set(value)

    a = np.where(settings == "lin. Transformation")
    value = settings[a[0][0]][a[1][0] + 1]
    transformationslider.set(value)

    '''
    a = np.where(settings == "Threshold final Type")
    value = settings[a[0][0]][a[1][0] + 1]
    threshold3entry1.config(text = value)
    '''
    a = np.where(settings == "Threshold final Min-value")
    value = settings[a[0][0]][a[1][0] + 1]
    threshold3slider.set(value)

def show_raw_img(img, index=0):
    if index == len(img):
        index = 0
    if index == -1:
        index = len(img) - 1

    # print("labelwidth: " + str(img_raw.winfo_width()))
    img = image_resize(img[index], height=img_raw.winfo_height() - 5)
    # print("imagesize" + str(np.shape(img)))
    img_tk = ImageTk.PhotoImage(image=Image.fromarray(img))
    img_raw.config(image=img_tk)
    img_raw.image = img_tk
    global imgindex
    imgindex = index


def show_img1_scratch(img):
    if img1_scratch.winfo_height() > 5 and Scratch.imageset is not None:
        img = image_resize(img, height=img1_scratch.winfo_height() - 5)
        # print("imagesize" + str(np.shape(img)))
        img_tk = ImageTk.PhotoImage(image=Image.fromarray(img))
        img1_scratch.config(image=img_tk)
        img1_scratch.image = img_tk


def start_calc_single():
    Scratch.calc_mig(Scratch.datapath, scaled=backgroundscaling.get())
    Scratch.plot_migprogress(Scratch.migprogresslist, (10, 10), "Mirgrationprogress")
    openplotwindow()


def start_calc_complete():
    resultlist = list()
    if not os.path.exists(Scratch.datapath + "/" + "results"):
        os.mkdir(Scratch.datapath + "/" + "results")
    for k, key in enumerate(Scratch.dict):
        Scratch.get_imageset(Scratch.dict[key])
        Scratch.calc_mask(Scratch.imageset[0])
        Scratch.calc_mig(scaled=backgroundscaling.get())
        Scratch.migprogresslist.insert(0, key)
        resultlist.append(Scratch.migprogresslist)
        cv2.imwrite(Scratch.datapath + "/" + "results" + "/" + str(list(Scratch.dict)[k]) + "scratch_detect.png",
                    Scratch.img_contour)
        console2.config(text="calculation " + str(k + 1) + " of " + str(len(Scratch.dict)) + " finished")
        root.update()
    Scratch.resultlist = resultlist
    # np.savetxt(savepath + "/" + "migprogress.csv", resultlist, delimiter=',', fmt = "%s")


    with open(Scratch.datapath + "/" + "results" + "/" + "migprogress_" + str(Scratch.variant) +  "_complete.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(resultlist)

    Scratch.plot_result(Scratch.resultlist, (10, 10), "Mirgrationprogress")
    openplotwindow()

    Scratch.get_imageset(list(Scratch.dict.values())[0])


def openplotwindow():
    plotwindow = tk.Toplevel(root)
    plotwindow.title("Migrationprogressplot")
    plotwindow.configure(background='gray17')
    # frame = tk.Frame(plotwindow)
    plotwindow.geometry("800x800")
    savegifbutton = tk.Button(plotwindow, text="Save Animation", command=savegif, bg="gray17", fg="gray70").pack()

    img_tk = ImageTk.PhotoImage(image=Image.fromarray(Scratch.plotarray))
    plotimg = tk.Label(plotwindow, bg="gray17", fg="gray70")
    plotimg.pack(fill="both", expand=True)
    plotimg.bind('<Configure>', lambda event: showplot(plotimg))
    plotwindow.mainloop()


def showplot(widget):
    img = image_resize(Scratch.plotarray, height=widget.winfo_height() - 5)
    # print("imagesize" + str(np.shape(img)))
    img_tk = ImageTk.PhotoImage(image=Image.fromarray(img))
    widget.config(image=img_tk)
    widget.image = img_tk


def savegif():
    Scratch.gen_gif()
    Scratch.save_gif()


def show_imgcalc(img):
    if img_calc.winfo_height() > 5:
        img = image_resize(img, height=img_calc.winfo_height() - 5)

        # print("imagesize" + str(np.shape(img)))
        img_tk = ImageTk.PhotoImage(image=Image.fromarray(img))
        img_calc.config(image=img_tk)
        img_calc.image = img_tk


def set_variant():
    Scratch.set_variant(variant.get())
    button_path.config(state = "normal")
    if variant.get() == "RFP":
        loadconfig(path=resource_path("rfp_default.txt"))
    elif variant.get() == "DAPI":
        loadconfig(path=resource_path("dapi_default.txt"))


def set_backgroundscaling():
    return 0


def forward():
    show_raw_img(Scratch.imageset, imgindex + 1)


def backward():
    show_raw_img(Scratch.imageset, imgindex - 1)


def setter(Scratchtool):
    Scratchtool.set_morphexkernel(morphslider.get())
    # Scratchtool.set_threshold1type(threshold1entry1.get())
    # Scratchtool.set_threshold1val(threshold1slider.get())
    Scratchtool.set_dilationkernel(eroslider.get())
    Scratchtool.set_blurring(blurslider.get())
    # Scratchtool.set_threshold2type(threshold2entry1.get())
    Scratchtool.set_threshold2val(threshold2slider.get())
    Scratchtool.set_lineartrans(transformationslider.get())


def setter2(Scratchtool):
    # Scratchtool.set_threshold3type(threshold3entry1.get())
    Scratchtool.set_threshold3val(threshold3slider.get())


def callback_1(event):
    dataimport2.pack(fill="both", expand=True)
    dataimport.pack(fill="both", expand=True, padx='5', pady='5')
    dataimport3.pack(anchor="w")
    scratchdetection2.pack_forget()
    scratchdetection.pack(fill="both", expand=False, padx='5', pady='5', )
    migcalc2.pack_forget()
    migcalc.pack(fill="both", padx='5', expand=False, pady='5')


def callback_2(event):
    dataimport2.pack_forget()
    dataimport.pack(fill="both", expand=False, padx='5', pady='5')
    scratchdetection2.pack(fill="both", expand=True)
    scratchdetection.pack(fill="both", expand=True, padx='5', pady='5', )
    migcalc2.pack_forget()
    migcalc.pack(fill="both", padx='5', expand=False, pady='5')
    setter(Scratch)
    if Scratch.imageset != None:
        Scratch.calc_mask(Scratch.imageset[0])
        show_img1_scratch(Scratch.img_contour)
    # print(str(folder_path.get()) + "/contour" +  ".png")
    # cv2.imwrite(str(folder_path.get()) + "/" + "image0" +  ".png", Scratch.imageset[0])
    # cv2.imwrite(str(folder_path.get()) + "/" + "tophat" + ".png", Scratch.im1_morphology)
    # cv2.imwrite(str(folder_path.get()) + "/" + "blur" + ".png", Scratch.im1_blur)
    # cv2.imwrite(str(folder_path.get()) + "/" + "thresholdtophat" + ".png", Scratch.im1_threshold2)
    # cv2.imwrite(str(folder_path.get()) + "/" + "contour" + ".png", Scratch.img_contour)
    # cv2.imwrite(str(folder_path.get()) + "/" + "scratch" + ".png", Scratch.im_thresh_scratch_list[-1])


def callback_3(event):
    dataimport2.pack_forget()
    dataimport.pack(fill="both", expand=False, padx='5', pady='5')
    scratchdetection2.pack_forget()
    scratchdetection.pack(fill="both", expand=False, padx='5', pady='5', )
    migcalc2.pack(fill="both", expand=True)
    migcalc.pack(fill="both", padx='5', expand=True, pady='5')
    setter2(Scratch)
    Scratch.calc_imgcalc()

    # print(Scratch.img_calc)

    show_imgcalc(Scratch.img_calc)


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="gray17", foreground="gray70", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


root = tk.Tk()
root.geometry("1100x900")
root.title("Scratch-Assay-Tool")
root.iconphoto("wm", tk.PhotoImage(file=resource_path("logo/friedrich-alexander-universitaet-logo.gif")))
###PARA
Scratch = scratch.Scratchtool()
folder_path = tk.StringVar()
variant = tk.StringVar()
backgroundscaling = tk.BooleanVar()
imgindex = 0
###PARA

###DATAIMPORT###
dataimport = tk.Frame(root, bg="grey17")
dataimport.bind("<Button-1>", callback_1)
dataimport.pack(fill="both", expand=True, padx='5', pady='5')
header_dataimport = tk.Label(dataimport, text="1. Dataimport", font=30, bg="gray17", fg="gray70")
header_dataimport.bind("<Button-1>", callback_1)
header_dataimport.pack()

dataimport2 = tk.Frame(dataimport, bg="grey17")
dataimport2.pack(fill="both", expand=True)
dataimport3 = tk.Frame(dataimport2, bg="gray17")
dataimport3.pack(side="left", fill="both", expand=True)
radioheader = tk.Label(dataimport3, text="Choose a variant:", bg="gray17", fg="gray70")
radioheader.grid(row=0, column=0, columnspan=2, sticky="nwe")
CreateToolTip(radioheader, "Select Imagetype to load default Parameters")
radio1 = tk.Radiobutton(dataimport3, bg="gray17", fg="gray70", activebackground="gray17", activeforeground="gray70",
                        selectcolor="gray17",
                        text="RFP",
                        padx=20,
                        variable=variant,
                        # indicator = 0,
                        value="RFP",
                        command=set_variant).grid(row=1, column=0, sticky="we")
radio2 = tk.Radiobutton(dataimport3, bg="gray17", fg="gray70", activebackground="gray17", activeforeground="gray70",
                        selectcolor="gray17",
                        text="DAPI",
                        padx=20,
                        variable=variant,
                        # indicator = 0,
                        value="DAPI",
                        command=set_variant).grid(row=1, column=1, sticky="we")
variant.set(None)

button_path = tk.Button(dataimport3, text="select datapath", bg="gray17", fg="gray70", command=browse_button, state="disabled")
button_path.grid(column=2, row=0, rowspan=2, sticky="nswe")
CreateToolTip(button_path, "Select the Folder, that contains the Imagesets. Fileformat must be .tif and the datasetname is in the first part of each filename. the Seperator is \"_\". the other part of th name must contain the variant. E.g. \"E6_-1_2_1_StitchedRFP[RFP 531,593]_003.tif\" ")

console = tk.Label(dataimport3, text="Select the Variant and Folder first.", bg="gray17", fg="gray70")
console.grid(row=2, column=0, columnspan=3, sticky="nwe")

img_raw = tk.Label(dataimport3, bg="gray17", fg="gray70")
img_raw.grid(row=0, column=3, rowspan=3, sticky="nsew")
dataimport3.columnconfigure(3, weight=1)
dataimport3.rowconfigure(2, weight=1)

button_back = tk.Button(dataimport3, text="<-", command=backward, bg="gray17", fg="gray70")
button_for = tk.Button(dataimport3, text="->", command=forward, bg="gray17", fg="gray70")
button_back.grid(row=0, column=3, rowspan=2, sticky="w")
button_for.grid(row=0, column=3, rowspan=2, sticky="e")

###SCRATCHDETECTION###
scratchdetection = tk.Frame(root, bg="grey17")
scratchdetection.bind("<Button-1>", callback_2)
scratchdetection.pack(fill="x", padx='5', pady='5', )
header_scratchdetection = tk.Label(scratchdetection, text="2. Scratch-Detection", font=30, bg="gray17", fg="gray70")
header_scratchdetection.bind("<Button-1>", callback_2)
header_scratchdetection.pack()

scratchdetection2 = tk.Frame(scratchdetection, bg="grey17")
morphlabel = tk.Label(scratchdetection2, text="Top-hat-kernel", bg="gray17", fg="gray70")
morphlabel.grid(row=0, column=0)
CreateToolTip(morphlabel, "Kernelsize for Top-hat transformation to correct nonuniform illumination")
morphslider = tk.Scale(scratchdetection2, from_=1, to=100, orient="horizontal", command=callback_2, bg="gray17",
                       fg="gray70")
morphslider.grid(row=0, column=1, sticky="nsew")
morphslider.set(49)

'''
threshold1label1 = tk.Label(scratchdetection2, text="Threshold 1 Type", bg = "gray17", fg = "gray70")
threshold1label1.grid(row=1, column=0)
threshold1entry1 = tk.Entry(scratchdetection2, bg = "gray17", fg = "gray70")
threshold1entry1.grid(row=1, column=1, sticky="nsew")
threshold1entry1.insert(0, "cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU")

threshold1label2 = tk.Label(scratchdetection2, text="Threshold 1 Min-value", bg = "gray17", fg = "gray70")
threshold1label2.grid(row=2, column=0)
threshold1slider = tk.Scale(scratchdetection2, from_=0, to=255, orient="horizontal", command=callback_2, bg = "gray17", fg = "gray70")
threshold1slider.grid(row=2, column=1, sticky="nsew")
threshold1slider.set(10)
'''

erolabel = tk.Label(scratchdetection2, text="Dilation-kernel", bg="gray17", fg="gray70")
erolabel.grid(row=3, column=0)
CreateToolTip(erolabel, "Impact of Morphological Operation (Dilation). Especially useful for DAPI.")
eroslider = tk.Scale(scratchdetection2, from_=0, to=20, orient="horizontal", command=callback_2, bg="gray17",
                     fg="gray70")
eroslider.grid(row=3, column=1, sticky="nsew")
eroslider.set(5)

blurlabel = tk.Label(scratchdetection2, text="Blurring-kernel", bg="gray17", fg="gray70")
blurlabel.grid(row=4, column=0)
CreateToolTip(blurlabel, "Impact of blur to smooth of scratch egde")
blurslider = tk.Scale(scratchdetection2, from_=1, to=200, orient="horizontal", command=callback_2, bg="gray17",
                      fg="gray70")
blurslider.grid(row=4, column=1, sticky="nsew")
blurslider.set(101)
'''
threshold2label1 = tk.Label(scratchdetection2, text="Threshold 2 Type", bg = "gray17", fg = "gray70")
threshold2label1.grid(row=5, column=0)
threshold2entry1 = tk.Entry(scratchdetection2, bg = "gray17", fg = "gray70")
threshold2entry1.grid(row=5, column=1, sticky="nsew")
threshold2entry1.insert(0, "cv2.THRESH_BINARY")
'''
threshold2label2 = tk.Label(scratchdetection2, text="Threshold-Value", bg="gray17", fg="gray70")
threshold2label2.grid(row=6, column=0)
threshold2slider = tk.Scale(scratchdetection2, from_=0, to=254, orient="horizontal", command=callback_2, bg="gray17",
                            fg="gray70")
threshold2slider.grid(row=6, column=1, sticky="nsew")
threshold2slider.set(200)

transformationlabel = tk.Label(scratchdetection2, text="linear scaling", bg="gray17", fg="gray70")
transformationlabel.grid(row=7, column=0)
CreateToolTip(transformationlabel,
              "Use to increase the contoursize to counteract the shrinking effect of the other transformations")
transformationslider = tk.Scale(scratchdetection2, from_=0.5, to=1.5, resolution=0.01, orient="horizontal",
                                command=callback_2, bg="gray17", fg="gray70")
transformationslider.grid(row=7, column=1, sticky="nsew")
transformationslider.set(1)

saveconfigbutton = tk.Button(scratchdetection2, text="save config", bg="gray17", fg="gray70", command=saveconfig).grid(
    column=1, row=8, sticky="nswe")
loadconfigbutton = tk.Button(scratchdetection2, text="load config", bg="gray17", fg="gray70", command=loadconfig).grid(
    column=1, row=9, sticky="nswe")

img1_scratch = tk.Label(scratchdetection2, bg="gray17", fg="gray70", text="Choose a file or folder")
img1_scratch.grid(row=0, column=2, rowspan=11, sticky="nsew")
img1_scratch.bind('<Configure>', lambda event: show_img1_scratch(Scratch.img_contour))
CreateToolTip(img1_scratch,"Shows the first Image of the first Imageset")


scratchdetection2.rowconfigure(10, weight=1)
scratchdetection2.columnconfigure(2, weight=1)
scratchdetection2.columnconfigure(1, weight=1)

###MIGRATION CALCULATION###
migcalc = tk.Frame(root, bg="grey17")
migcalc.bind("<Button-1>", callback_3)
migcalc.pack(fill="x", padx='5', pady='5')
header_migcalc = tk.Label(migcalc, text="3. Migration Calculation", font=30, bg="gray17", fg="gray70")
header_migcalc.bind("<Button-1>", callback_3)
header_migcalc.pack()

migcalc2 = tk.Frame(migcalc, bg="grey17")

'''
threshold3label1 = tk.Label(migcalc2, text="Threshold final Type", bg = "gray17", fg = "gray70")
threshold3label1.grid(row=0, column=0)
threshold3entry1 = tk.Entry(migcalc2, bg = "gray17", fg = "gray70")
threshold3entry1.grid(row=0, column=1, sticky="nsew")
threshold3entry1.insert(0, "cv2.THRESH_BINARY_INV")
'''

threshold3label2 = tk.Label(migcalc2, text="Threshold final Min-value", bg="gray17", fg="gray70")
threshold3label2.grid(row=1, column=0)
threshold3slider = tk.Scale(migcalc2, from_=0, to=254, orient="horizontal", command=callback_3, bg="gray17",
                            fg="gray70")
threshold3slider.grid(row=1, column=1, sticky="nsew")
threshold3slider.set(11)

scalingheader = tk.Label(migcalc2, text="Background Scaling", bg="gray17", fg="gray70").grid(row=2, column=1,
                                                                                             sticky="nswe")
scalingon = tk.Radiobutton(migcalc2, bg="gray17", fg="gray70", activebackground="gray17", activeforeground="gray70",
                           selectcolor="gray17",
                           text="ON",
                           padx=20,
                           variable=backgroundscaling,
                           # indicator = 0,
                           value=True,
                           command=set_backgroundscaling).grid(row=3, column=1, sticky="we")
scalingoff = tk.Radiobutton(migcalc2, bg="gray17", fg="gray70", activebackground="gray17", activeforeground="gray70",
                            selectcolor="gray17",
                            text="OFF",
                            padx=20,
                            variable=backgroundscaling,
                            # indicator = 0,
                            value=False,
                            command=set_backgroundscaling).grid(row=4, column=1, sticky="we")
backgroundscaling.set(True)

console2 = tk.Label(migcalc2, bg="gray17", fg="gray70", text="")
console2.grid(row=5, column=1, sticky="new")

button_startcalc_single = tk.Button(migcalc2, text="start Calculation single", command=start_calc_single, bg="gray17",
                                    fg="gray70")
button_startcalc_single.grid(row=4, column=0, sticky="nwe")

CreateToolTip(button_startcalc_single,
              "Calculates the migrationprogress of the first imageset, saves it as a csv-file in the imagefolder and plots the result in a new window. ")

button_startcalc_complete = tk.Button(migcalc2, text="start Calculation complete", command=start_calc_complete,
                                      bg="gray17", fg="gray70")
button_startcalc_complete.grid(row=5, column=0, sticky="nwe")

CreateToolTip(button_startcalc_complete,
              "Calculates the mirgrationprogess of the whole folder and saves the result as a csv-file in the imagefolder")

img_calc = tk.Label(migcalc2, bg="gray17", fg="gray70")
img_calc.grid(row=0, column=2, rowspan=6, sticky="nsew")
img_calc.bind('<Configure>', lambda event: show_imgcalc(Scratch.img_calc))
CreateToolTip(img_calc, "Shows the threshold of the last image of the first imageset. The migrationprogess should be clearly visible.")

migcalc2.rowconfigure(5, weight=1)
migcalc2.columnconfigure(1, weight=1)
migcalc2.columnconfigure(2, weight=1)

root.mainloop()
