from __future__ import annotations

from dataclasses import dataclass
import random
from functools import reduce
from datetime import datetime
import bisect

from gamekit.coordinator.types import Player



def add_skill(a, b):
    return a + b.skill

def add_skill_squared(a, b):
    return a + b.skill ** 2

def min_skill(a, b):
    return min(a, b.skill)

def max_skill(a, b):
    return max(a, b.skill)


@dataclass
class Bucket:
    """Group player with the same skill

    Note
    ----
    Some Ranking system have a volatility parameter which could be used to
    group players together given a confidence interval.

    """
    min: int        # Min skill
    max: int        # Max skill
    players: list   # Players
    start: datetime # Creation time
    sum: float      # sum of plauer skill
    smm: float      # squared sum of player skill

    @staticmethod
    def new_bucket(*players, var=0.1):
        err = reduce(add_skill_squared, players, 0)
        sum = reduce(add_skill, players, 0)

        return Bucket(
            reduce(min_skill, players, +9999999999) * (1 - var),
            reduce(max_skill, players, -9999999999) * (1 + var),
            list(players),
            start=datetime.utcnow(),
            sum=sum,
            smm=err
        )

    def contains(self, player: Player) -> bool:
        #
        #  1 = 68%
        #  2 = 95%
        #  3 = 99.7% confience interval
        # min = player.skill - 1 * player.std
        # max = player.skill + 2 * player.std
        # min < (self.min + self.max) / 2 < max

        return self.min < player.skill and player.skill < self.max

    def __lt__(self, other):
        return self.min < other.min

    def __gt__(self, other):
        return self.min < other.min

    def avg(self):
        return self.sum / len(self.players)

    def var(self):
        return self.smm / len(self.players) - self.avg() ** 2

    def std(self):
        return self.var() ** 0.5

    def add_player(self, player, match_size, var):
        assert len(self.players) < 10

        self.min = min(self.min, player.skill * (1 - var))
        self.max = max(self.max, player.skill * (1 + var))
        self.smm += player.skill ** 2
        self.sum += player.skill

        self.players.append(player)

        if len(self.players) == match_size:
            return self.players

        return None


def merge_buckets(b1: Bucket, b2: Bucket, match_size: int, var: float):
    """Merge two buckets into one bucket, generate teams if the merging can produce one"""
    player_pool = b1.players + b2.players
    team = None

    if len(player_pool) >= match_size:
        random.shuffle(player_pool)
        team = player_pool[:match_size]
        player_pool = player_pool[match_size:]

    bucket = None
    if player_pool:
        bucket = Bucket.new_bucket(*player_pool, var=var)

    return bucket, team


class Matchmaker:
    """Players are added in buckets of skill, this is to avoid making teams with too big difference skills between players.

    When the queue time starts to be too long, the buckets are merged in two until a team can be made.

    """
    def __init__(self) -> None:
        self.buckets = []

        #
        # Match quality Metrics
        #
        self.wait_times = []        # we want wait times to be low
        self.advantage = []         # we want advantage to be around 0
        self.deviation = []         # we want deviation to be low
        self.n = 5
        self.var = 0.1

    def metrics(self):
        metrics = dict(
            wait_times=self.wait_times,
            advantage=self.advantage,
            deviation=self.deviation
        )
        self.wait_times = []
        self.advantage = []
        self.deviation = []
        return metrics

    def save_metrics(self, team , wait_time):
        t1 = 0
        s = 0
        ss = 0

        for p in team[:self.n]:
            t1 += p.skill
            ss += p.skill ** 2
            s += p.skill

        for p in team[self.n:]:
            t1 -= p.skill
            ss += p.skill ** 2
            s += p.skill

        self.advantage.append(t1)
        self.deviation.append(ss / (2 * self.n) - (s / (2 * self.n)) ** 2)
        self.wait_times.append(wait_time.total_seconds())
        return team

    def make_team(self, team):
        random.shuffle(team)

        for i, player in enumerate(team):
            player.position = i

        return team

    def remove_player(self, player):
        pass

    def add_player(self, player: Player):
        now = datetime.utcnow()

        for i, bucket in enumerate(self.buckets):

            if bucket.contains(player):
                team = bucket.add_player(player, self.n * 2, var=self.var)

                if team:
                    del self.buckets[i]
                    return self.save_metrics(self.make_team(team), now - bucket.start)

                break

        else:
            bisect.insort(self.buckets, Bucket.new_bucket(player, var=self.var))

    def check_buckets(self, merge_deadline: float):
        """Periodically called to make sure the wait time do not become too high"""
        teams = []
        now = datetime.utcnow()

        i = 1
        while i < len(self.buckets):
            bucket = self.buckets[i]
            elasped = (now - bucket.start).total_seconds()

            if i == 1:
                # because we always skip the first bucket we need to check its time here
                elasped_first =  (now - self.buckets[0].start).total_seconds()
                elasped = max(elasped_first, elasped)

            if elasped >= merge_deadline:
                offset = i - 1
                mbucket = self.buckets[offset]
                nbucket, team = merge_buckets(bucket, mbucket, self.n * 2, var=self.var)

                if team:
                    team = self.make_team(team)
                    team = self.save_metrics(team, max(now - mbucket.start, now - bucket.start))
                    teams.append(team)

                del self.buckets[i]
                del self.buckets[offset]

                # we deleted 2 buckets and inserted none, next bucket is at index i - 1
                increment = -1
                if nbucket:
                    bisect.insort(self.buckets, nbucket)

                    # we detected 2 buckets and inserted one, next bucket is at index i
                    # we skip the inserted bucket on go to next
                    increment = 0

                i = max(0, i + increment)
            else:
                # Bucket does not need to be merged, move forward
                i += 1

        for team in teams:
            yield team
