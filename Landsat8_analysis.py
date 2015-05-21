# -*- coding: utf-8 -*-
"""
Created on Mon May  4 02:30:39 2015

@author: Margherita Di Leo

Instructions:
Set paths before running
"""

import os
from os import listdir
import csv
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt

#----------------------

global landsat_path, graphs_path, csv_filename, csv_output

#### Set paths here:
# Directory in which the landsat are stored
landsat_path = "/home/user/Projects/test_landsat8/landsat8" 
# Directory where you want to save the graphs
graphs_path = "/home/user/Projects/test_landsat8/graphs" 
# Name for CSV input file, with cat, ordn, x, y of points, path included
csv_filename = "/home/user/Projects/test_landsat8/utm_coord_with_id.csv"
# Name for CSV output file, path included
csv_output = "/home/user/Projects/test_landsat8/output.csv"

L = 0.2 # coefficient used for calculating SAVI index

#----------------------                               

class Point(object):
    '''The point has a cat, a ord identifier and coordinates x, y'''
    def __init__(self, cat, ordn, x, y, **kwargs):
        '''id is cat, ord is NUMERO_ORD'''
        self.cat = cat
        self.ordn = ordn
        self.X = x
        self.Y = y
        self.TS = np.asarray(self)
        
#----------------------

def readCSVfile(filename):
    '''reads cat, NUMERO_ORD, coordinates x and y from CSV file'''
    points = []
    with open(csv_filename, 'rb') as csvfile:
        for cat, ordn, x, y in csv.reader(csvfile, delimiter = ','):
            point = Point(int(cat), float(ordn), float(x), float(y))
            print point
            points.append(point)       
    print points
    csvfile.close()
    return points    
   
#----------------------
   
def getImageNames(landsat_path):
    '''lists all the raster files in a directory'''
    images = listdir(landsat_path)
    return images
    
#----------------------    

def getSignal(image, band, coordx, coordy):
    '''reads the value of the pixel in the point of given coordinates for one band in the image'''  
    try:
        bandValue = os.popen('gdallocationinfo -valonly -b %s -geoloc %s %s %s' % (band, 
                                                                            os.path.join(landsat_path, image), 
                                                                            coordx, 
                                                                            coordy)).read()
    except:
        bandValue = -9999
    return bandValue
    
#----------------------    
                                                                      
def getTimeSeries(images, coordx, coordy):  
    '''for each pairs of coordinates, gets the time series over Landsat images and 
    calculates NDVI and SAVI indexes'''
    TS = np.zeros((len(images), 5), float)
    
    for i in range(0, len(images)):
        print "i", i
        print "image", images[i]
        # get NIR
        TS[i, 0] = getSignal(images[i], 5, coordx, coordy)
        print "NIR ", TS[i, 0]
        # get RED
        TS[i, 1] = getSignal(images[i], 4, coordx, coordy)
        print "RED ", TS[i, 1]
        # get GREEN
        TS[i, 2] = getSignal(images[i], 3, coordx, coordy)
        print "GREEN ", TS[i, 2]
        # calculate NDVI
        TS[i, 3] = (TS[i,0] - TS[i,1])/(TS[i,0] + TS[i,1])
        print "NDVI ", TS[i, 3]
        # calculate SAVI
        TS[i, 4] = ((1 + L)*(TS[i,0] - TS[i,1]))/(TS[i,0] + TS[i,1] + L)
        print "SAVI ", TS[i, 4]
   
    print "TS", TS  
    return TS    
    
#----------------------  
    
def plotImage(cat, nir, red, green, ndvi, savi):
    os.chdir(graphs_path)
    # NIR
    plt.figure(1)
    plt.plot(nir, color = 'm') #magenta
    plt.ylim(0, 0.6)
    plt.title("NIR for point %s" % cat)
    plt.grid(True)
    #plt.show() # optional
    plt.savefig("point_%s_nir.jpeg" % cat)
    # RED
    plt.figure(2)
    plt.plot(red, color = 'r') #red
    plt.ylim(0, 0.6)
    plt.title("RED for point %s" % cat)
    plt.grid(True)    
    #plt.show() # optional
    plt.savefig("point_%s_red.jpeg" % cat)
    # GREEN
    plt.figure(3)
    plt.plot(green, color = 'g') #green
    plt.ylim(0, 0.6)
    plt.title("GREEN for point %s" % cat)
    plt.grid(True)    
    #plt.show() # optional
    plt.savefig("point_%s_green.jpeg" % cat)
    # NDVI
    plt.figure(4)
    plt.plot(ndvi, color = 'c') #cyan
    plt.ylim(0, 0.6)
    plt.title("NDVI for point %s" % cat)
    plt.grid(True)    
    #plt.show() # optional
    plt.savefig("point_%s_ndvi.jpeg" % cat)
    # SAVI
    plt.figure(5)
    plt.plot(savi, color = 'b') #blue
    plt.ylim(0, 0.6)
    plt.title("SAVI for point %s" % cat)
    plt.grid(True)    
    #plt.show() # optional
    plt.savefig("point_%s_savi.jpeg" % cat)
    plt.close('all')     
 
#----------------------  
 
def writeOutput(points):
    pass

#----------------------  
 
if __name__ == '__main__':

    points = readCSVfile(csv_filename)
    images = getImageNames(landsat_path)

    for i in range(0, len(points)):
        points[i].TS = getTimeSeries(images, points[i].X, points[i].Y)
        plotImage(points[i].cat, points[i].TS[:,0], points[i].TS[:,1],
                  points[i].TS[:,2], points[i].TS[:,3], points[i].TS[:,4])
    

    
    
    
    
    
    
