import abc
import numpy
import Automation.BDaq as BDaq
from Automation.BDaq.InstantAiCtrl import InstantAiCtrl


DAQ_CARD = "PCIe-1816H,BID#0"


class AbstractInstantDAQ(abc.ABC):
    def __init__(self, device_id: str) -> None:
        super().__init__()
        self.device_id = device_id

    @abc.abstractmethod
    def init_device(self) -> None:
        return NotImplemented

    @abc.abstractmethod
    def next(self) -> float:
        return NotImplemented



class InstantDAQ(AbstractInstantDAQ):
    def __init__(self, device_id: str) -> None:
        super().__init__(device_id)
        self.instant_ai_ctrl = InstantAiCtrl(self.device_id)

    def init_device(self) -> None:
        self.instant_ai_ctrl.channels[0].signalType = BDaq.AiSignalType.SingleEnded
        self.instant_ai_ctrl.channels[0].valueRange = BDaq.ValueRange.V_Neg10To10

    def next(self) -> float:
        _, signals = self.instant_ai_ctrl.readDataF64(0, 1) # start_ch = 0; ch_count = 1

        return signals[0]
