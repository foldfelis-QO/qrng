import qrng.stats as stats
import qrng.daq as daq


DAQ_CARD = "PCIe-1816H,BID#0"


def test_min_entropy():
    pbdaq = daq.PseudoBufferedDAQ(DAQ_CARD)
    pbdaq.init_device(n_signals=1048576)

    signals = pbdaq.next()


    assert stats.min_entropy(stats.pmf(signals)) == 12
