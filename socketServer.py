import socketio
from flask import Flask
from PlayerJoined import PlayerJoined
import requests


sio = socketio.Server(async_mode='threading', cors_allowed_origins='*')
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

players = []


@sio.on('connect')
def connect(sid, env):
    print('connected ', sid)
    sio.emit('joined-room', "")


@sio.on('disconnect')
def disconnect(sid):
    print('disconnected ', sid)
    print('disconnected ', len(players))
    rid = 0
    pid = 0
    for i in players:
        if i.sid == sid:
            rid = i.rid
            pid = i.pid
            players.remove(i)
    requests.post(url="https://localhost:8443/leave-room", data={'idPlayer': pid}, verify=False)
    sio.emit('someone left', room=str(rid), skip_sid=sid)
    print('disconnected ', len(players))


@sio.on('joined-room')
def joined_room(sid, data):
    print('joined room ', sid)
    players.append(PlayerJoined(sid, data['player_id'], data['room_id'], 0, 0))
    sio.enter_room(sid, str(data['room_id']))
    sio.emit('someone joined', data, room=str(data['room_id']), skip_sid=sid)
    num_players = 0
    for i in players:
        if i.rid == data['room_id']:
            num_players += 1
    if num_players  == 4:
        sio.emit('start game', data, room=str(data['room_id']))


@sio.on('update-paddle')
def update_paddle(sid, data):
    print('updating paddle location ', sid)
    rid = 0
    for i in range(len(players)):
        if players[i].sid == sid:
            rid = players[i].rid
            players[i].x = data['x']
            players[i].y = data['y']
    sio.enter_room(sid, str(rid))
    sio.emit('paddle moved', data, room=str(rid), skip_sid=sid)


if __name__ == '__main__':
    app.run(threaded=True,debug=True)