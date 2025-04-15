#
# author rahulk
# complex networks
#

"""
count_worms.py

Description: This script counts worms form the images in png format.
Author: RK Verma
Date: 2023-10-1
"""

import imageio.v2 as iio
import numpy as np
import matplotlib.pyplot as plt
import skimage.color
import skimage.filters
from skimage.morphology import skeletonize
import os
import glob
import scipy

plt.interactive(False)


treat = '2Parent'                                           #for folders with different treatments
folder_path = '/image_folder/'

def count_worms(treat):
    fw = open(folder_path+treat+'.dat', 'w')                    # storing the number of worms
    G = []                                                      # glowing worms
    NG = []                                                     # non-glowing worms
    number_worms = []
    for images in glob.glob(folder_path+'*.png'):
        if images.endswith("*.png"):
            wormimage = iio.imread(images)
        parts = 1                                                      # number of parts to divide the image into
        M = wormimage.shape[0] // parts
        N = wormimage.shape[1] // parts
        tiles = [wormimage[x:x + M, y:y + N] for x in range(0, wormimage.shape[0], M) for y in
                 range(0, wormimage.shape[1], N)]
        for subimage in tiles:
            gray_image = skimage.color.rgb2gray(subimage)
            gray_worm = skimage.util.img_as_float(gray_image)          # to get the values in the range 0, 1
            nimage = skimage.feature.canny(gray_worm, sigma=1.6, mode='nearest')              # detect object edges
            blurred_image = skimage.filters.gaussian(nimage, sigma=0.9)       # blurring the object shapes
            filled = scipy.ndimage.binary_fill_holes(blurred_image)           # filling the object edge boundaries

            # remove small objects from the image
            cleaned = skimage.morphology.remove_small_objects(filled, min_size=350, connectivity=2)
            cleaned = skimage.morphology.remove_small_holes(cleaned, connectivity=2)
            

            labeled_worm, count = skimage.measure.label(cleaned, return_num=True, connectivity=2)
            fw.write(images.replace(folder_path, '')+'\t'+ str(count) +'\n')
            number_worms.append(count)
            for i in range(1, 12):                                            # these numbers are the total images and treatments (eg: 4_11_2_NG: 4=treatment, 11=Replicate, 2=image_num, NG/G)
                for j in range(1,3):
                    name = images.replace(folder_path, '').split('_')
                    if str(i) == name[0] and str(j) == name[1] and 'G.png' == name[2]:   
                        G.append((name[0:2], count))
                    elif str(i) == name[0] and str(j) == name[1] and 'NG.png' == name[2]:   
                        NG.append((name[0:2], count))
    fw.close()
    retrun G, NG



gfp = []
ngfp = []
sorted_G = sorted(count_worms[0], key=lambda i:(int(i[0][0]), int(i[0][1])))   
sorted_NG = sorted(count_worms[1], key=lambda i:(int(i[0][0]), int(i[0][1])))
def count_stats(sorted_G, sorted_NG):
    fw_stats = open(folder_path+treat+'_stats.dat', 'w')        # storing the stats of worm count
    sum_G = []
    sum_NG = []
    for kk in range(0, len(sorted_G)-1):
        if sorted_G[kk][0][0] == sorted_G[kk+1][0][0]:        #  sorted_G[kk][0][0] == sorted_G[kk+1][0][0]
            sum_G.append((sorted_G[kk][0][0:2], sorted_G[kk][1]+sorted_G[kk+1][1]))
        else:
            pass

    for pp in range(0, len(sorted_NG)-1):
        if sorted_NG[pp][0][0] == sorted_NG[pp + 1][0][0]:    # sorted_NG[pp][0][0:2] == sorted_NG[pp + 1][0][0:2]:
            sum_NG.append((sorted_NG[pp][0][0:2], sorted_NG[pp][1]+sorted_NG[pp+1][1]))
        else:
            pass

    for l in sum_NG:
        for m in sum_G:
            if l[0] == m[0]:
                try:
                    rel_fitness = (l[1]-m[1])/l[1]
                except:
                    ZeroDivisionError
                ngfp.append((l[0][0], l[1], m[1], l[1]-m[1], rel_fitness))      #for parent l[0], and others l[0] and l[1]

    for k in ngfp:
        fw_stats.write(str(k[0])+'\t'+str(k[1])+'\t'+str(k[2])+'\t'+str(k[3])+'\t'+str(k[4])+'\n')    # +'\t'+str(k[5])
    fw_stats.close()

    
os.system('say "Your code is finished" ')

