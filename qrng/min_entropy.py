import numpy as np
from .daq import DAQ_RES


def min_entropy(signals: np.ndarray):
    ps = np.zeros(DAQ_RES)
    for signal in signals:
        ps[signal] += 1
    ps = np.vectorize(lambda p: p/len(signals))(ps)

    return np.floor(-np.log2(ps.max()))
