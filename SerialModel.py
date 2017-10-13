#!/usr/bin/env python3.3

def meanpers(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

class SerialModel:

    def __init__(self):
        self.serie = []
        self.TwelveDayEMA = []
        self.TwenSixDayEMA = []
        self.MACD = []
        self.signal = []
        self.histogram = []

    def UpdateSerie(self):

        idx = len(self.serie) - 1
        val = self.serie[idx]

        # update Twelve Day EMA
        if idx < 11:
            self.TwelveDayEMA.append(None)
        if idx == 11:
            self.TwelveDayEMA.append(meanpers(self.serie[0: (idx + 1)]))
        if idx > 11:
            self.TwelveDayEMA.append((val * (2.0 / (12 + 1)) + self.TwelveDayEMA[idx - 1] * (1 - (2.0 / (12 + 1)))))

        # update TwenSix day EMA / MACD
        if idx < 25:
            self.TwenSixDayEMA.append(None)
            self.MACD.append(None)
        if idx == 25:
            self.TwenSixDayEMA.append(meanpers(self.serie[0:(idx + 1)]))
            self.MACD.append(self.TwelveDayEMA[idx] - self.TwenSixDayEMA[idx])
        if idx > 25:
            self.TwenSixDayEMA.append(val * (2.0 / (26 + 1)) + self.TwenSixDayEMA[idx - 1] * (1 - (2.0 / (26 + 1))))
            self.MACD.append(self.TwelveDayEMA[idx] - self.TwenSixDayEMA[idx])

        # update signal
        if idx < 33:
            self.signal.append(None)
            self.histogram.append(None)
        if idx == 33:
            self.signal.append(meanpers(self.MACD[25:idx + 1]))
            self.histogram.append(self.MACD[idx] - self.signal[idx])
        if idx > 33:
            self.signal.append(self.MACD[idx] * (2.0 / (9 + 1)) + self.signal[idx - 1] * (1 - (2.0 / (9 + 1))))
            self.histogram.append(self.MACD[idx] - self.signal[idx])

    def AddVal(self, val):
        self.serie.append(val)
        self.UpdateSerie()
