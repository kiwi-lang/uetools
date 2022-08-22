
import asyncio

from gamekit.coordinator.types import MMStatus
from gamekit.coordinator.coordinator import Server, read, write


count = 0

def client_done(task):
    if count == 0:
        loop = asyncio.get_event_loop()
        loop.stop()


@asyncio.coroutine
def game_client_mock(host, port, player_id, skill):
    count += 1
    reader, writer = yield from asyncio.open_connection(host, port)

    write(writer, dict())

    while True:
        data = yield from read(reader)

        if (data['status'] == MMStatus.Cancelled):
            break

        elif (data['status'] == MMStatus.Found):
            break

        elif (data['status'] == MMStatus.Pending):
            pass

    count -= 1

# https://gist.github.com/dbehnke/9627160

def test_coordinator():
    server = Server()
    loop = asyncio.get_event_loop()

    host = ''
    port = 8123
    client_counts = 200

    for i in range(client_counts):
        player_id = i
        skill = i

        task = asyncio.Task(game_client_mock(host, port, player_id, skill))
        task.add_done_callback(client_done)

    server.run()


