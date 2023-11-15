# Cell Migration Tool (under development)

`CellMigrationTool` is a Python tool that provides an Interface for Cell migration quantification for high throughput microscopy. It was developed as part of the publication "Automated high-throughput live cell monitoring of endothelial cell migration" (Schmidt, Lerm et al.). 

![](https://github.com/DomiLerm/CellMigrationTool/blob/master/test_imgs/high_migration/RFP/migrationprogressB2.gif)

# Installation

To run the Cell Migration Tool download and install the following dependencies:

```
pip install --upgrade Pillow
pip install --upgrade opencv-python
pip install --upgrade numpy
pip install --upgrade matplotlib
pip install --upgrade imageio
pip install --upgrade natsort
```

Download the the github-repo and run gui.py

# General information

The general tool functionality is summarized in the corresponding publication. You can use the tool to quantify single migration timelines (including the generation of .gifs as showcased) or batch-analyse a whole dataset of timelines.

An overview of the different parameters utilized by the application for scratch-detection and migration calculation are shown below. 

|          |     Parameter            |     Function                                                                                                                                                                                                                                           |
|----------|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|     1    |     Top-hat-kernel       |     Sets   the kernel size for the top-hat transformation used in the image preprocessing module to correct uneven illumination.                                                                                                                       |
|     2    |     Dilation-Kernel      |     Sets   the kernel size for morphological operation dilation in the scratch detection module. The lower the cell density, or for Hoechst33342-stained cells, a larger kernel is necessary.                                                          |
|     3    |     Blurring-Kernel      |     Sets   the kernel size for smoothing after the dilation operation. The higher the value the more homogeneous the image content becomes, which leads to an improved thresholding but can also cause unwanted smoothing of the wound edges.          |
|     4    |     Threshold-Value      |     Sets   the threshold for the detection of the initial wounded area.                                                                                                                                                                                |
|     5    |     Linear-scaling       |     Sets   the factor with which the detected wound is scaled to counteract any shrinking of the region induced by the previous analysis steps.                                                                                                        |
|     6    |     Threshold   final    |     Sets the threshold for the detection of migrated cells in the wound area.      


# Data format

This tools expects a an exact data format and labeling. When preparing your dataset make sure to only use .tif images with an appropriate resolution. The folder to be analyzed can contain multiple timelines, however each image must start with a timeline identifier that is followed by an underscore and ends with the given image index. Since this tool was initial developed for RFP and DAPI stained migration assays the filename should include "DAPI" or "RFP", depending on the selected default parameters (e.g A1_-2_1_1_Tsf[Stitched[DAPI 377,447]]_001.tif).

The "test_imgs" folder contains 4 sample timelines that show you the expected naming of the images and can be used for testing.

# Contributing Citing

Please let us know if there is something that does not work, or needs to be changed or if you would like additional features. 

If `CellMigrationTool` contributes to a project that leads to a publication, please acknowledge this by citing the publication.
      