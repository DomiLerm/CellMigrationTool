import imageio
import cv2
import numpy as np
#from PIL import Image
import math
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')
import io
import natsort
import glob
import os
#import CellTracker

class Scratchtool():

    def set_variant(self, variant):
        self.variant = variant

    def set_datapath(self, datapath):
        self.datapath = datapath

    def set_dict(self, dict):
        self.dict = dict

    def set_morphexkernel(self, size):
        self.morphexkernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))

    def set_threshold1type(self, type):
        if type == "cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU":
            self.threshold1type = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU

        elif type == "cv2.THRESH_BINARY":
            self.threshold1type = cv2.THRESH_BINARY

        elif type == "cv2.THRESH_BINARY_INV":
            self.threshold1type = cv2.THRESH_BINARY_INV


    def set_threshold1val(self, value):
        self.threshold1val = value

    def set_dilationkernel(self, size):
        self.dilationkernel = np.ones((size, size), np.uint8)

    def set_blurring(self, size):
        self.blursize = size

    def set_threshold2type(self, type):
        if type == "cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU":
            self.threshold2type = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU

        elif type == "cv2.THRESH_BINARY":
            self.threshold2type = cv2.THRESH_BINARY

        elif type == "cv2.THRESH_BINARY_INV":
            self.threshold2type = cv2.THRESH_BINARY_INV

    def set_threshold2val(self, value):
        self.threshold2val = value

    def set_lineartrans(self, value):
        self.lineartrans = value

    def set_threshold3type(self, type):
        if type == "cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU":
            self.threshold3type = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU

        elif type == "cv2.THRESH_BINARY":
            self.threshold3type = cv2.THRESH_BINARY

        elif type == "cv2.THRESH_BINARY_INV":
            self.threshold3type = cv2.THRESH_BINARY_INV

    def set_threshold3val(self, value):
        self.threshold3val = value

    def find_largest_contours(self, image):
        contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        largest_contour = sorted(contours, key=cv2.contourArea, reverse=True)[0]
        return largest_contour

    def calc_scale_contour(self, contour, scale):
        moments = cv2.moments(contour)
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])

        cnt_norm = contour - [cx, cy]
        cnt_scaled = cnt_norm
        cnt_scaled[:,:,1] = cnt_norm[:,:,1] * scale

        cnt_scaled = cnt_scaled + [cx, cy]
        cnt_scaled = cnt_scaled.astype(np.int32)

        return cnt_scaled

    def get_imageset(self, datapath):
        imglist = list()
        height, width = (math.inf, math.inf)
        if isinstance(datapath, str):
            for image in glob.glob(datapath + '/*.tif'):
                im = cv2.imread(image,  cv2.IMREAD_ANYDEPTH)
                print(image)
                im = cv2.convertScaleAbs(im, alpha=(255.0/65535.0))
                imglist.append(im)
                h, w = im.shape[0:2]
                if h < height:
                    height = h
                if w < width:
                    width = w
        elif isinstance(datapath, list):
            for image in datapath:
                im = cv2.imread(image,  cv2.IMREAD_ANYDEPTH)

                im = cv2.convertScaleAbs(im, alpha=(255.0 / 65535.0))

                imglist.append(im)
                h, w = im.shape[0:2]
                if h < height:
                    height = h
                if w < width:
                    width = w

        else:
            raise ValueError
        # crop image in case of different sizes
        for i, img in enumerate(imglist):
            h, w = img.shape[0:2]
            h_tocrop = math.ceil((h - height) / 2)
            w_tocrop = math.ceil((w - width) / 2)
            # print("height = " + str(height) + "width = " + str(width))
            # print("h_tocrop = " + str(h_tocrop) + "w_tocrop = " + str(w_tocrop))
            imglist[i] = img[h_tocrop: h_tocrop + height, w_tocrop:w_tocrop + width]
        self.imageset = imglist


    def get_imagespaths(sellf, folderpath, mode="RFP"):
        nameslist = glob.glob(folderpath + "/" + "*.tif")
        nameslist = [name for name in nameslist if ("[" + mode) in name]
        nameslist = natsort.natsorted([name.split("\\")[-1] for name in nameslist])
        # nameslist = [folderpath + "\\" + name for name in nameslist]
        print(nameslist)
        return nameslist

    def create_imagedict(self, folderpath, mode="RFP"):
        dict = {}
        seen = list()

        nameslist = glob.glob(folderpath + "/" + "*.tif")
        nameslist = [name for name in nameslist if ("[" + mode) in name]
        nameslist = natsort.natsorted([name.split("\\")[-1] for name in nameslist])

        keys = [name.split("_")[0] for name in nameslist if
                not (name.split("_")[0] in seen or seen.append(name.split("_")[0]))]
        for key in keys:
            dict[key] = [folderpath + "/" + name for name in nameslist if key == name.split("_")[0]]
        print(dict)
        return dict

    def get_samplesize(self, images):
        seen = list()
        samplesize = [str.split("_")[0] for str in images if
                      not (str.split("_")[0] in seen or seen.append(str.split("_")[0]))]
        return samplesize

    def get_setlength(self, images):
        seen = list()
        setlength = [str[-7:-4] for str in images if not (str[-7:-4] in seen or seen.append(str[-7:-4]))]
        return setlength


    def calc_mask(self, img1):
        self.im1_morphology = cv2.morphologyEx(img1, cv2.MORPH_TOPHAT, self.morphexkernel, 1)
        x, im1_threshold1 = cv2.threshold(self.im1_morphology, 0, int(255), cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)   #treshold1type + value
        im1_dilation = cv2.erode(im1_threshold1, kernel=self.dilationkernel, iterations=1)
        self.im1_blur = cv2.blur(im1_dilation, (self.blursize, self.blursize))
        x, self.im1_threshold2 = cv2.threshold(self.im1_blur, int(self.threshold2val), 255, cv2.THRESH_BINARY)                                    #threshold2type
        largest_contour = self.find_largest_contours(self.im1_threshold2)
        self.scaled_contour = self.calc_scale_contour(largest_contour, self.lineartrans)
        self.img_contour = cv2.drawContours(self.imageset[0].copy(), self.scaled_contour.copy(), -1, 255, 10, offset=(-1, -1))

    def calc_imgcalc(self):
        imgmorph = cv2.morphologyEx(self.imageset[-1], cv2.MORPH_TOPHAT, self.morphexkernel, 1)
        x, self.img_calc = cv2.threshold(imgmorph, int(self.threshold3val), 255, cv2.THRESH_BINARY_INV)                            #threshold3type

    def calc_mig(self, filepath = None, scaled = True):
        mask = np.zeros(self.imageset[0].shape, np.uint8)
        self.mask = cv2.fillPoly(mask, [self.scaled_contour], 255)

        self.scratcharea = np.count_nonzero(mask)

        self.backgroundarea = np.shape(self.imageset[0])[0] * np.shape(self.imageset[0])[1] - self.scratcharea
        self.migprogresslist = list()
        self.im_thresh_scratch_list = list()
        self.im_maskedscratch_list = list()
        self.im_maskedbackground_list = list()
        #print(self.scratcharea)
        #print(np.shape(self.imageset[0])[0] * np.shape(self.imageset[0])[1])
        if not (0.1 < (self.scratcharea)/(np.shape(self.imageset[0])[0] * np.shape(self.imageset[0])[1]) < 0.5):
            print("ERROR in Scratch-Detection")
            self.migprogresslist.append("ERROR")
            return


        for index, image in enumerate(self.imageset):
            im_morph = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, self.morphexkernel, 1)
            im_maskedscratch = im_morph.copy()
            im_maskedscratch[self.mask == 0] = 255
            self.im_maskedscratch = im_maskedscratch
            self.im_maskedscratch_list.append(self.im_maskedscratch)
            self.im_maskedbackground = im_morph.copy()
            self.im_maskedbackground[self.mask == 255] = 255
            self.im_maskedbackground_list.append(self.im_maskedbackground)
            x, self.im_thresh_scratch = cv2.threshold(self.im_maskedscratch, int(self.threshold3val), 255, cv2.THRESH_BINARY_INV)                 #threshold3type
            self.im_thresh_scratch_list.append(self.im_thresh_scratch)
            x, im_thresh_background = cv2.threshold(self.im_maskedbackground, int(self.threshold3val), 255, cv2.THRESH_BINARY_INV)           #threshold3type
            noncellscratcharea = np.count_nonzero(self.im_thresh_scratch)

            noncellbackgroundarea = np.count_nonzero(im_thresh_background)
            backgrounddens = (self.backgroundarea - noncellbackgroundarea) / self.backgroundarea
            if index == 0:
                self.backgrounddens_0 = backgrounddens
            scratchdens = (self.scratcharea - noncellscratcharea) / self.scratcharea
            if scaled is True:
                migprogress = (scratchdens / self.backgrounddens_0) * 100
            else:
                migprogress = scratchdens * 100
            self.migprogresslist.append(migprogress)

        if filepath != None:
            if not os.path.exists(filepath + "/" + "results"):
                os.mkdir(filepath + "/" + "results")
            np.savetxt(filepath + "/" + "results" + "/" + "migprogress_" + str(list(self.dict)[0]) + ".csv", [self.migprogresslist], delimiter=',', fmt='%f')
            cv2.imwrite(filepath + "/" + "results" + "str(list(self.dict)[0])" + "scratch_detect.png", self.img_contour)


    def plot_migprogress(self,plotlist, size, title, length_default=None):
        fig = plt.figure(figsize=size, dpi=100)
        new_plot = fig.add_subplot(111)
        if length_default != None:
            plt.xlim(0, length_default)
            plt.ylim(0, math.ceil(sorted(self.migprogresslist)[-1]/10) * 10)
            x = list(range(1, len(plotlist) + 2))
            new_plot.plot(list(range(1, len(plotlist) + 1)), plotlist, 'bo-')
        else:
            new_plot.plot(list(range(1, len(plotlist) + 1)), plotlist, 'bo-')
        plt.xlabel("TIME")
        plt.ylabel("%")
        plt.title(title)
        # fig.plot()
        io_buf = io.BytesIO()
        plt.savefig(io_buf, format='raw')
        io_buf.seek(0)
        img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                             newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
        img_arr = cv2.cvtColor(np.uint8(img_arr), cv2.COLOR_BGRA2BGR)
        io_buf.close()
        plt.close()
        self.plotarray = img_arr

    def plot_result(self,plotlist, size, title, length_default=None):
        fig = plt.figure(figsize=size, dpi=100)
        new_plot = fig.add_subplot(111)
        if length_default != None:
            plt.xlim(0, length_default)
            plt.ylim(0, math.ceil(sorted(self.migprogresslist)[-1]/10) * 10)
            x = list(range(1, len(plotlist) + 2))
            for plot in plotlist:
                new_plot.plot(list(range(1, len(plot[1:]) + 1)), plot[1:], 'o-', label = str(plot[0]))
        else:
            for plot in plotlist:
                new_plot.plot(list(range(1, len(plot[1:]) + 1)), plot[1:], 'o-', label = str(plot[0]))
        plt.xlabel("TIME")
        plt.ylabel("%")
        plt.legend()
        plt.title(title)
        # fig.plot()
        io_buf = io.BytesIO()
        plt.savefig(io_buf, format='raw')
        io_buf.seek(0)
        img_arr = np.reshape(np.frombuffer(io_buf.getvalue(), dtype=np.uint8),
                             newshape=(int(fig.bbox.bounds[3]), int(fig.bbox.bounds[2]), -1))
        img_arr = cv2.cvtColor(np.uint8(img_arr), cv2.COLOR_BGRA2BGR)
        io_buf.close()
        plt.close()
        self.plotarray = img_arr


    def gen_gif(self):
        self.im_cell_colored_list = list()
        for index, img in enumerate(self.imageset.copy()):
            img_contour = cv2.drawContours(img.copy(), self.scaled_contour.copy(), -1, 255, 10, offset=(-1, -1))
            cells = 255 - self.im_thresh_scratch_list[index].copy()
            cells[self.mask == 0] = 0

            #cells[self.im_maskedscratch[0] == 0] = 0
            image2 = cv2.cvtColor(img_contour, cv2.COLOR_GRAY2BGR)
            overlay = np.zeros(shape=image2.shape,dtype=np.uint8)
            overlay[cells != 0, 2] = 255
            overlay[cells != 0, 0:2] = 0
            combined = cv2.addWeighted(image2,1,overlay,1,0)
            self.im_cell_colored_list.append(combined)

    def save_gif(self):
        self.gif_list = list()
        for index, image in enumerate(self.im_cell_colored_list):
            self.plot_migprogress(self.migprogresslist[:index + 1], size=(10, 10), title="MIGRATION PROGRESS",
                                             length_default=len(self.im_cell_colored_list) + 1)
            resizey = self.plotarray[index].shape[0] / image.shape[0]
            resizex = resizey
            image = cv2.resize(image, None, fx=resizex, fy=resizey, interpolation=cv2.INTER_AREA)
            image3 = np.hstack((image, self.plotarray))
            self.gif_list.append(image3)
            imageio.mimsave(self.datapath + "/" + "migrationprogress" + str(list(self.dict)[0]) + ".gif", self.gif_list, duration=1)
