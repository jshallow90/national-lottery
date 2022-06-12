from packages.Winnings import Winnings
from packages.NationalLottery import NationalLottery
from national_lottery.utils import get_logger as gl

logger = gl.get_default_logger(__name__)
logger.setLevel('INFO')
COST_PER_GAME = 2

# way to play national lottery:
# - pick 6 numbers plus bonus ball
# - numbers must be between 1-59
# - game is played twice a week and costs £2
# - numbers are picked at random and once a random is picked, it cannot be selected again

# - win in the following screnarios:
#     6: 6 numbers = jackpot
#     5: 5 numbers + bb = £1m
#     4: 5 numbers = £1750
#     3: 4 numbers = £140
#     2: 3 numbers = £30
#     1: 2 numbers = free lucky dip (replay)


def check_winning_numbers(user: NationalLottery, national: NationalLottery):
    matches = set(national.main_balls).intersection(set(user.main_balls))
    logger.debug(f"Matches between {user} and {national} is {matches}")
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
        if national.bonus_ball in user.main_balls:
            return Winnings.five_numbers_bb
        else:
            return Winnings.five_numbers
    elif num_matches == 6:
        return Winnings.jackpot


def accumulate_lottery_tries(user_selections: NationalLottery, ending_combo: Winnings=Winnings.jackpot):
    national_selection = NationalLottery()
    games_played = 1
    money_spent = COST_PER_GAME
    results = {e: 0 for e in Winnings}
    draw_number = check_winning_numbers(user_selections, national_selection)

    while draw_number != ending_combo:
        games_played += 1
        money_spent += COST_PER_GAME
        national_selection = NationalLottery()
        results[draw_number] += 1

        logger.info(f"Total games played {games_played}, total costs {money_spent}, "
                    f"number of weeks played {games_played}, number of years played {games_played // 52}, {results}")
        draw_number = check_winning_numbers(user_selections, national_selection)

    # include final jackpot
    results[draw_number] += 1
    return games_played, money_spent, results


if __name__ == '__main__':
    user_numbers = (1, 4, 9, 27, 49, 6)

    user_lottery = NationalLottery(user_numbers)
    outputs = accumulate_lottery_tries(user_lottery, Winnings.four_numbers)
    print(outputs)
