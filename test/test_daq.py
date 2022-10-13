import qrng.daq as daq
import numpy as np


DAQ_CARD = "PCIe-1816H,BID#0"


def test_pseudo_instant_daq():
    pidaq = daq.PseudoInstantDAQ(DAQ_CARD)
    pidaq.init_device()

    assert isinstance(pidaq.next(), np.uint16)
    assert 0 <= pidaq.next() < 65536

    signals = np.empty(1048576)
    for i in range(len(signals)):
        signals[i] = pidaq.next()

    # the mean of signals should be around the middle of 0 to 2**16
    assert abs(signals.sum()/len(signals) - 65536/2.0) < 10
