import random
import pandas as pd
from abc import ABC, abstractmethod
import seaborn as sns
import itertools
cm = sns.light_palette("green", as_cmap=True)


class LiarsGame:
    def __init__(self, initial_money, players, verbose=False):

        assert players
        assert len(players) == len(
            {player.name for player in players}), "You have different players with the same name"
        assert len(players) > 2, "You need at least 3 players to start a game"
        assert initial_money > 0

        # Secret attributes
        self.__players = players
        self.__money = {player: initial_money for player in players}
        self.__game_history = pd.DataFrame(
            columns=[player.name for player in players],
            index=[],
            data=0
        )
        self.__verbose = verbose
        self.__run_game()

    def __repr__(self):
        return f"LiarsGame: {self.n_players} with {self.total_money}¥"

    def __weight(self, coin_list):
        return sum([self.__coin_weights[i] for i in coin_list])

    # Accessible attributes
    @property
    def money(self):
        return self.__money

    @property
    def total_money(self):
        return sum(self.__money.values())

    @property
    def players(self):
        return self.__players

    @property
    def n_players(self):
        return len(self.__players)

    @property
    def game_history(self):
        return self.__game_history

    def show_game_history(self):
        return self.__game_history.T.style.background_gradient(cmap=cm).set_precision(2).highlight_null('red')

    def my_money(self, player):
        return self.__money[player]

    # Key Methods

    def __run_round(self):

        self.__game_history.loc[self.n_players] = {
            player.name: self.money[player] for player in self.players}

        current_move = {
            player: max([min([player.move(self), 1]), 0])*self.money[player]
            for player in self.players
        }

        if self.__verbose:
            for player in self.players:
                print(
                    f"{player.name}: {current_move[player]:.2f} / {self.money[player]:.2f}")
            print("\n" + "="*50 + "\n")

        smallest_contributor = min(self.players, key=current_move.__getitem__)
        current_move[smallest_contributor] = self.__money[smallest_contributor]
        pot = sum(current_move.values())
        self.__players = [
            player for player in self.__players if player != smallest_contributor]
        self.__money = {
            player: self.__money[player] -
            current_move[player] + pot/self.n_players
            for player in self.players
        }

    def __run_game(self):
        while self.n_players > 1:
            self.__run_round()

        winner = self.players[0]
        self.__game_history.loc[1] = {winner.name: self.money[winner]}

        print(f"Winner: {winner.name}")

        return winner.name


class Player:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    @abstractmethod
    def move(self):
        pass


class half(Player):
    def move(self, status):
        return .5


class everything(Player):
    def move(self, status):
        return 1


class ninety_percentile(Player):
    def move(self, status):
        return .9


class tenth_percentile(Player):
    def move(self, status):
        return .1


class uniformly_random(Player):
    def move(self, status):
        return random.random()


class two_over_n_players(Player):

    def __init__(self, name):
        self.name = name
        self.initial_number_of_players = None

    def move(self, status):
        if not self.initial_number_of_players:
            self.initial_number_of_players = status.n_players
        return 2*(1 - status.n_players/self.initial_number_of_players)


class everything_except_on_initial(Player):

    def __init__(self, name):
        self.name = name
        self.first_move = True

    def move(self, status):
        if not self.first_move:
            return 1
        else:
            self.first_move = False
            return random.random()


class exponential_decay(Player):

    def __init__(self, name):
        self.name = name
        self.initial_number_of_players = None

    def move(self, status):

        if not self.initial_number_of_players:
            self.initial_number_of_players = status.n_players

        return 1 - 0.1**(1 + self.initial_number_of_players - status.n_players)


if __name__ == "__main__":
    initial_money = 100
    strategies = [
        half,
        ninety_percentile,
        tenth_percentile,
        two_over_n_players,
        uniformly_random,
        everything,
        everything_except_on_initial,
        exponential_decay
    ]
    n_replicas = 2
    players = [
        strategy(name=f"{strategy.__name__}_{i}")
        for (strategy, i) in itertools.product(strategies, range(n_replicas))]

    x = LiarsGame(initial_money=initial_money, players=players)
    x.show_game_history()
