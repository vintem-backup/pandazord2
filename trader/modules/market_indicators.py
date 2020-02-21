#TODO: Docstrings and Type annotations

class Trend:

    def __init__(self, price_series_in):

        self.price_series_in = price_series_in


    def simple_moving_average(self, number_of_samples):

        return self.price_series_in.rolling(number_of_samples).mean()


class Momentum:
    pass


class Volatility:
    pass


class Volume:
    pass