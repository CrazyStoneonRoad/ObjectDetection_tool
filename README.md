# ObjectDetection_tool
Tool kits of object detection.



## avr_std_detection_sets.py
### Usage
Put this file under root of a dataset. 
For example, like '~/DATA/VOCdevkit/voc2007/', while the file tree is like:

    voc2007
      |--------JPEGImages
      |           |------- *.jpg
      |--------others1
      |--------others2
      
### Function
This file samples N images to count average and standard deviation of the datset. 

Change: N denotes the number of randomly selected images. You can change N to control the sample numbers.

Outputs: Print two lists of 1x3, correspond to average/std and three channels of RGB.

## voc_formatting.py
### Usage
Put this file under '~/DATA/DOTA', while the file tree is like:

    DOTA
      |--------train
      |         |------- images
      |         |------- labelTxt
      |--------test
      |         |------- images
      |         |------- labelTxt
      |--------val
      |         |------- images
      |         |------- labelTxt

### Function
This file is to convert DOTA dataset with 8 coordinate parameters into VOC-format annotations.

Output:  '~/DATA/DOTA/DOTA-voc', while the file tree is like:

    DOTA
      |--------JPEGImages
      |--------Annotations
      |         |------- *.xml
      |--------ImageSets
      |         |------- train.txt
      |         |------- val.txt
      
Note: JPEGImages will be empty, need mannually soft link or copy images into this folder.
