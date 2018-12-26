import enum


class TradeFlags(enum.Enum):
    BEFORE_BUY = 10
    BUY = 20
    BEFORE_SELL = 30
    SELL = 40


class MovingTrend(enum.Enum):
    NONE = 'none'
    RISE = 'rise'
    TOP = 'top'
    FALL = 'fall'
    BOTTOM = 'bottom'

class TradeSignal(enum.Enum):
    NONE = 'none'
    WAITING_SELL = 'ws'
    SELL = 'sell'
    WAITING_BUY = 'wb'
    BUY = 'buy'
