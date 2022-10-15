import numpy as np
from .daq import DAQ_RES


def pmf(signals: np.ndarray):
    counts = np.zeros(DAQ_RES)
    for signal in signals:
        counts[signal] += 1

    probs = np.vectorize(lambda count: count/len(signals))(counts)

    return probs


def min_entropy(pmf: np.ndarray):
    return np.int64(np.floor(-np.log2(pmf.max())))
