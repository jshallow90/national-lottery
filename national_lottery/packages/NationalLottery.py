import random

from national_lottery.utils import get_logger as gl

logger = gl.get_default_logger('NationalLottery')
logger.setLevel('INFO')


class NationalLottery(object):
    def __init__(self, numbers: tuple=None):
        if numbers:
            self.main_balls = numbers
            self.bonus_ball = None
        else:
            main_balls, bonus = self.draw_lottery_numbers()
            self.main_balls = main_balls
            self.bonus_ball = bonus

        if any([self.main_balls.count(x) > 1 for x in self.main_balls]):
            raise ValueError("Duplicate values are not allowed in lottery ball selection")

        if self.bonus_ball in self.main_balls:
            raise ValueError("Bonus ball must be different from main ball selection")

        logger.debug(f"Class initialized with main balls: {self.main_balls} and bonus ball {self.bonus_ball}")

    def __repr__(self):
        return f"NationalLottery(numbers={self.main_balls}, bonus_ball={self.bonus_ball})"

    @staticmethod
    def get_available_numnbers():
        return list(range(1, 60))

    def draw_lottery_numbers(self):
        available_numbers = self.get_available_numnbers()
        main_balls = []

        for i in range(6):
            lottery_number = random.choice(available_numbers)
            main_balls.append(lottery_number)
            available_numbers.remove(lottery_number)

        main_balls.sort()
        main_balls = tuple(main_balls)
        bonus_ball = random.choice(available_numbers)

        return main_balls, bonus_ball
