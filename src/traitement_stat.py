#! /usr/bin/python3
# coding:utf8

import matplotlib.pyplot as plt
import numpy as np
from random import random

def moyenne(donnees):
    return sum(donnees)/len(donnees)

def ecart_type(donnees):
    
    somme = 0
    moy = moyenne(donnees)

    for donnee in donnees:
        somme += (donnee-moy)**2

    return (1/len(donnees)*somme)**0.5


gauss = lambda x, sig, mu : 1/(sig*(2*np.pi)**0.5)*np.exp(-(x-mu)**2/(2*sig)**2)

def trace_stat(donnees):
    '''Trace les donnees en entrée avec leur moyenne et la courbe de Gauss
    correspondante à cette moyenne et à l'écart-type

    Entrées
    -------
    donnees (liste de liste) : contient les listes de chaque type de donnée à
    traiter

    Sortie
    ------
    figures
    '''

    for liste in donnees:
        moy = moyenne(liste)
        ecart = ecart_type(liste)

        plt.figure()
        plt.plot(liste,[0]*len(liste),'b')
        plt.plot([moy],[0],'r', marker='o', markersize=7)
        
        ordonnees = np.linspace(min(liste), max(liste), 100)
        plt.plot(ordonnees, gauss(ordonnees, ecart, moy))

if __name__ == '__main__' :
    
    n = 100
    liste_test1 = [random() for k in range(n)]
    liste_test2 = [random() for k in range(n)]
    trace_stat([liste_test1, liste_test2])
    
    plt.show()
