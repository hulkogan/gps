#! /usr/bin/env python
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
