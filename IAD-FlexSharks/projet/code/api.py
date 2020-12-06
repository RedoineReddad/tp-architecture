import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# DB handle parameter : 
# Connection to the DB is done globally due to the concurrent nature of API calls.
# This ensures concurrent writes will succeed instead of failing to connect
# because a connection is already established elsewhere.
dbconn = sqlite3.connect('books.db')

# note to self : request.args contains GET arguments

# 4 API calls :
# - login
# post adresse mail > get user_id
# - get available tickets
# returns a json list of tickets with : 
# ticketid, départ, destination, prix
# - book a flight
# - ticketid, user_id
# - get reserved by
# /booked_tickets/username
# ticketid, départ, dest, prix

# /api/login
# /tickets/available
# /tickets/booked/USERNAME

# ^^^^^^^^^^ hot smoking garbo ^^^^^^^^^^^
##########################################

# Login
##############################
# The client sends the login email using a URL parameter (e.g.
# /login?email=john.doe@gmx.com), and the API returns the corresponding user ID
# or an error string if login fails.
# GET is used because even though we are sending user information, since
# semantically, the intent is to "GET" a user ID.
# 
# This API call entirely disregards any notion of security when it comes to
# login. While a production application may be run with SSL (in which case the
# URL parameters would be encrypted since SSL resides between the TCP and HTTP
# layers), a more typical approach would involve getting a token (decorrelated
# from the user name / id) or a HMAC-based mechanism, or a even a two-step
# challenge mechanism.
# 
# Using a URL parameter allows us to easily scale the parameters account to any
# new authentication method.
@app.route('/login', methods=['GET'])
def login(): 
    global dbconn
    return request.args.get('user')

# Fetch available tickets
##############################
# The API call returns a JSON list of all available tickets at the current time. Most notably, it returns :
# - the ticket ID
# - the departure airport
# - the arrival airport
# - the ticket price
# - the flight departure date / time (TODO ?)
@app.route('/tickets/available', methods=['GET'])
def tickets_available():
    global dbconn
    return 'ticket JSON list'

# Fetch booked tickets
##############################
# The client sends the logged in user ID in the URL
# The API call returns a JSON list of all booked tickets by the user specified as a URL parameter. Most notably, it returns : 
# - the ticket ID
# - the departure airport
# - the arrival airport
# - the ticket price
# - the flight departure date / time (TODO ?) or status if 
# 
# In a production application, we would also need some kind of authentication
# here. Most likely, the client would pass a session token / id, which would
# both act as an identifier and a way to verify authentication. In the case,
# the route would probably look like '/tickets/booked?sid=[session token]'.
@app.route('/tickets/booked_tickets', methods=['GET'])
def tickets_booked(uid): 
    global dbconn
    uid = request.args.get('uid')
    return 'list of booked tickets'


# Book a ticket
##############################
# In this case, the "PUT" verb on the '/tickets/[ticket_id]' route clearly
# indicates the intention to modify a specific "ticket" ressource.
# 
# Given the potentially concurrent nature of API calls, it is necessary to take
# into account the possibility of two clients wanting to book the same ticket
# at about that same time. In practice, client 1 and 2 would load the ticket
# list, and client 1 would book said ticket. Without a page refresh, client 2
# would still see the ticket available, and the API needs to be able to signify
# the client that this specific ticket isn't available for purchase anymore
# (whereupon the client would reload the list, displaying another ticket for
# the same flight -with a different id-, or nothing if none is left).
@app.route('/tickets/<int:tid>', methods=['PUT'])
def tickets_book(tid): 
    global dbconn

    return 'list of booked tickets'


app.run()
dbconn.close() # Close the connection upon program exit
