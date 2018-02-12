#! /usr/bin/env python3
# coding: utf8
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
        plt.plot(x[i],y[i],'go')
    ab=np.linspace(0,len(x)-1,15)
    xlab=[x[int(i)][0] for i in ab]
    plt.xticks(ab,xlab)
    axes.set_yticks([i for i in range(1,33)])
    plt.xlabel('Heure',Fontsize=20,FontWeight='bold') ## ZULU OU AUTRE?
    plt.ylabel('Satellite numéro',Fontsize=20,FontWeight='bold')
    plt.title('SATELLITES ACTIFS EN FONCTION DU TEMPS',
              Fontsize='30', FontWeight='bold',Color='r')

    #Affichage de la position (long/lat)
    plt.figure()
    plt.scatter(long, lat)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid()

    # Affichage de la position des satellites
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], polar=True)

    # Reglage des axes
    ax.set_thetamin(0)
    ax.set_thetamax(360)
    ax.set_theta_zero_location('N')
   
    # Traitement des positions
    for prn, sat in satellites.items():
        elevations = sat.get_elevation()
        azimuths = sat.get_azimuth()

        # Conversion en radians
        elevations = [int(elevation)*np.pi/180 for elevation in elevations]
        azimuths = [int(azimuth)*np.pi/180 for azimuth in azimuths]
        
        plt.plot(azimuths, elevations)

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
