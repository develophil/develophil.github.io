from enums.PyEnum import MovingTrend
from enums.PyEnum import TradeSignal


class MovingAverageStrategy:
    def __init__(self):
        self.before_ma_values = [0, 0, 0]
        self.current_ma_values = [0, 0, 0]
        self.moving_trend = MovingTrend.NONE
        self.strength = 0
        self.signal = TradeSignal.NONE


    def set_ma_values(self, ma5, ma20, ma60):
        self.before_ma_values = self.current_ma_values
        self.current_ma_values = [ma5, ma20, ma60]
        self.check_moving_trend()
        self.check_strength()


    def get_signal(self):
        ma5 = self.current_ma_values[0]
        ma20 = self.current_ma_values[1]
        ma60 = self.current_ma_values[2]
        if ma5 < ma20 < ma60:
            return TradeSignal.BUY
        elif ma5 > ma20 > ma60:
            return TradeSignal.SELL

    def check_moving_trend(self):
        if self.moving_trend == MovingTrend.NONE:
            self.moving_trend = MovingTrend.RISE

        elif self.moving_trend == MovingTrend.NONE:
            self.moving_trend = MovingTrend.RISE

        elif self.moving_trend == MovingTrend.NONE:
            self.moving_trend = MovingTrend.RISE

        elif self.moving_trend == MovingTrend.NONE:
            self.moving_trend = MovingTrend.RISE

        else:
            self.moving_trend = MovingTrend.RISE




    def check_strength(self):
        self.strength = 0

    def is_ascending(self, ma_list):
        before = -9999999
        ma_values = ma_list | self.current_ma_values
        for ma in ma_values:
            if ma <= before:
                return False
            else:
                before = ma
        return True

    def is_descending(self):
        return self.is_ascending(reversed(self.current_ma_values))

    def get_moving_trend(self):
        return self.moving_trend

    def get_strength(self):
        return self.strength


