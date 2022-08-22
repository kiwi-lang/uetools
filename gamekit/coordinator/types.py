from asyncio import Future
from enum import Enum
from dataclasses import dataclass


class MMStatus(Enum ):
    Pending = 0
    Found = 1
    Cancelled = 2
    Error = 3


@dataclass
class MatchmakingRequest:
    player_id: int


class Storage:
    def add_player(self, player_id, player_skill):
        pass

    def remove_player(self, player_id):
        pass


@dataclass
class Player:
    id: int         # Player ID
    skill: int      # Estiamted Player skill
    position: int   # Player Position inside the team
    fututre: Future # Match future value


@dataclass
class Match:
    id: int         # Match ID
    players: list   # List of player assigned to this match
    server: int     # Server ID


class Ranker:
    pass

    def update_skill(self, player, match):
        """Update a player skill"""
        return player
