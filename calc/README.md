
## avr_std_detection_sets.py
- Usage
Put this file under root of a dataset. 

For example, like '~/DATA/VOCdevkit/voc2007/', while the file tree is like:

    voc2007
      |--------JPEGImages
      |           |------- *.jpg
      |           |------- *.jpg
      |           |------- *.jpg
      |           |------- *.jpg
      |           |------- *.jpg
      |--------others1
      |--------others2
      
- Function
This file samples N images to count average and standard deviation of the datset. 

N denotes the number of randomly selected images.

Print two lists of 1x3, correspond to average/std and three channels of RGB.
