#! /usr/bin/env python
from osgeo import gdal
import pyproj
import sys

import matplotlib.pyplot as plt
import numpy as np
import pynmea2 as nmea


class Satellite:
    def __init__(self, prn):
        self.prn = prn
        self.elevation = []
        self.azimuth = []
    
    def add_pos(self, elevation, azimuth):
        self.elevation.append(elevation)
        self.azimuth.append(azimuth)
    
    def get_azimuth(self):
        return self.azimuth
    
    def get_elevation(self):
        return self.elevation
    
    def get_prn(self):
        return self.prn


def dmstodd(degre):
    d = int(degre/100)
    m = degre - d*100
    return d + m/60

def traitement(msgs):
    trames = []
    for msg in msgs:
        try:
            trame = nmea.parse(msg)
            trames.append(trame)
        except:
            pass

    long = []
    lat = []
    
    satellites = dict()   

    # Lecture des donnees
    for trame in trames:
        if trame.sentence_type == 'GGA' and trame.is_valid:
            long.append(float(trame.lon))
            lat.append(float(trame.lat))

        if trame.sentence_type == 'GSV':
            if len(trame.sv_prn_num_1) > 0:
                prn = trame.sv_prn_num_1 #dictionnaire prn
                if prn in satellites.keys():
                    satellite = satellites[prn]
                    
                else:
                    satellite = Satellite(prn)
                elevation = trame.elevation_deg_1
                azimuth = trame.azimuth_1
                satellite.add_pos(elevation, azimuth)
                satellites[prn] = satellite
                
            if len(trame.sv_prn_num_2) > 0:
                prn = trame.sv_prn_num_2
                if prn in satellites.keys():
                    satellite = satellites[prn]
                    
                else:
                    satellite = Satellite(prn)
                elevation = trame.elevation_deg_2
                azimuth = trame.azimuth_2
                satellite.add_pos(elevation, azimuth)
                satellites[prn] = satellite
            
            if len(trame.sv_prn_num_3) > 0:
                prn = trame.sv_prn_num_3
                if prn in satellites.keys():
                    satellite = satellites[prn]
                    
                else:
                    satellite = Satellite(prn)
                elevation = trame.elevation_deg_3
                azimuth = trame.azimuth_3
                satellite.add_pos(elevation, azimuth)
                satellites[prn] = satellite
            
            if len(trame.sv_prn_num_4) > 0:
                prn = trame.sv_prn_num_4
                if prn in satellites.keys():
                    satellite = satellites[prn]
                    
                else:
                    satellite = Satellite(prn)
                elevation = trame.elevation_deg_4
                azimuth = trame.azimuth_4
                satellite.add_pos(elevation, azimuth)
                satellites[prn] = satellite
    
    
    # Affichage des donnees

    # Affichage sur une carte
    im = gdal.Open('res/ensta_2015.jpg')
    nx = im.RasterXSize
    ny =  im.RasterYSize
    nb = im.RasterCount
    image = np.zeros((ny,nx,nb))
    image[:,:,0]=im.GetRasterBand(1).ReadAsArray()*255
    image[:,:,1]=im.GetRasterBand(2).ReadAsArray()*255
    image[:,:,2]=im.GetRasterBand(3).ReadAsArray()*255
    plt.figure()
    plt.xlim([500,1000])
    plt.ylim([1200,800])
    
    # origin_x et origin_y sont dans le format lambert 93
    origin_x, pixel_width, _, origin_y, _, pixel_height = im.GetGeoTransform()

    wgs84 = pyproj.Proj(init='epsg:4326')
    lambert = pyproj.Proj(init='epsg:2154')

    # Conversion en degrés décimaux
    long = [-dmstodd(x) for x in long]
    lat = [dmstodd(x) for x in lat]

    lx, ly = pyproj.transform(wgs84, lambert, long,
                              lat)

    lx = np.array(lx)
    ly = np.array(ly)

    # Conversion en coordonnées sur l'image
    x = (lx - origin_x) / pixel_width
    y = (ly - origin_y) / pixel_height
    plt.imshow(image)
    plt.scatter(x, y)

    plt.show()

    
if __name__=='__main__':
    file = 'data/data_uv24.nmea'
    
    i = 0
    n = len(sys.argv)
    while i < n:
        if sys.argv[i] == '-i':
            file = sys.argv[i+1]
            i +=2
        else:
            i += 1
    
    
    with open(file, 'r')as f:
        msgs = f.readlines()
    
    traitement(msgs)
