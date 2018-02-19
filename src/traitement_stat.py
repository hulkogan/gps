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

    plt.style.use('classic')

    for liste in donnees:
        moy = moyenne(liste)
        ecart = ecart_type(liste)

        plt.figure()
        
        ordonnees = np.linspace(min(liste), max(liste), 100)
        courbe_normale = gauss(ordonnees, ecart, moy)

        mini = min(courbe_normale)
        maxi = max(courbe_normale)

        #Cadrage des données pour que tout soit visible notamment la légende
        plt.ylim(mini - (maxi - mini) * 0.1, maxi + (maxi - mini) * 0.5)

        #traçage de la courbe de gauss
        plt.plot(ordonnees, courbe_normale, 'k', label = 'Loi normale correspondante')


        #traçage des données avec comme abscisse le min de la courbe de Gauss
        plt.plot(liste,[mini]*len(liste),'b', label = 'Données')
        #traçage du point correspondant à la moyenne en rouge
        plt.plot([moy],[mini],'r', marker='o', markersize=5, label = 'Moyenne des données')
        
        #traçage des verticales correspondants à moyenne +/- ecart_type
        plt.plot([moy-ecart, moy-ecart],[mini, maxi], 'g', label = 'Moyenne $\pm$ écart-type')
        plt.plot([moy+ecart, moy+ecart],[mini, maxi], 'g')

        #Affichage de la légende
        plt.legend(loc = 'upper right')

        plt.show()


if __name__ == '__main__' :
    
    n = 100
    liste_test1 = [random() for k in range(n)]
    liste_test2 = [random() for k in range(n)]
    trace_stat([liste_test1, liste_test2])
