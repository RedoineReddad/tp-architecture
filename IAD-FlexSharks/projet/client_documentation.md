# Documentation client

Nous partons d'un template de projet de Client view, que l'on adapte à notre cas d'utilisation :  
   
  
  Pour celà, nous utilisons plusieurs routes: 
  - `/login?email=[email]` (requête GET,POST) :   
    On envoie une adresse email en paramètre de requête et le serveur renvoie un id qui permet de récupérer les billets d'avions associés à l'email.
  - `/tickets/available` (requête GET):  
    Renvoie les billets disponibles de la base de données.
  
  - `/tickets/booked?uid=[UID]` (requête GET):  
    On réserve le ticket avec l'id récupérer avec la première route.
  - `/tickets/[TID]?uid=[UID]` (requête PUT):  
    Finalise la réservation avec l'id de l'utilisation et l'id du ticket.
    
    
