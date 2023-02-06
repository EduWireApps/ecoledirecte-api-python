# EduWire: Python Unofficial EcoleDirecteAPI 
*Cette API est en cours de developpement et n'est pas disponible via `pip`*

## Fonctionnalités:

 - classes Client, Eleve
 - methodes getRawNotes, getRawEmploiDuTemps

## Exemple
```python
compte = Eleve("identifiant","motdepasse")
print(compte.getEmploiDuTemps()) #renvoie l'emploi du temps d'aujourd'hui
print(compte.getRawNotes()) #renvoie le json complet de la commande
```