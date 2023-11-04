import random

from eventvec.server.data.factuality.factuality_readers.factuality_reader import FactualityReader  # noqa


class FactualityDatahandler:
    def __init__(self):
        self._factuality_reader = FactualityReader()

    def load(self):
        data = self._factuality_reader.belief_data().data()
        random.seed(42)
        random.shuffle(data)
        data_len = len(data)
        train_len = int(data_len * 0.8)
        self._train_data = data[:train_len]
        self._test_data = data[train_len:]

    def train_data(self):
        return self._train_data

    def test_data(self):
        return self._test_data
