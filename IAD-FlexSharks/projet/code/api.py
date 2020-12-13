import flask
from flask import request, jsonify, g
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Using g as the application context ; we have only one connection object
# shared between all requests in order to ensure successful concurrent API
# calls. This ensures concurrent writes will succeed instead of failing to
# connect because a connection is already established elsewhere.
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('ticket_booking.db')
        db.row_factory = sqlite3.Row
    return db

@app.errorhandler(400)
def bad_request(e):
    return "<h1>Error 400 : Bad Request.<h1> <h3><p>Unknown or malformed API call. RTFM.</p></h3>", 400

@app.errorhandler(401)
def unauthorized(e):
    return "<h1>Error 401 : Unauthorized.<h1>", 401

@app.errorhandler(422) # WebDAV but who cares ? :D (seriously, it's the most semantically appropriate code...)
def unprocessable_entity(e) :
    return "<h1>Error 422 : Unprocessable entity.<h1> <h3><p>Wrong parameter.</p></h3>", 422

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
    if not request.args.get('email') :
        return bad_request(400)

    c = get_db().cursor()
    rs = c.execute('SELECT id FROM users WHERE email=?', (request.args.get('email'),)).fetchall() # note to self : execute expects a tuple of parameters
    
    buf = [dict(row) for row in rs]
    return jsonify(buf) if buf != [] else unauthorized(401)

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
    c = get_db().cursor()
    query = (
    'SELECT * FROM ( ' # get flights' contents ; need to make a select on top in order to return all fields after the join with flights
    '    SELECT tickets.* FROM tickets ' # get tickets' contents
    '    JOIN ( '
    '        SELECT ticket_id, flight_id FROM tickets ' # get unique ids for each flight_id group
    '        WHERE tickets.buyer_id IS NULL ' # do this in the innermost request, before group by
    '        GROUP BY flight_id '
    '    ) AS t '
    '    ON tickets.ticket_id = t.ticket_id ' # join unique flight tickets with tickets on these unique ids
    ') AS test '
    'JOIN flights ON flights.flight_id = test.flight_id;')

    rs = c.execute(query).fetchall() # TODO add check date

    return jsonify( [dict(row) for row in rs] )

    #return 'ticket JSON list'

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
@app.route('/tickets/booked', methods=['GET'])
def tickets_booked(): 
    #if request.args.get('uid') # gérer absence de l'arg return page_not_found(404)
    if not request.args.get('uid') :
        return bad_request(400)
    try:
        uid = int(request.args.get('uid'))
    except:
        return unprocessable_entity(422)

    c = get_db().cursor()

    query = (
    'SELECT * FROM ( ' # get flights' contents ; need to make a select on top in order to return all fields after the join with flights
    '    SELECT tickets.* FROM tickets ' # get tickets' contents
    '    JOIN ( '
    '        SELECT ticket_id, flight_id FROM tickets ' # get unique ids for each flight_id group
    '        WHERE tickets.buyer_id IS ? ' # do this in the innermost request, before group by
    '        GROUP BY flight_id '
    '    ) AS t '
    '    ON tickets.ticket_id = t.ticket_id ' # join unique flight tickets with tickets on these unique ids
    ') AS test '
    'JOIN flights ON flights.flight_id = test.flight_id;')

    rs = c.execute(query, (request.args.get('uid'),)).fetchall() # note to self : execute expects a tuple of parameters

    if c.rowcount != 1 : # Argument(s) wrong / the request doesn't modify anything
        return unprocessable_entity(422) # WebDAV but who cares ? :D (seriously, it's the most semantically appropriate code...)

    return jsonify( [dict(row) for row in rs] )


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
# 
# The same remark as above applies here about identification. We don't want
# just any client booking tickets as other clients.
@app.route('/tickets/<int:tid>', methods=['PUT'])
def tickets_book(tid): 
    # Make sure the request is formed correctly and types are correct (no need to check tid, it's in the where clause and it's parsed as a route argument)
    if not request.args.get('uid') :
        return bad_request(400)
    try:
        uid = int(request.args.get('uid'))
    except:
        return unprocessable_entity(422)

    c = get_db().cursor()

    query = 'UPDATE tickets SET buyer_id=? WHERE ticket_id=?'

    rs = c.execute(query, (request.args.get('uid'), tid)) # note to self : execute expects a tuple of parameters
    get_db().commit()

    if c.rowcount != 1 : # Argument(s) wrong / the request doesn't modify anything
        return unprocessable_entity(422) # WebDAV but who cares ? :D (seriously, it's the most semantically appropriate code...)

    return "", 200 # OK

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

app.run()
