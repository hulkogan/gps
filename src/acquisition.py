#!/usr/bin/env python3
# coding: utf8
"""
Ce fichier  est destiné à obtenir des trames nmea à partir d'un recepteur
GPS.
"""
import sys

from serial import Serial
from time import time


def acquisition(t_acq, port, baudrate):
    """
    Connection au GPS et acquisition des trames nmea.
    Paramètres:
    -----------
    t_acq: temps d'acquisition
    port: port du gps
    baudrate: fréquence du gps
    """
    # Connection au GPS à l'address 
    gps = Serial(port, baudrate)
    
    lines = []
    
    t1 = time()
    t2 = time()
    while t2-t1<t_acq:
        try:
            lines.append(gps.readline().decode('ascii')[:-2])
        except:
            pass
        t2 = time()
    
    return lines


if __name__=='__main__':
    print("Acquisition...")
    
    t_acq = 10 # Temps d'acquisition
    out = 'data' # Nom du fichier de sorti
    port = None
    baudrate = None
    
    # Lecture des arguments
    # -t t_acq -o out
    i = 0
    n = len(sys.argv)
    while i < n:
        if sys.argv[i] == '-o':
            out = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == '-t':
            t_acq = int(sys.argv[i+1])
            i += 2
        elif sys.argv[i] == '--port':
            port = sys.argv[i+1]
            i += 2
        elif sys.argv[i] == '--baudrate':
            baudrate = int(sys.argv[i+1])
            i += 2
        else:
            i += 1
    
    lines = acquisition(t_acq, port, baudrate)
    with open(out, 'w') as f:
        for line in lines:
            f.write(line + '\n')
