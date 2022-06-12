from enum import Enum, unique


@unique
class Winnings(Enum):
    no_payout = 0
    lucky_dip = 1
    three_numbers = 2
    four_numbers = 3
    five_numbers = 4
    five_numbers_bb = 5
    jackpot = 6
