import abc
import numpy as np

import Automation.BDaq as BDaq
from Automation.BDaq.InstantAiCtrl import InstantAiCtrl


class AbstractInstantDAQ(abc.ABC):
    def __init__(self, device_id: str) -> None:
        super().__init__()
        self.device_id = device_id

    @abc.abstractmethod
    def init_device(self) -> None:
        return NotImplemented

    @abc.abstractmethod
    def next(self) -> np.uint16:
        return NotImplemented



class InstantDAQ(AbstractInstantDAQ):
    def __init__(self, device_id: str) -> None:
        super().__init__(device_id)
        self.instant_ai_ctrl = None
        self.ai_delta_v = 20/65536

    def init_device(self) -> None:
        self.instant_ai_ctrl = InstantAiCtrl(self.device_id)
        self.instant_ai_ctrl.channels[0].signalType = BDaq.AiSignalType.SingleEnded
        self.instant_ai_ctrl.channels[0].valueRange = BDaq.ValueRange.V_Neg10To10

    def next(self) -> np.uint16:
        _, signals = self.instant_ai_ctrl.readDataF64(chStart=0, chCount=1)

        return np.uint16(np.floor((signals[0]+10) / self.ai_delta_v))


class PseudoInstantDAQ(AbstractInstantDAQ):
    def __init__(self, device_id: str) -> None:
        super().__init__(device_id)
        self.ai_delta_v = 20/65536
        
    def init_device(self) -> None:
        ...

    def next(self) -> np.uint16:
        rand_signal = np.random.normal(loc=0.0, scale=1.0)
        while not -10 <= rand_signal <= 10:
            rand_signal = np.random.normal(loc=0.0, scale=1.0)

        return np.uint16(np.floor((rand_signal+10) / self.ai_delta_v))
