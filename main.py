import db as db
from Player import Player
from Room import Room
from Scores import Scores
from flask_cors import CORS,cross_origin
from flask import request
import json

import flask

dbConn = db.DataBase()
app = flask.Flask(__name__)
app.config['CORS_HEADERS'] = 'application/json'
CORS(app, support_credentials=True)


@app.route('/scores', methods=['GET'])
def scores():
    return dbConn.get_scores()


@app.route('/players', methods=['GET'])
def players():
    return dbConn.get_players()


@app.route('/rooms', methods=['GET'])
def rooms():
    return dbConn.get_rooms()


@app.route('/room', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def room():
    req = json.loads(request.data.decode("utf-8"))
    r = dbConn.get_room(req.get('room_id'))
    room = Room(r[0]['room_name'], r[0]['room_password'], r[0]['player1'], r[0]['player2'], r[0]['player3'],r[0]['player4'])
    return dbConn.update_room(room, req.get('room_id'))


@app.route('/rooms', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def create_room():
    req = json.loads(request.data.decode("utf-8"))
    p = req.get('player_id')
    r = Room(req.get('room_name'), req.get('password'), p, None, None, None)
    return dbConn.insert_room(r)


@app.route('/player', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def create_player():
    req = json.loads(request.data.decode("utf-8"))
    p = Player(req.get('playerName'))
    return dbConn.insert_player_object(p)


@app.route('/players', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def join_room():
    req = json.loads(request.data.decode("utf-8"))
    p = req.get('player_id')
    r = dbConn.get_room(req.get('room_id'))
    room = Room(r[0]['room_name'], r[0]['room_password'], r[0]['player1'],r[0]['player2'],r[0]['player3'],r[0]['player4'])
    if room.password != "":
        if room.password != req.get('roomPassword'):
            return "Wrong password!"
    if room.player1 is None:
        room.player1 = p
    elif room.player2 is None:
        room.player2 = p
    elif room.player3 is None:
        room.player3 = p
    elif room.player4 is None:
        room.player4 = p
    else:
        return "Room is full!"

    return dbConn.update_room(room, req.get('room_id'))


@app.route('/leave-room', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def leave_room():
    req = json.loads(request.data.decode("utf-8"))
    r = dbConn.get_room(req.get('idRoom'))
    player1 = None if r[0]['player1'] == req.get('idPlayer') else r[0]['player1']
    player2 = None if r[0]['player2'] == req.get('idPlayer') else r[0]['player2']
    player3 = None if r[0]['player3'] == req.get('idPlayer') else r[0]['player3']
    player4 = None if r[0]['player4'] == req.get('idPlayer') else r[0]['player4']
    room = Room(r[0]['room_name'], r[0]['room_password'], player1, player2, player3, player4)

    return dbConn.update_room(room,  req.get('roomId'))


@app.route('/scores', methods=['POST', 'OPTIONS'])
@cross_origin(supports_credentials=True)
def create_score():
    s = Scores("Najboljsi", 1000)
    return dbConn.insert_score(s)


def main():
    dbConn.empty_database()
    p = Player("player3")
    r = Room("Room1", "", None, None, None, None)
    s = Scores("Najboljsi", 1000)
    p_id = dbConn.insert_player(p)
    print(p_id)
    r2 = Room("Room2", "fgh", p_id, None, None, None)
    print(dbConn.insert_room(r))
    print(dbConn.insert_room(r2))
    print(dbConn.insert_score(s))

    context = ('cert.pem', 'key.pem')
    app.run(debug=True,host="localhost", port=8443, ssl_context=context)


if __name__ == "__main__":
    main()