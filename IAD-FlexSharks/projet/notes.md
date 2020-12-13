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


json / verbes HTTP REST

sélectionner arrivée / destination / jour pour voir les billets > semlbe un poil complexe

API : ne pas remonter ceux dont la date est déjà passée

group tickets by date


TODO makefile that generates flights at T+1-7 days

add number of seats ?




FILL UP DB AT API LAUNCH

/tmp/test.sql

TODO : document API

instruction ; pip install flask-cors
https://dev.to/matheusguimaraes/fast-way-to-enable-cors-in-flask-servers-42p0
