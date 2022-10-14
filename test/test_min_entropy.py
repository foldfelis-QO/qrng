import qrng.min_entropy as h
import qrng.daq as daq


DAQ_CARD = "PCIe-1816H,BID#0"


def test_min_entropy():
    pbdaq = daq.PseudoBufferedDAQ(DAQ_CARD)
    pbdaq.init_device(n_signals=1048576)

    signals = pbdaq.next()

    assert h.min_entropy(signals) == 12
