QUESTIONS : 
	- client / front : 2 entités différentes ? client > API problématique ?
		> SPA : le js envoie des requêtes XHR & co à l'API
		> Angular / Vue / React
		> ne pas avoir à recharger la page pour récupérer la liste des vols
	- plusieurs utilisateurs ? Ou juste un booléen réservé / pas réservé ?
		> renseigner son nom à la réservation du billet ?


Répartition :
	- Alexandre : back / python
	- Filippo : front
	- Redoine : front
	- Vincent : front
	- Houyou : back
	- Jingyang : back

TODO maz :
	- DONE regen base à chaque exécution de l'api
	- DONE ne pas remonter les available dont la date est passée
	- DONE order by dep_time
	- documenter comment lancer le bordel
	- gérer le CORS
		instruction ; pip install flask-cors
		https://dev.to/matheusguimaraes/fast-way-to-enable-cors-in-flask-servers-42p0
