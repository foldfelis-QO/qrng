import abc
import numpy as np

import Automation.BDaq as BDaq
from Automation.BDaq.InstantAiCtrl import InstantAiCtrl
from Automation.BDaq.WaveformAiCtrl import WaveformAiCtrl


class AbstractInstantDAQ(abc.ABC):
    def __init__(self, device_id: str) -> None:
        super().__init__()
        self.device_id = device_id
        self.instant_ai_ctrl = None
        self.ai_delta_v = 20.0/65536.0

    def encode(self, signal: float) -> np.uint16:
        return np.uint16(np.floor((signal+10) / self.ai_delta_v))

    @abc.abstractmethod
    def init_device(self) -> None:
        return NotImplemented

    @abc.abstractmethod
    def next(self) -> np.uint16:
        return NotImplemented

    @abc.abstractmethod
    def dispose(self) -> None:
        return NotImplemented


class InstantDAQ(AbstractInstantDAQ):
    def init_device(self) -> None:
        self.instant_ai_ctrl = InstantAiCtrl(self.device_id)
        self.instant_ai_ctrl.channels[0].signalType = BDaq.AiSignalType.SingleEnded
        self.instant_ai_ctrl.channels[0].valueRange = BDaq.ValueRange.V_Neg10To10

    def next(self) -> np.uint16:
        _, signals = self.instant_ai_ctrl.readDataF64(chStart=0, chCount=1)

        return self.encode(signals[0])

    def dispose(self) -> None:
        self.instant_ai_ctrl.dispose()


class PseudoInstantDAQ(AbstractInstantDAQ):
    def init_device(self) -> None:
        ...

    def next(self) -> np.uint16:
        rand_signal = np.random.normal(loc=0.0, scale=1.0)
        while not -10 <= rand_signal <= 10:
            rand_signal = np.random.normal(loc=0.0, scale=1.0)

        return self.encode(rand_signal)

    def dispose(self) -> None:
        ...


class AbstractBufferedDAQ(abc.ABC):
    def __init__(self, device_id: str) -> None:
        super().__init__()
        self.device_id = device_id
        self.waveform_ai_ctrl = None
        self.n_signals = 0
        self.ai_delta_v = 20.0/65536.0

    def encode(self, signals: list) -> np.ndarray:
        return np.vectorize(
            lambda signal: np.uint16(np.floor((signal+10) / self.ai_delta_v))
        )(np.array(signals))

    @abc.abstractmethod
    def init_device(self, n_signals: int) -> None:
        return NotImplemented

    @abc.abstractmethod
    def next(self) -> np.ndarray:
        return NotImplemented

    @abc.abstractmethod
    def dispose(self) -> None:
        return NotImplemented

class BufferedDAQ(AbstractBufferedDAQ):
    def init_device(self, n_signals: int) -> None:
        self.n_signals = n_signals
        self.waveform_ai_ctrl = WaveformAiCtrl(self.device_id)

        self.waveform_ai_ctrl.conversion.channelStart = 0
        self.waveform_ai_ctrl.conversion.channelCount = 1
        self.waveform_ai_ctrl.conversion.clockRate = 5000000.0

        self.waveform_ai_ctrl.record.sectionCount = 1 # 0 means setting 'streaming' mode
        self.waveform_ai_ctrl.record.sectionLength = n_signals

        self.waveform_ai_ctrl.channels[0].signalType = BDaq.AiSignalType.SingleEnded
        self.waveform_ai_ctrl.channels[0].valueRange = BDaq.ValueRange.V_Neg10To10

    def next(self) -> np.ndarray:
        self.waveform_ai_ctrl.prepare()
        self.waveform_ai_ctrl.start()

        result = self.waveform_ai_ctrl.getDataF64(count=self.n_signals, timeout=-1)  # timeout=-1 meaning infinite waiting
        _, _, signals = result

        return self.encode(signals)

    def dispose(self) -> None:
        self.waveform_ai_ctrl.dispose()


class PseudoBufferedDAQ(AbstractBufferedDAQ):
    def init_device(self, n_signals: int) -> None:
        self.n_signals = n_signals

    def next(self) -> np.ndarray:
        rand_signals = np.empty(self.n_signals)
        for i in range(len(rand_signals)):
            rand_signals[i] = np.random.normal(loc=0.0, scale=1.0)
            while not -10 <= rand_signals[i] <= 10:
                rand_signals[i] = np.random.normal(loc=0.0, scale=1.0)

        return self.encode(rand_signals)

    def dispose(self) -> None:
        ...
