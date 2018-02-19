#!/usr/bin/env python3
# coding: utf8
"""
Ce fichier  est destiné à obtenir des trames nmea à partir d'un recepteur
GPS.
"""
import sys

from serial import Serial
from time import time


def acquisition(t_acq):
    """
    Connection au GPS et acquisition des trames nmea.
    """
    # Connection au GPS à l'address 
    gps = Serial('/dev/ttyUSB0', 4800)
    
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
        else:
            i += 1
    
    lines = acquisition(t_acq)
    with open(out, 'w') as f:
        for line in lines:
            f.write(line + '\n')
