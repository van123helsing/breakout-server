import psycopg2
from psycopg2.extras import RealDictCursor
import json
from RoomDump import RoomDump


class DataBase:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="ec2-34-248-165-3.eu-west-1.compute.amazonaws.com",
            database="dbkn76lf791csu",
            user="wpfzluzejjgqls",
            password="c33480019251cfacc235c671d5d7ab6cc186f323fc29bf0bd9096172b2cabdac"
        )
        self.conn.autocommit = True

    def insert_player(self, data_object):
        cur = self.conn.cursor()
        query = """INSERT INTO public.players (player_name) VALUES (%s) RETURNING player_id;"""
        cur.execute(query, (data_object.name,))
        player_id = cur.fetchone()
        cur.close()
        if player_id is not None:
            return player_id[0]
        return player_id

    def insert_player_object(self, data_object):
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        query = """INSERT INTO public.players (player_name) VALUES (%s) RETURNING *;"""
        cur.execute(query, (data_object.name,))
        player = cur.fetchone()
        cur.close()
        return json.dumps(player, indent=2)

    def insert_room(self, data_object):
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        query = """ with upd as
                    (INSERT INTO public.rooms (room_name, room_password, player1, player2, player3, player4)
                                VALUES (%s, %s, %s, %s, %s, %s) RETURNING *)
                select room_id, room_name, room_password,plyr1.player_name as player1,plyr2.player_name as player2,plyr3.player_name as player3, plyr4.player_name as player4
                from upd
                    LEFT join  public.players plyr1 ON (plyr1.player_id = upd.player1 and upd.player1 is not null)
                    LEFT join  public.players plyr2 ON (plyr2.player_id = upd.player2 and upd.player2 is not null)
                    LEFT join  public.players plyr3 ON (plyr3.player_id = upd.player3 and upd.player3 is not null)
                    LEFT join  public.players plyr4 ON (plyr4.player_id = upd.player4 and upd.player4 is not null)"""
        cur.execute(query,
                    (data_object.name, data_object.password, data_object.player1,
                     data_object.player2, data_object.player3, data_object.player4))
        room = cur.fetchone()
        cur.close()
        return json.dumps(room, indent=2)

    def insert_score(self, data_object):
        cur = self.conn.cursor()
        query = """INSERT INTO public.scores (player_name, score) VALUES (%s, %s) RETURNING scores_id;"""
        cur.execute(query, (data_object.name, data_object.score))
        scores_id = cur.fetchone()
        cur.close()
        if scores_id is not None:
            return scores_id[0]
        return scores_id

    def empty_database(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM public.rooms")
        cur.execute("DELETE FROM public.players")
        cur.execute("DELETE FROM public.scores")
        cur.close()
        return True

    def get_players(self):
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM public.players")
        value = cur.fetchall()
        cur.close()
        return json.dumps(value, indent=2)

    def get_rooms(self):
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM public.rooms")
        value = cur.fetchall()
        cur.close()
        li = list()
        for i in value:
            players = 0
            players += 1 if i['player1'] is not None else 0
            players += 1 if i['player2'] is not None else 0
            players += 1 if i['player3'] is not None else 0
            players += 1 if i['player4'] is not None else 0
            password = True if i['room_password'] != '' and i['room_password'] is not None else False
            is_join = True if players < 4 else False
            li.append(RoomDump(i['room_id'], i['room_name'], players, password, is_join, i['player1'],i['player2'],i['player3'],i['player4']))
        return json.dumps([o.dump() for o in li])

    def get_scores(self):
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM public.scores ORDER BY score DESC LIMIT 10")
        value = cur.fetchall()
        cur.close()
        return json.dumps(value, indent=2)

    def get_room(self, id):
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM public.rooms WHERE room_id=%s",(id,))
        room = cur.fetchall()
        cur.close()
        return room

    def update_room(self, data_object, id):
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        query = """ with upd as
                        (UPDATE public.rooms
                        SET player1=%s, player2=%s, player3=%s, player4=%s
                        WHERE room_id=%s
                        RETURNING *)
                select room_id, room_name, room_password,plyr1.player_name as player1,plyr2.player_name as player2,plyr3.player_name as player3, plyr4.player_name as player4
                from upd
                    LEFT join  public.players plyr1 ON (plyr1.player_id = upd.player1 and upd.player1 is not null)
                    LEFT join  public.players plyr2 ON (plyr2.player_id = upd.player2 and upd.player2 is not null)
                    LEFT join  public.players plyr3 ON (plyr3.player_id = upd.player3 and upd.player3 is not null)
                    LEFT join  public.players plyr4 ON (plyr4.player_id = upd.player4 and upd.player4 is not null)"""
        cur.execute(query, (data_object.player1, data_object.player2, data_object.player3, data_object.player4, id))
        room = cur.fetchone()
        cur.close()
        return json.dumps(room, indent=2)
