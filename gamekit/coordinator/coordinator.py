from ast import Load
import asyncio
from datetime import datetime
import struct
import time
import json
import bisect

from gamekit.coordinator.types import MMStatus, MatchmakingRequest, Player, Storage, Ranker
from gamekit.coordinator.matchmaker import Matchmaker


def to_obj(message: bytes) -> any:
    return json.loads(message)

async def read(reader, timeout=None):
    data = await (reader.read(4096))

    if not data:
        return None

    size = struct.unpack('I', data[0:4])[0]

    elapsed = 0
    while len(data) < size:
        data += await reader.read(4096)

        if len(data) == 0:
            time.sleep(0.01)
            elapsed += 0.01

        if timeout and elapsed > timeout:
            raise TimeoutError('Was not able to receive the entire message in time')

    return to_obj(data[4:])


def write(writer, msg):
    data = json.dumps(msg).encode('utf-8')
    size = struct.pack('I', len(data))
    writer.write(size + data)


class StorageMemory(Storage):
    def __init__(self):
        self.queue = []
        self.n = 5

    def add_player(self, player_id, player_skill):
        item = (player_id, player_skill)
        bisect.insort(self.players, item, key=lambda x: x[1])

    def remove_player(self, player_id):
        for i, (id, _) in enumerate(self.players):
            if id == player_id:
                del self.players[i]
                break

    def group(self):
        team = []

        while len(self.queue) > self.n * 2:
            player = self.queue.pop()
            team.append(player)

            if len(team) == self.n * 2:
                self.improve_team(team)
                yield team
                team = []


class LoadBalancer:
    def __init__(self) -> None:
        self.resources = []


class Server:
    """

    TODO: handle the case were no game server are available
    TODO: how could we compute an ETA
        * MM ETA + Free Server ETA

    """
    def __init__(self) -> None:
        self.matchmaker = Matchmaker()      # Match player together
        self.ranker = Ranker()              # Player Skill estimator
        self.storage = Storage()            # Store player & Match information
        self.load_balancer = LoadBalancer() # Load balance the game server
        self.queue = asyncio.Queue()        # Queue Matchmaking requests
        self.loop = asyncio.new_event_loop()

    def run(self):
        asyncio.set_event_loop(self.loop)

        self.loop.create_task(self.matchmaking_task, self.matchmaker, self.queue)
        self.loop.create_task(asyncio.start_server(self.handle_client))
        self.loop.run_forever()

    async def fetch_player_skill(self, playerid):
        # Fetch player skill from the database
        return self.storage.get_player(playerid)['skill']

    async def insert_match(self, match):
        # the match is insterted into the database
        #
        # The machined is assigne right now
        # Players user the match_id as the 'key' to connect to the server
        # So not infra information is shared to clients
        #
        # if not server is available this is going to wait
        # until one is available
        machine = self.load_balancer()

        match_id = self.storage.insert_match(dict(
            players=match,
            server=machine
        ))

        return match_id

    async def update_player_skill(self, match_id, result):
        """This is a private method that can only be triggered by the game server"""
        # Update player skill in the database from the match result
        # Release the game server to the pool

        match = self.storage.update_match(match_id, result)

        for player in match['players']:
            self.ranker.update_player_skill(player['id'], match)
            self.storage.update_player(player['id'], player['skill'])

        self.storage.free_server(match['server'])

    async def handle_client(self, reader, writer):
        """This is a public method that is triggered by game clients to connect to a server"""
        request = MatchmakingRequest(**await read(reader))

        skill = await self.fetch_player_skill(request.player_id)

        # Insert player into the matchmaking queue
        future = self.loop.create_future()
        player = Player(request.player_id, skill, future)

        self.queue.put_nowait(('add', player))
        started = datetime.utcnow()
        while True:
            # Player cancels the matchmaking request
            try:
                request = asyncio.wait_for(read(reader), timeout=1)
                self.queue.put_nowait(('remove', player))
                write(writer, json.dumps(dict(
                    status=MMStatus.Cancelled,
                )).encode())
                writer.close()
                break
            except asyncio.TimeoutError:
                pass

            # Wait for the matchmaking reply
            try:
                match_id, pos_id = asyncio.wait_for(future, timeout=1)

                write(writer, json.dumps(dict(
                    status=MMStatus.Found,
                    match_id=match_id,
                    position_id=pos_id,
                )).encode())
                break
            except asyncio.TimeoutError:
                pass

            if (datetime.utcnow() - started).total_seconds > 30:
                write(writer, json.dumps(dict(
                    status=MMStatus.Pending,
                )).encode())

        writer.close()

    async def prepare_match(self, team):
        match_id = self.insert_match(team)

        for player in team:
            player.future.set_result((match_id, player.position))

    async def matchmaking_task(self):
        while True:
            try:
                try:
                    # wait new players
                    action, player = asyncio.wait_for(self.queue.get(), timeout=10)

                    if action == 'remove':
                        self.matchmaker.remove_player(player)

                    elif action == 'add':
                        team = self.matchmaker.add_player(player)

                        self.prepare_match(team)
                    #
                except asyncio.TimeoutError:
                    pass

                # merge buckets after 60 seconds
                for team in self.matchmaker.check_buckets(60):
                     self.prepare_match(team)

            except KeyboardInterrupt:
                self.queue.task_done()
                break


def main():
    server = Server()
    server.run()
