class RoomDump:
    def __init__(self, room_id, room_name, players, password, isJoin, player1, player2, player3, player4):
        self.room_id = room_id
        self.room_name = room_name
        self.players = players
        self.password = password
        self.isJoin = isJoin
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4

    def dump(self):
        return {'room_id': self.room_id,
                'room_name': self.room_name,
                'players': self.players,
                'password': self.password,
                'isJoin': self.isJoin,
                'player1': self.player1,
                'player2': self.player2,
                'player3': self.player3,
                'player4': self.player4
                }
