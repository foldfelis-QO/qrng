import numpy as np
from . import daq
from . import stats


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
        self.delta_signal = 0.0

    def estimate(self) -> None:
        self.bdaq.init_device(n_signals=self.n_signals_for_estimation)
        self.signals = self.bdaq.next()
        self.pmf = stats.pmf(self.signals)
        self.min_entropy = stats.min_entropy(self.pmf)
        self.delta_signal = daq.DAQ_RES / 2**self.min_entropy
        self.bdaq.dispose()

        self.idaq.init_device()

    def encode(self, signal: np.uint16) -> np.uint16:
        # TODO: signal = hash(signal)
        return np.uint16(np.floor(signal / self.delta_signal))

    def rand(self) -> np.uint16:
        return self.encode(self.idaq.next())
