# Architecture générale / technos utilisées

L'application serait découpée de la manière suivante : 
- un front-end statique qui distribue une application SPA, développé en HTML / CSS / React.js
- un back-end qui expose une API REST (Python / Flask) et avec laquelle communique le front en HTTP. Il requête aussi une base de données SQLite.

# Modèle de données

Il est nécessaire d'associer un utilisateur à chaque billet réservé, mais nous
allons simplifier la chose au maximum : il n'y aura pas d'authentification, et
on suppose que les noms des clients sont uniques. On suppose aussi que les
billets ne sont pas liés à une date / heure. On se retrouve ainsi avec une
seule table billets dans la base de données :
- aéroport de départ (TEXT)
- aéroport d'arrivée (TEXT)
- prix (REAL)
- réservé par (TEXT)

Ainsi : 
- pour permettre à un utilisateur de voir la liste des vols disponibles, on cherche tous les billets dont le champ "réservé par" n'est pas NULL
- pour réserver un billet, le client fournit son nom / prénom
- pour voir ce qu'il a réservé, on cherche tous les billets dont le champ "réservé par"

## Stack technique / technos utilisées

- Front : Single-Page app. en HTML / CSS / React.js
- Back-end : Python / Flask
- BDD : sqlite3
