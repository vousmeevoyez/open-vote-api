"""
    Handle Web Socket here
"""
from flask_socketio import emit, send

from app.api import socket

from app.api.election.modules.election_services import ElectionServices

NAMESPACE="/stream"

def current_vote(election_id):
    """
        function to check current vote for certain election
    """
    response = ElectionServices(election_id).info()[0]

    # init place holder for trimmed response
    current_vote = []
    # trim response so it return essentials information only
    candidates = response["data"]["candidates"]
    for candidate in candidates:
        current_vote.append({
            "name" : candidate["name"],
            "id"   : candidate["id"],
            "votes": candidate["votes"]
        })
    return current_vote

@socket.on('connect', namespace=NAMESPACE)
def client_connect():
    """
        Socket Event when client connected
    """
    send({'data': 'connected'})

@socket.on('disconnect', namespace=NAMESPACE)
def client_disconnect():
    """
        Socket Event when client disconnected
    """
    print('disconnected')

@socket.on('live_count', namespace=NAMESPACE)
def count_vote(message):
    """
        Socket Event client send some data
    """
    # fetch election id
    election_id = message["election_id"]
    votes = current_vote(election_id)

    emit("live_count", votes, broadcast=True)
