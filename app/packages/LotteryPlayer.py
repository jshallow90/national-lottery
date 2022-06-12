from app.packages.Winnings import Winnings
from app.packages.NationalLottery import NationalLottery
from app.utils import get_logger as gl

logger = gl.get_default_logger('LotteryTicket')
logger.setLevel('INFO')
COST_PER_GAME = 2


class LotteryPlayer(object):
    """
    Class to hold a users' lottery numbers and to check these against the NationLottery class numners
    The way to play national lottery:
        - pick 6 numbers plus bonus ball
        - numbers must be between 1-59
        - game is played twice a week and costs £2
        - numbers are picked at random and once a random is picked, it cannot be selected again

    A win is determined in the following screnarios:
        6: 6 numbers = jackpot
        5: 5 numbers + bb = £1m
        4: 5 numbers = £1750
        3: 4 numbers = £140
        2: 3 numbers = £30
        1: 2 numbers = free lucky dip (replay)

    Attributes:
        numbers: user nunber selection numbers must be between 1-59 and must be unique.
        money_spent: £2 per game per play
        games_played: number of lotto tickets purchased
        results: collection of results expressed in terms of Winnings enum
    Methods:
        check_winning_numbers(NationalLottery): function to check user numbers against the national lottery numbers
                                                returns enum from Winnings (6=jackpot ... 1=lucky dip).
    """
    def __init__(self, numbers: tuple):
        if any([numbers.count(x) > 1 for x in numbers]):
            raise ValueError("Duplicate values are not allowed in lottery ball selection")
        if any([x not in range(1, 60) for x in numbers]):
            raise ValueError("Numbers must be between 1 and 59")

        self.numbers = numbers
        self.money_spent = COST_PER_GAME
        self.games_played = 1
        self.results = {e: 0 for e in Winnings}
        logger.debug(f"Class initialized with main balls: {self.numbers}")

    def __repr__(self):
        return f"LotteryTicket(numbers={self.numbers})"

    def check_winning_numbers(self, national: NationalLottery):
        matches = set(national.main_balls).intersection(set(self.numbers))
        logger.debug(f"Matches between {self} and {national} is {matches}")
        num_matches = len(matches)
        if num_matches < 2:
            return Winnings.no_payout
        elif num_matches == 2:
            return Winnings.lucky_dip
        elif num_matches == 3:
            return Winnings.three_numbers
        elif num_matches == 4:
            return Winnings.four_numbers
        elif num_matches == 5:
            # if 5 matches, check bonus ball
            if national.bonus_ball in self.numbers:
                return Winnings.five_numbers_bb
            else:
                return Winnings.five_numbers
        elif num_matches == 6:
            return Winnings.jackpot

    def accumulate_lottery_tries(self, ending_combo: Winnings = Winnings.jackpot):
        national_selection = NationalLottery()
        draw_number = self.check_winning_numbers(national_selection)

        while draw_number != ending_combo:
            self.games_played += 1
            self.money_spent += COST_PER_GAME
            self.results[draw_number] += 1

            logger.info(f"Total games played {self.games_played}, total costs {self.money_spent}, "
                        f"number of weeks played {self.games_played}, number of years played "
                        f"{self.games_played // 52}, {self.results}")
            national_selection = NationalLottery()
            draw_number = self.check_winning_numbers(national_selection)

        # include final jackpot
        self.results[draw_number] += 1
