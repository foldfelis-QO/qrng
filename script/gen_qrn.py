
import sys, os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], ".."))

import qrng.daq as daq
from qrng.qsystem import QSystem

import numpy as np
import matplotlib.pyplot as plt


DAQ_CARD = "PCIe-1816H,BID#0"


if __name__ == "__main__":
    qsys = QSystem(daq.PseudoBufferedDAQ(DAQ_CARD), daq.PseudoInstantDAQ(DAQ_CARD), 2097152)
    qsys.estimate()

    qrns = [qsys.rand() for _ in range(2097152)]


    signals_counts = np.bincount(qsys.signals, minlength=daq.DAQ_RES)
    qrns_counts = np.bincount(qrns, minlength=2**qsys.min_entropy)

    plt.plot(signals_counts)
    plt.plot(qrns_counts)
    plt.savefig("a.png")
