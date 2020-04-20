from itertools import combinations
from random import shuffle
from random import choice
import yaml
import datetime


class Game:
    def __init__(self, t1, t2):
        if t1.p1 in t2 or t1.p2 in t2:
            raise ValueError("can't have a game with same person on both teams")
        else:
            self.t1 = t1
            self.t2 = t2
            self.__i = 0

    # item is a team
    def __contains__(self, item):
        return self.t1 == item or self.t2 == item

    def __str__(self):
        return "{} vs {}".format(str(self.t1), str(self.t2))

    def __eq__(self, other):
        return self.t1 in other and self.t2 in other

    def __iter__(self):
        return self

    def __next__(self):
        if self.__i == 0:
            self.__i = 1
            return self.t1
        elif self.__i == 1:
            self.__i = 2
            return self.t2
        else:
            self.__i = 0
            raise StopIteration


class Team:
    # no need for duplicate player error checking. combinations() won't give duplicate player team. ex P01 P01
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.__i = 0

    # overrides the "x in y" phrase! :)
    # check player in team. "item" is a player (int)
    def __contains__(self, item):
        return self.p1 == item or self.p2 == item

    def __str__(self):
        return "(P{:02}, P{:02})".format(self.p1, self.p2)

    def __eq__(self, other):
        """
        :param other: a Team object to compare against
        :return: True if players are identical
        """
        return self.p1 in other and self.p2 in other

    def __iter__(self):
        return self

    def __next__(self):
        if self.__i == 0:
            self.__i = 1
            return self.p1
        elif self.__i == 1:
            self.__i = 2
            return self.p2
        else:
            self.__i = 0
            raise StopIteration


def team_players_duplicate_in_round(team1, round):
    val = False
    for game in round:
        for tm in game:
            if team1.p1 in tm or team1.p2 in tm:
                val = True
    return val


def team_duplicate_in_tourney(team, tourney):
    val = False
    for round in tourney:
        for game in round:
            if team in game:
                val = True
    return val


def create_tourny():
    """
        read in the yaml, output tournament brackets
    """
    # TODO: make it so the same person can't be left out of multiple games before everyone else has been left out
    # TODO: add capability to demand certain games before generation starts by placing info in yaml

    with open("kqoc.yaml", 'r') as yml:
        cfg = yaml.load(yml, Loader=yaml.FullLoader)

    # list of ints ex: [1, 2, 3, 4]
    players = [x for x in range(1, cfg['num_players'] + 1)]
    print("Number of players: {}".format(cfg['num_players']))

    # list of team objects
    all_possible_teams = [Team(x, y) for x, y in combinations(players, 2)]
    print("Number of possible teams: " + str(len(all_possible_teams)))

    tourney_rounds = []
    while cfg['num_rounds'] > 0:
        # create one round and append to tourney
        single_round_games = []
        for x in range(cfg['num_players'] // 4):
            # runs for each game for a round. num of games per round = numplayers // 4

            # choose team1.
            # team1 cannot duplicate players within this round
            # team1 cannot duplicate teams within this tourney
            possible_team1 = []
            team1 = None
            for team in all_possible_teams:
                if not team_players_duplicate_in_round(team, single_round_games) and not team_duplicate_in_tourney(team,
                                                                                                                   tourney_rounds):
                    possible_team1.append(team)
            try:
                team1 = choice(possible_team1)
            except:
                pass

            # choose team2
            # team2 cannot duplicate players within this round (don't forget team1!)
            # team2 cannot duplicate teams within this tourney
            possible_team2 = []
            team2 = None
            for team in all_possible_teams:
                if not team_players_duplicate_in_round(team, single_round_games) and not team_duplicate_in_tourney(team,
                                                                                                                   tourney_rounds) and team.p1 not in team1 and team.p2 not in team1:
                    possible_team2.append(team)
            try:
                team2 = choice(possible_team2)
            except:
                pass

            # create game, add to round
            if team1 is not None and team2 is not None:
                single_round_games.append(Game(team1, team2))

        if len(single_round_games) == (cfg['num_players'] // 4):
            tourney_rounds.append(single_round_games)
        cfg['num_rounds'] -= 1
    return tourney_rounds


if __name__ == "__main__":
    tourney = create_tourny()

    with open('tourny_{}.txt'.format(datetime.datetime.now().strftime('%Y%m%d')), 'w') as file:
        file.write('KQOC Tournament Generator\n\n')
        i = 1
        for vb_round in tourney:
            file.write("round {}:\n".format(i))
            for game in vb_round:
                file.write(str(game) + ': \n')
            i += 1
            file.write('\n')
