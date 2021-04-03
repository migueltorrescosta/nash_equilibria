class Player:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    @abstractmethod
    def move(self):
        pass


# Always contributes half of their wealth
class half(Player):
    def move(self, status):
        return .5

# Always contributes all their wealth


class everything(Player):
    def move(self, status):
        return 1

# Always contributes 90% of their wealth


class ninety_percentile(Player):
    def move(self, status):
        return .9

# Always contributes 10% of their wealth


class tenth_percentile(Player):
    def move(self, status):
        return .1

# Contributes an uniformly random amount of their wealth


class uniformly_random(Player):
    def move(self, status):
        return random.random()

# Contributes a weird amount


class two_over_n_players(Player):

    def __init__(self, name):
        self.name = name
        self.initial_number_of_players = None

    def move(self, status):
        if not self.initial_number_of_players:
            self.initial_number_of_players = status.n_players
        return 2*(1 - status.n_players/self.initial_number_of_players)

# In the first random it contributes a random amount, otherwise it contributes everything


class everything_except_on_initial(Player):

    def __init__(self, name):
        self.name = name
        self.is_first_move = True

    def move(self, status):
        if self.is_first_move:
            self.is_first_move = False
            return random.random()
        else:
            return 1

# Contributes an amount that converges to 1 exponentially


class exponential_decay(Player):

    def __init__(self, name):
        self.name = name
        self.initial_number_of_players = None

    def move(self, status):

        if not self.initial_number_of_players:
            self.initial_number_of_players = status.n_players

        return 1 - 0.3**(1 + self.initial_number_of_players - status.n_players)

# First round it contributes an uniformly random amount, after that it contributes the minimum needed to ensure survival.


class slightly_more(Player):

    def __init__(self, name):
        self.name = name
        self.is_first_move = True

    def move(self, status):
        if self.is_first_move:
            self.is_first_move = False
            return random.random()
        else:
            least_money = min(status.money.values())
            return least_money/status.my_money(self) + 10e-9
