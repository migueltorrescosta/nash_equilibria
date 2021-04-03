class LiarsGame:
    def __init__(self, initial_money, strategies, verbose=False):

        assert len(strategies) > 2, "You need at least 3 players to start a game"
        assert initial_money > 0

        # Secret attributes
        self.__players = [strategy(name=strategy.__name__)
                          for strategy in strategies]
        self.__initial_n_players = len(self.__players)
        self.__money = {player: initial_money for player in self.__players}
        self.__game_history = pd.DataFrame(
            columns=[player.name for player in self.__players],
            index=[],
            data=0
        )
        self.__verbose = verbose
        self.__eliminations = []
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
    def eliminations(self):
        return self.__eliminations

    @property
    def game_history(self):
        return self.__game_history

    def show_game_history_heatmap(self):
        return self.__game_history.T.style.background_gradient(cmap=cm).set_precision(2).highlight_null('red')

    def show_game_history_bar_plot(self):
        return self.__game_history.plot.bar(
            stacked=True,
            figsize=(20, 10),
            width=.95
        ).legend(
            loc="center right",
            bbox_to_anchor=(0, 0.5),
            prop={'size': 18}
        )

    def my_money(self, player):
        return self.__money[player]

    # Key Methods

    def __run_round(self):

        self.__game_history.loc[self.__initial_n_players - self.n_players] = {
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

        lowest_contribution = min(current_move.values())
        smallest_contributor = random.choice([
            player
            for player in self.__players
            if current_move[player] == lowest_contribution
        ])
        self.__eliminations.append(smallest_contributor)
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
        self.__game_history.loc[self.__initial_n_players -
                                self.n_players] = {winner.name: self.money[winner]}
        self.__eliminations.append(winner)
        if self.__verbose:
            print(f"Winner: {winner.name}")

        return winner.name
