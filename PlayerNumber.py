class PlayerNumber:
    def __init__(self, playerNumber):
        self.playerNumber = playerNumber

    def dump(self):
        return {
            'playerNumber': self.playerNumber
        }
