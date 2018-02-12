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

    temps = None
    
    satellites = dict()    

    satellite_a = dict()    

    # Lecture des donnees
    for trame in trames:
        if trame.sentence_type == 'GGA' and trame.is_valid:
            long.append(float(trame.lon))
            lat.append(float(trame.lat))
            temps = trame.timestamp

        if trame.sentence_type == 'GSA':
            temps_str=str(temps.hour)+':'+str(temps.minute)+':'+str(temps.second)
            satellite_a[temps_str]=[]
            
            if trame.sv_id01!='':
                satellite_a[temps_str].append(int(trame.sv_id01))

            if trame.sv_id02!='':
                satellite_a[temps_str].append(int(trame.sv_id02))
                
            if trame.sv_id03!='':
                satellite_a[temps_str].append(int(trame.sv_id03))
                
            if trame.sv_id04!='':
                satellite_a[temps_str].append(int(trame.sv_id04))
                
            if trame.sv_id05!='':
                satellite_a[temps_str].append(int(trame.sv_id05))

            if trame.sv_id06!='':
                satellite_a[temps_str].append(int(trame.sv_id06))
                
            if trame.sv_id07!='':
                satellite_a[temps_str].append(int(trame.sv_id07))
  
            if trame.sv_id08!='':
                satellite_a[temps_str].append(int(trame.sv_id08))
                
            if trame.sv_id09!='':
                satellite_a[temps_str].append(int(trame.sv_id09))
                
            if trame.sv_id10!='':
                satellite_a[temps_str].append(int(trame.sv_id10))  
                
            if trame.sv_id11!='':
                satellite_a[temps_str].append(int(trame.sv_id11))  
                
            if trame.sv_id12!='':
                satellite_a[temps_str].append(int(trame.sv_id12))        

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

    #  Affichage des satellites actifs en fonction du temps
    x=list(satellite_a.keys())
    y=list(satellite_a.values())
    x=[[x[j] for i in range(len(y[j]))] for j in range(len(x))]
    plt.figure()
    axes=plt.gca()
    for i in range(len(x)):
        plt.scatter(x[i],y[i],c='g')
    axes.set_xticks([x[15*i][0] for i in range(len(x)//15)])
    axes.set_yticks([i for i in range(1,33)])
    plt.xlabel('Heure',Fontsize=20,FontWeight='bold') ## ZULU OU AUTRE?
    plt.ylabel('Satellite numéro',Fontsize=20,FontWeight='bold')
    plt.title('SATELLITES ACTIFS EN FONCTION DU TEMPS', Fontsize='30', FontWeight='bold',Color='r')

    plt.figure()
    plt.scatter(long, lat)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid()
    
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], polar=True)
    
    # elevation
#    ax.set_rmin(0)
#    ax.set_rmax(90)
    
    
    #azimuth
    # Regler axes r
    ax.set_thetamin(0)
    ax.set_thetamax(360)
    ax.set_theta_zero_location('N')
   
    for prn, sat in satellites.items():
        elevation = sat.get_elevation()
        azimuth = sat.get_azimuth()
        
        plt.plot(azimuth, elevation)

    im = gdal.Open('res/ensta_2015.jpg')
    nx = im.RasterXSize
    ny =  im.RasterYSize
    nb = im.RasterCount
    image = np.zeros((ny,nx,nb))
    image[:,:,0]=im.GetRasterBand(1).ReadAsArray()*255
    image[:,:,1]=im.GetRasterBand(2).ReadAsArray()*255
    image[:,:,2]=im.GetRasterBand(3).ReadAsArray()*255
    plt.figure()
    #plt.xlim([500,1000])
    #plt.ylim([1200,800])
    
    # origin_x et origin_y sont dans le format lambert 93
    origin_x, pixel_width, _, origin_y, _, pixel_height = im.GetGeoTransform()

    wgs84 = pyproj.Proj('+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs')
    lambert = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')

    lx, ly = pyproj.transform(wgs84, lambert, long,
                              lat)

    lx = np.array(lx)
    ly = np.array(ly)

    x = (lx - origin_x) / pixel_width
    y = (ly - origin_y) / pixel_height
    plt.imshow(image)
    plt.scatter(x, y)
    

    print(lx[0], origin_x)
    plt.show()

    
if __name__=='__main__':
    file = 'data'
    
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
