from itertools import combinations
from random import shuffle
from random import choice
import yaml
import datetime


class Game():
    def __init__(self, t1, t2):
        if t1.p1 in t2 or t1.p2 in t2:
            raise ValueError("can't have a game with same person on both teams")
        else:
            self.t1 = t1
            self.t2 = t2

    def __contains__(self, item):
        # item is a team
        return self.t1 == item or self.t2 == item

    def __str__(self):
        return "{} vs {}".format(str(self.t1), str(self.t2))

    def __eq__(self, other):
        return self.t1 in other and self.t2 in other


class Team():
    # no need for duplicate player error checking. combinations() won't give duplicate player team. ex P01 P01
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    # overrides the "x in y" phrase! :)
    # check player in team. "item" is a player (int)
    def __contains__(self, item):
        return self.p1 == item or self.p2 == item

    def __str__(self):
        return "(P{:02}, P{:02})".format(self.p1, self.p2)

    def __eq__(self, other):
        return self.p1 in other and self.p2 in other


def create_tourny():
    with open("kqoc.yaml", 'r') as yml:
        cfg = yaml.load(yml, Loader=yaml.FullLoader)

    # list of ints ex: [1, 2, 3, 4]
    players = [x for x in range(1, cfg['num_players'] + 1)]
    print("Number of players: {}".format(cfg['num_players']))

    # list of team objects
    all_possible_teams = [Team(x, y) for x, y in combinations(players, 2)]
    print("Number of possible teams: " + str(len(all_possible_teams)))

    # list of game objects
    all_possible_games = []
    for x in all_possible_teams:
        for y in all_possible_teams:
            try:
                if Game(x, y) not in all_possible_games:
                    all_possible_games.append(Game(x, y))
            except(ValueError):
                pass  # same players on opposite teams not possible
    print("Number of possible games: {}\n".format(str(len(all_possible_games))))
    # print(*all_possible_games, sep='\n')

    removed_teams = [] # used to track removals
    while(cfg['num_rounds'] and len(all_possible_teams)):
        # choose a random team
        team_1 = choice(all_possible_teams)
        # temp remove other teams with duplicate players
        temp_teams = all_possible_teams.copy()
        temp_teams = [x for x in all_possible_teams if team_1.p1 not in x and team_1.p2 not in x]
        # choose other team, create game.
        # restore temp removals
        # remove that team from all_teams
        removed_teams.append(team_1)
        all_possible_teams.remove(team_1)



















    # randomly create rounds of games
    # TODO: make it so the same person can't be left out of multiple games before everyone else has been left out
    # TODO: add capability to demand certain games before generation starts by placing info in yaml
    rounds = []  # each round is list of games. rounds is a list of these lists
    while (cfg['num_rounds'] and len(all_possible_games)):
        round_games = all_possible_games.copy()
        shuffle(round_games)
        round = []  # list of games
        for i in range(cfg['num_players'] // 4):  # numbers of games in each round is num_players / 4
            try:
                tempgame = round_games[0]
                # remove tempgame from all_games, remove all games with those teams
                all_possible_games.remove(tempgame)
                all_possible_games = [x for x in all_possible_games if tempgame.t1 not in x and tempgame.t2 not in x]
                # remove tempgame from round_games, remove all game with those players
                round_games.remove(tempgame)
                round_games = [x for x in round_games
                               if tempgame.t1.p1 not in x.t1 and tempgame.t1.p1 not in x.t2 and
                               tempgame.t1.p2 not in x.t1 and tempgame.t1.p2 not in x.t2 and
                               tempgame.t2.p1 not in x.t1 and tempgame.t2.p1 not in x.t2 and
                               tempgame.t2.p2 not in x.t1 and tempgame.t2.p2 not in x.t2]
                round.append(tempgame)
            except IndexError:
                print("IndexError. allposgames has {} items. round_games has {} items.".format(len(all_possible_games),
                                                                                               len(round_games)))
        cfg['num_rounds'] -= 1
        rounds.append(round)

    with open('tourny_{}.txt'.format(datetime.datetime.now().strftime('%Y%m%d')), 'w') as file:
        file.write('KQOC Tournament Generator\n\n')
        i = 1
        for round in rounds:
            file.write("round {}:\n".format(i))
            for game in round:
                file.write(str(game) + ': \n')
            i += 1
            file.write('\n')


if __name__ == "__main__":
    create_tourny()