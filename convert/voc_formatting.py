import xml.etree.ElementTree as ET
import os
from os import getcwd
import pathlib
import subprocess
from PIL import Image
#from os import listdir
#import pickle
#from os.path import join

#
sets=['train', 'val'] # 'test' labels are unavailable for equility of competition
classes = ['large-vehicle', 'swimming-pool', 'helicopter', 'bridge',
           'plane', 'ship', 'soccer-ball-field', 'basketball-field',
           'ground-track-field', 'small-vehicle', 'harbor', 'baseball-diamond',
           'tennis-court', 'roundabout', 'storage-tank']




#
def convert(size, box):
    ## TODO: converted to (x,y,w,h)
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def max_box(box):
    ## TODO: converted to (x1,x2,y1,y2)
    x_s = box[0:8:2]
    y_s = box[1:8:2]
    x1,x2,y1,y2 = ( min(x_s),max(x_s),min(y_s),max(y_s) )
    return (x1,x2,y1,y2)

#
def convert_annotation( img_id, pth_imgs, pth_lbtxt, pth_antsn ):
    ## TODO: convert label files. pth_lbtxt is the DOTA labels path.
    ## labelTxt is "x1, y1, x2, y2, x3, y3, x4, y4, category, difficult"
    ## convert to VOC-formated xml files

    pth_in = '{}/{}.txt'.format(pth_lbtxt, img_id[:-4])
    pth_ot = '{}/{}.xml'.format(pth_antsn, img_id[:-4])
    pth_im = '{}/{}.png'.format(pth_imgs, img_id[:-4])

    img = Image.open(pth_im)
    w,h = img.size

    # start xml
    name = img_id
    root = ET.Element('annotation')
    filename = ET.SubElement(root, 'filename')
    filename.text = name
    source = ET.SubElement(root, 'source')
    source.text = 'DOTA'
    size = ET.SubElement(root, 'size')
    width = ET.SubElement(size, 'width')
    width.text = '%d'%w
    height = ET.SubElement(size, 'height')
    height.text = '%d'%h
    depth = ET.SubElement(size, 'depth')
    depth.text = '%d'%3
    segmented = ET.SubElement(root, 'segmented')
    segmented.text = '0'

    # deal boxes / objects
    with open(pth_in, 'r') as fp:
        for ln in fp.readlines():
            if ln[:3] in ['ima', 'gsd']:
                continue
            else:
                infos = ln.strip().split()
                box_8 = [int(i) for i in infos[0:8]]
                box_4 = max_box(box_8)

                # box_voc = convert(img.size, box_4)
                box_voc = box_4
                category = infos[8]
                diff = infos[9]

                # xml object
                object = ET.SubElement(root, 'object')
                name = ET.SubElement(object, 'name')
                name.text = category
                pose = ET.SubElement(object, 'pose')
                pose.text = 'Unspecified'
                difficult = ET.SubElement(object, 'difficult')
                difficult.text = diff
                bndbox = ET.SubElement(object, 'bndbox')
                xmin = ET.SubElement(bndbox, 'xmin')
                xmin.text = '%d'%box_voc[0]
                ymin = ET.SubElement(bndbox, 'ymin')
                ymin.text = '%d'%box_voc[2]
                xmax = ET.SubElement(bndbox, 'xmax')
                xmax.text = '%d'%box_voc[1]
                ymax = ET.SubElement(bndbox, 'ymax')
                ymax.text = '%d'%box_voc[3]

    w=ET.ElementTree(root)
    w.write(pth_ot,'utf-8',True)

    # in_file = open('%s/%s.xml'%(image_id))
    # out_file = open('VOCdevkit/labels/%s.txt'%(image_id), 'w')
    # tree = ET.parse(in_file)
    # root = tree.getroot()
    # size = root.find('size')
    # w = int(size.find('width').text)
    # h = int(size.find('height').text)
    #
    # for obj in root.iter('object'):
    #     difficult = obj.find('difficult').text
    #     cls = obj.find('name').text
    #     if cls not in classes or int(difficult) == 1:
    #         continue
    #     cls_id = classes.index(cls)
    #     xmlbox = obj.find('bndbox')
    #     b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
    #     bb = convert((w,h), b)
    #     out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


#
wd = getcwd()

# dealing each set
for image_set in sets:
    # prepare
    paths__ = ['DOTA-voc/Annotations',
               'DOTA-voc/JPEGImages',
               'DOTA-voc/ImageSets',
               'DOTA-voc/ImageSets/Main' ]
    for pth in paths__:
        pathlib.Path(pth).mkdir(parents=True, exist_ok=True)

    # write ImageSets
    pth_imgs = os.path.join(image_set,'images')
    lst_imgs = os.listdir( pth_imgs )
    imgst_file = '{}/{}.txt'.format(paths__[3],image_set)
    with  open(imgst_file, 'w') as fp:
        # because of deleting elements, use inverted sequence
        i = len(lst_imgs)
        for img_id in lst_imgs[::-1]:
            if img_id[-3:] in ['jpg', 'png', 'tif']:
                # write
                fp.write( '{}\n'.format(img_id[:-4]) )
            else:
                # delete
                del lst_imgs[i]
            i = i-1

    # write JPEGImages    PLEASE DO THIS BY HAND !!!!!!!!!!!!!!!!!!!
    # fr__ = os.path.dirname(os.path.abspath( os.path.join(image_set,'images','*') ))
    # to__ = os.path.dirname(os.path.abspath( paths__[1] ))
    # subprocess.run('ln -sf {} {}'.format(fr__, to__))

    # convert labels.txt to annotations.xml
    for img_id in lst_imgs:
        # img_id, pth_imgs, pth_lbtxt, pth_antsn
        pth_imgs = os.path.join(image_set,'images') # '{}/images'.format(image_set, img_id)
        pth_lbtxt = os.path.join(image_set,'labelTxt') # '{}/labelTxt'.format(image_set, img_id)
        pth_antsn = paths__[0]
        convert_annotation(img_id, pth_imgs, pth_lbtxt, pth_antsn )






        #
    # # get images in 'val' or 'train'
    #     image_ids = open('VOCdevkit/ImageSets/%s.txt'%image_set).read().strip().split() # ids
    # list_file = open('%s.txt'%(image_set), 'w') # open val.txt or train.txt
    #
    # # dealing each image
    # for image_id in image_ids:
    #     # writing val.txt or train.txt
    #     list_file.write('%s/positive_images/%s.jpg\n'%(wd, image_id))
    #     # convert labels to annotations
    #     convert_annotation(image_id)
    # list_file.close()

