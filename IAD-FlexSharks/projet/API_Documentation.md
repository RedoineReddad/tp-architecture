# Documentation de l'API

Dans ce document, nous documenterons explicitement les fonctionnalités de l'API développée dans le cadre de ce projet.

## Appels à l'API

Cette API propose 4 appels différents sur 4 routes distinctes :
- `/login?email=[email]` (`GET`) : Permet de récupérer l'user id correspondant à l'`email` fourni ;
- `/tickets/available` (`GET`) : Permet de récupérer la liste des billets disponibles et réservables (un billet par vol) ;
- `/tickets/booked?uid=[UID]` (`GET`) : Permet de récupérer la liste des billets réservés par l'utilisateur désigné par son `UID` ;
- `/tickets/[TID]?uid=[UID]` : Permet de réserver un billet désigné par son "ticket ID" `TID` pour l'utisateur désigné par son `UID`.

### Login
- Route : `/login?email=[email]`
- Méthode : `GET`
- Paramètre(s) à fournir : `email` (obligatoire)
- Réponse : 
	- Nominale : 
		- Code HTTP : 200 (OK)
		- Corps du message : identifiant utilisateur au format JSON
	- Paramètre attendu non ou mal fourni : 
		- Code HTTP : 400 (Bad Request)
		- Corps du message : message d'erreur
	- Adresse mail incorrecte ou inconnue :
		- Code HTTP : 401 (Unauthorized)
		- Corps du message : message d'erreur

##### Description :
L'appel de login permet d'authentifier l'utilisateur. Dans un cas simplifié
comme celui-ci, il se contente simplement de récupérer l'`uid` de l'utilisateur
et de le retourner. Dans une application plus évoluée, l'utilisateur devrait
soumettre son mot de passe, et l'API pourrait éventuellement retourner un
`session-id`.

##### Exemple : 
TODO insérer image curl


### Billets réservables
- Route : `/login/available`
- Méthode : `GET`
- Paramètre(s) à fournir : Aucun.
- Réponse : 
	- Nominale : 
		- Code HTTP : 200 (OK)
		- Corps du message : liste de billets et leurs attributs (détaillés dans l'exemple) au format JSON
	- Aucun billet disponible :
		- Code HTTP : 200 (OK)
		- Corps du message : liste au format JSON vide (`[]`)

##### Description :
Cet appel permet de récupérer une liste des billets que l'utilisateur peut
réserver.  Les billets sont retournés sous la forme d'une liste de
dictionnaires sérialisée : chaque champ est donc accessible explicitement. Pour
chaque vol disposant de plus d'un billet, l'API retournera un seul billet. En
effet, avec un grand nombre de billets, le client n'a pas à connaître les
caractéristiques des milliers voire millions d'autres billets pas encore
réservés.

##### Exemple : 
TODO insérer image curl


### Billets réservés
- Route : `/tickets/booked?uid=[UID]`
- Méthode : `GET`
- Paramètre(s) à fournir : `UID` (obligatoire)
- Réponse : 
	- Nominale : 
		- Code HTTP : 200 (OK)
		- Corps du message : liste de billets et leurs attributs (détaillés dans l'exemple) au format JSON
	- Paramètre attendu non ou mal fourni : 
		- Code HTTP : 400 (Bad Request)
		- Corps du message : message d'erreur
	- `UID` incorrect (non entier ou inconnu par la base de données) :
		- Code HTTP : 422 (Unprocessable Entity)
		- Corps du message : message d'erreur

##### Description :
Cet appel permet de récupérer toutes les informations des billets réservés par
l'utilisateur. Se référer à "Billets réservables" pour des informations sur le
format des données.

##### Exemple : 
TODO insérer image curl


### Réserver un billet
- Route : `/tickets/[TID]?uid=[UID]`
- Méthode : `PUT`
- Paramètre(s) à fournir : `UID` (obligatoire), `TID` (obligatoire
- Réponse : 
	- Nominale : 
		- Code HTTP : 200 (OK)
		- Corps du message : vide
	- Paramètre attendu non ou mal fourni : 
		- Code HTTP : 400 (Bad Request) ou 404 (Not Found)
		- Corps du message : message d'erreur
	- Paramètre au format incorrect :
		- Code HTTP : 422 (Unprocessable Entity)
		- Corps du message : message d'erreur
	- `TID` introuvable :
		- Code HTTP : 422 (Unprocessable Entity)
		- Corps du message : message d'erreur

##### Description :
Cet appel permet de réserver un billet spécifique désigné par son ticket ID
`TID` pour un utilsateur désigné par son `UID`.

##### Exemple : 
TODO insérer image curl


## Format des données

| Attribut        | Type                 | Description                                         |   |   |
|-----------------|----------------------|-----------------------------------------------------|---|---|
| `dep_code`      | Chaîne de caractères | Code IATA en 3 lettres de l'aéroport de départ      |   |   |
| `arr_code`      | Chaîne de caractères | Code IATA en 3 lettres de l'aéroport d'arrivée      |   |   |
| `dep_time`      | Entier               | Timestamp UNIX de la date et heure de départ du vol |   |   |
| `buyer_id`      | Entier               | `UID` de l'utilisateur ayant réservé le billet      |   |   |
| `ticket_id`     | Entier               | `TID` du billet                                     |   |   |
| `flight_id`     | Entier               | Identifiant unique du vol associé au ticket         |   |   |
| `price`         | Réel                 | Prix du billet                                      |   |   |
| `flight_number` | Chaîne de caractères | Numéro de vol (à ne pas confondre avec `flight_id`) |   |   |
| `seat`          | Chaîne de caractères | Siège réservé associé au billet                     |   |   |
| `company_id`    | Entier               | Identifiant unique de la compagnie aérienne         |   |   |
