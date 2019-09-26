import numpy as np
import random
from blackjack_game import BlackjackGame


class SimulateBlackjack:
    game = ()
    player_wins = False
    push = False

    def __init__(self):
        self.game = BlackjackGame()

    def play(self):
        self.player_wins = False
        self.push = False

        self.game.deal_cards()
        if self.game.best_move() == 'blackjack':
            self.player_wins = True
            return

        elif self.game.best_move() == 'dealer_blackjack':
            self.player_wins = False
            return

        else:
            while self.game.best_move() is 'hit':
                self.game.hit(True)

            if self.game.did_bust(True):
                self.player_wins = False
            else:
                self.game.stand()
                player_total, dealer_total = self.game.get_totals()
                if self.game.did_bust(False):
                    self.player_wins = True
                elif player_total > dealer_total:
                    self.player_wins = True
                else:
                    if player_total == dealer_total:
                        self.push = True
                    self.player_wins = False

    def did_player_win(self):
        return self.player_wins

    def did_player_win_or_push(self):
        return self.player_wins or self.push

    def __str__(self):
        return f"""
        {self.game}

        {'Player wins' if self.player_wins else 'Dealer wins' if not self.push else 'Push'}
        {'PLAYER BLACKJACK' if self.game.best_move() == 'blackjack' else ''}
        """


game = SimulateBlackjack()

games_won = []
games_won_or_draw = []

for i in range(10000):
    game.play()
    games_won.append(game.did_player_win())
    games_won_or_draw.append(game.did_player_win_or_push())

print(np.mean(games_won))
print(np.mean(games_won_or_draw))
