#! /usr/bin/python3
# coding:utf8

import matplotlib.pyplot as plt
import numpy as np
from random import random

def moyenne(donnees):
    '''Renvoie la moyenne d'une liste de données

    Entrées
    -------
    donnees (liste)

    Sortie
    ------
    moyenne (int)
    '''

    return sum(donnees)/len(donnees)

def ecart_type(donnees):
    '''Renvoie l'écart-type d'une liste de données

    Entrées
    -------
    donnees (liste)

    Sortie
    ------
    ecart-type (int)
    '''


    somme = 0
    moy = moyenne(donnees)

    for donnee in donnees:
        somme += (donnee-moy)**2

    return (1/len(donnees)*somme)**0.5


gauss = lambda x, sig, mu : 1/(sig*(2*np.pi)**0.5)*np.exp(-(x-mu)**2/(2*sig)**2)


if __name__ == '__main__' :
    
    n = 100
    liste_test1 = [random() for k in range(n)]
    liste_test2 = [random() for k in range(n)]
    trace_stat([liste_test1, liste_test2])
