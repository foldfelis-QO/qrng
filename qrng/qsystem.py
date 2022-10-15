import numpy as np
from . import daq
from . import stats
from . import toeplitz


class QSystem:
    def __init__(
        self,
        bdaq: daq.AbstractBufferedDAQ,
        idaq: daq.AbstractInstantDAQ,
        n_signals_for_estimation: int,
    ) -> None:
        self.bdaq = bdaq
        self.idaq = idaq
        self.n_signals_for_estimation = n_signals_for_estimation
        self.signals = None
        self.pmf = None
        self.min_entropy = 0
        self.encoder = None

    def estimate(self) -> None:
        self.bdaq.init_device(n_signals=self.n_signals_for_estimation)
        self.signals = self.bdaq.next()
        self.pmf = stats.pmf(self.signals)
        self.min_entropy = stats.min_entropy(self.pmf)
        self.bdaq.dispose()

        self.encoder = toeplitz.Toeplitz((self.signals[0], self.signals[1]), daq.NBITS, self.min_entropy)

        self.idaq.init_device()

    def rand(self) -> int:
        return self.encoder.hash(self.idaq.next())
