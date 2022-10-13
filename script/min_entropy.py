import sys
import os
sys.path.append(os.path.join(os.path.split(os.path.realpath(__file__))[0], ".."))
import qrng.daq as daq
import numpy as np


DAQ_CARD = "PCIe-1816H,BID#0"


def main():
    pbdaq = daq.PseudoBufferedDAQ(DAQ_CARD)
    pbdaq.init_device(n_signals=1048576)

    signals = pbdaq.next()

    ps = np.zeros(65536)
    for signal in signals:
        ps[signal] += 1
    ps = np.vectorize(lambda p: p/1048576.0)(ps)

    h_min = np.floor(-np.log2(ps.max()))
    print(h_min)


if __name__ == "__main__":
    main()
