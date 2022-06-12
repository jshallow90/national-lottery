from app.packages.Winnings import Winnings
from app.packages.LotteryPlayer import LotteryPlayer
from app.utils import get_logger as gl

logger = gl.get_default_logger(__name__)
logger.setLevel('INFO')
COST_PER_GAME = 2


if __name__ == '__main__':
    user_numbers = (1, 4, 9, 27, 49, 6)

    user_lottery = LotteryPlayer(user_numbers)
    user_lottery.accumulate_lottery_tries(Winnings.four_numbers)
    print(user_lottery.results)
