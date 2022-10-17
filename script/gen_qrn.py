
import sys, os
REPO_PATH = os.path.join(os.path.split(os.path.realpath(__file__))[0], "..")
sys.path.append(REPO_PATH)

import qrng.daq as daq
from qrng.qsystem import QSystem

import numpy as np
import matplotlib.pyplot as plt


DAQ_CARD = "PCIe-1816H,BID#0"


if __name__ == "__main__":
    print("estimating system")
    # qsys = QSystem(daq.PseudoBufferedDAQ(DAQ_CARD), daq.PseudoInstantDAQ(DAQ_CARD), 2097152)
    qsys = QSystem(daq.BufferedDAQ(DAQ_CARD), daq.InstantDAQ(DAQ_CARD), 2097152)
    qsys.estimate()
    print(f"min_entropy: {qsys.min_entropy}")

    print("get rns")
    qrns = [qsys.rand() for _ in range(2097152)]

    print("analize")
    signals_counts = np.bincount(qsys.signals, minlength=daq.DAQ_RES)
    qrns_counts = np.bincount(qrns, minlength=2**qsys.min_entropy)

    print("plot")
    plt.cla()
    plt.plot(signals_counts)
    # plt.savefig(os.path.join(REPO_PATH, "gallery/pseudo_signals.png"))
    plt.savefig(os.path.join(REPO_PATH, "gallery/signals.png"))

    plt.cla()
    plt.plot(qrns_counts)
    # plt.savefig(os.path.join(REPO_PATH, "gallery/pseudo_rns.png"))
    plt.savefig(os.path.join(REPO_PATH, "gallery/rns.png"))


# DAQ_CARD = "PCIe-1816H,BID#0"
# import qrng.daq as daq
# from qrng.qsystem import QSystem
# qsys = QSystem(daq.BufferedDAQ(DAQ_CARD), daq.InstantDAQ(DAQ_CARD), 2097152)
# qsys.estimate()
