from unittest import TestCase
from kqoc import *
from itertools import combinations
from random import shuffle
from random import choice


class Test_KQOC(TestCase):

    def setUp(self) -> None:
        self.players = [x for x in range(1, 9)]
        self.all_possible_teams = [Team(x, y) for x, y in combinations(self.players, 2)]
        # round1 = (P01, P02) vs (P03, P04)
        #          (P05, P06) vs (P07, P08)
        self.round1 = [Game(self.all_possible_teams[0], self.all_possible_teams[13]),
                       Game(self.all_possible_teams[22], self.all_possible_teams[27])]
        # round2 = (P01, P03) vs (P02, P04)
        #          (P05, P07) vs (P06, P08)
        self.round2 = [Game(self.all_possible_teams[1], self.all_possible_teams[8]),
                       Game(self.all_possible_teams[23], self.all_possible_teams[26])]
        # round3 = (P01, P04) vs (P02, P03)
        self.round3 = [Game(self.all_possible_teams[2], self.all_possible_teams[7])]
        self.tourney = [self.round1, self.round2, self.round3]

    def test_team_players_duplicate_in_round(self):
        tm1 = Team(1, 2)
        tm2 = Team(7, 8)
        tm3 = Team(1, 8)
        self.assertTrue(team_players_duplicate_in_round(tm1, self.round3))
        self.assertFalse(team_players_duplicate_in_round(tm2, self.round3))
        self.assertTrue(team_players_duplicate_in_round(tm3, self.round3))


class Test(TestCase):

    def setUp(self) -> None:
        self.players = [x for x in range(1, 9)]
        self.all_possible_teams = [Team(x, y) for x, y in combinations(self.players, 2)]
        self.round1 = [Game(self.all_possible_teams[0], self.all_possible_teams[13]),
                       Game(self.all_possible_teams[22], self.all_possible_teams[27])]
        self.round2 = [Game(self.all_possible_teams[1], self.all_possible_teams[8]),
                       Game(self.all_possible_teams[23], self.all_possible_teams[26])]
        self.round3 = [
            Game(self.all_possible_teams[2], self.all_possible_teams[7])]  # recreates a round halfway through creation
        self.tourney = [self.round1, self.round2, self.round3]

    def test_team_duplicate_in_tourney(self):
        tm1 = Team(1, 2)
        self.assertTrue(team_duplicate_in_tourney(tm1, self.tourney))
        tm2 = Team(6, 8)
        self.assertTrue(team_duplicate_in_tourney(tm2, self.tourney))
        tm3 = Team(10, 11)
        self.assertFalse(team_duplicate_in_tourney(tm3, self.tourney))
