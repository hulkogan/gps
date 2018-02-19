#! /usr/bin/env python3
# coding: utf8
"""
Ce fichier contient les classes et fonctions nécessaires au traitement
de trames nmea.
"""
from osgeo import gdal
import pyproj
import sys

import matplotlib.pyplot as plt
import numpy as np
import pynmea2 as nmea


class Satellite:
    """
    Représentation d'un satellite.
    """
    def __init__(self, prn):
        """
        Creer un satellite en l'identifiant par son prn.
        """
        self.prn = prn
        self.elevation = []
        self.azimuth = []
    
    def add_pos(self, elevation, azimuth):
        """
        Ajoute une nouvelle position du satellite au format elevation/azimuth.
        """
        self.elevation.append(elevation)
        self.azimuth.append(azimuth)
    
    def get_azimuth(self):
        """
        Renvoie la liste des azimuths.
        """
        return self.azimuth
    
    def get_elevation(self):
        """
        Renvoie la liste des élévations.
        """
        return self.elevation
    
    def get_prn(self):
        """
        Renvoie le prn.
        """
        return self.prn


def dmtodd(degre):
    """
    Converti une longitude/lattitude du format degré°minute vers le format
    degré décimal.
    """
    # Récupération des degrées
    d = int(degre/100)
    # Récupération des minutes en décimal
    m = degre - d*100
    # Conversion des minutes en minutes d'angles
    return d + m/60

def traitement(msgs):
    """
    Fonction principale qui traite les trames nmea et affiches les graphiques.
    """
    trames = []
    for msg in msgs:
        try:
            trame = nmea.parse(msg)
            trames.append(trame)
        except:
            pass

    # Stockage de la longitude et lattitude du récepteur.
    long = []
    lat = []

    # temps suit l'heure de reception des trames
    temps = None
    
    # Stockage des satellites
    satellites = dict()

    # Stockage de la disponnibilité des sattelites
    satellite_a = dict()

    # Lecture des donnees
    for trame in trames:
        # Traitement des trames GGA
        if trame.sentence_type == 'GGA' and trame.is_valid:
            long.append(float(trame.lon))
            lat.append(float(trame.lat))
            temps = trame.timestamp    

        # Traitement des trames GSA
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

        # Traitement des trames GSV
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

    # Conversion en degrés décimaux
    long = [-dmtodd(x) for x in long]
    lat = [dmtodd(x) for x in lat]

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

    lx, ly = pyproj.transform(wgs84, lambert, long,
                              lat)

    lx = np.array(lx)
    ly = np.array(ly)

    # Conversion en coordonnées sur l'image
    x = (lx - origin_x) / pixel_width
    y = (ly - origin_y) / pixel_height
    plt.imshow(image)
    plt.scatter(x, y)

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
