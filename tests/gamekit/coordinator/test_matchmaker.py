from time import sleep, time
from gamekit.coordinator.matchmaker import Matchmaker

from gamekit.coordinator.types import MMStatus, MatchmakingRequest, Player, Storage



MMR_START = 1500
MMR_HIGH = 1700

def test_base_matchmaker():
    mm = Matchmaker()

    assert mm.add_player(Player(1, MMR_START)) is None
    assert mm.add_player(Player(2, MMR_START)) is None
    assert len(mm.buckets) == 1, "Player gets added to bucket"

    # Bucket(
    #   min=1350.0,
    #   max=1650.0,
    #   players=[
    #       Player(id=1, skill=1500),
    #       Player(id=2, skill=1500)
    #   ],
    #   start=datetime.datetime(2022, 8, 14, 16, 35, 16, 227756),
    #   sum=3000,
    #   smm=4500000
    # )
    # print(mm.buckets[0])

    assert mm.add_player(Player(3, MMR_START)) is None
    assert mm.add_player(Player(4, MMR_START)) is None
    assert mm.add_player(Player(5, MMR_START)) is None
    assert mm.add_player(Player(6, MMR_START)) is None
    assert mm.add_player(Player(7, MMR_START)) is None
    assert mm.add_player(Player(8, MMR_START)) is None
    assert mm.add_player(Player(9, MMR_START)) is None

    team = mm.add_player(Player(10, MMR_START))
    assert team is not None

    for i, player in enumerate(team):
        if i != player.id:
            break
    else:
        assert False, "Players were shuffled"

    metrics = mm.metrics()
    metrics['wait_times'] = [t if t > 1e-3 else 0 for t in metrics['wait_times']]

    assert metrics == dict(
        advantage=[0],
        deviation=[0.0],
        wait_times=[0.0]
    ), 'Metrics were generated'


def test_matchmaker_group_similar_skill():
    mm = Matchmaker()
    assert mm.add_player(Player(1, MMR_START)) is None
    assert mm.add_player(Player(2, MMR_START + 25)) is None
    assert mm.add_player(Player(3, MMR_START - 25)) is None
    assert mm.add_player(Player(4, MMR_START + 100)) is None
    assert mm.add_player(Player(5, MMR_START - 170)) is None
    assert mm.add_player(Player(6, MMR_START + 50)) is None
    assert mm.add_player(Player(7, MMR_START - 150)) is None
    assert mm.add_player(Player(8, MMR_START + 45)) is None
    assert mm.add_player(Player(9, MMR_START + 50)) is None
    assert len(mm.buckets) == 1, "Player gets added to bucket"
    team = mm.add_player(Player(10, MMR_START))
    assert team is not None

    metrics = mm.metrics()

    deviation = metrics.pop('deviation')
    advantage = metrics.pop('advantage')

    assert deviation[0] == 6911.25, "Deviation is correct"
    assert int(abs(advantage[0])) > 0, "Advantage is correct"


def test_matchmaker():
    mm = Matchmaker()

    assert mm.add_player(Player(1, MMR_START)) is None
    assert mm.add_player(Player(2, MMR_HIGH)) is None
    assert len(mm.buckets) == 2, "Player gets added to different bucket"

    assert mm.add_player(Player(3, MMR_START)) is None
    assert mm.add_player(Player(4, MMR_HIGH)) is None
    assert mm.add_player(Player(5, MMR_START)) is None
    assert mm.add_player(Player(6, MMR_HIGH)) is None
    assert mm.add_player(Player(7, MMR_START)) is None
    assert mm.add_player(Player(8, MMR_HIGH)) is None
    assert mm.add_player(Player(9, MMR_START)) is None
    assert mm.add_player(Player(10, MMR_HIGH)) is None, "No team could be generated right now"
    assert len(mm.buckets) == 2, "Players are in 2 different buckets"

    # Nor merge because the wait time is < to 10s
    teams = list(mm.check_buckets(10))
    assert len(teams) == 0

    sleep(0.1)

    # Force merge
    teams = list(mm.check_buckets(0.1))
    assert len(teams) == 1

    metrics = mm.metrics()
    wait_times = metrics.pop('wait_times')
    assert all([(t - 0.1) < 1e-2 for t in wait_times])

    deviation = metrics.pop('deviation')
    advantage = metrics.pop('advantage')

    assert deviation[0] == 10000.0, "Deviation is correct"
    assert int(abs(advantage[0])) in (0, 200, 600)

