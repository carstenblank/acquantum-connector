from typing import List


class Gate(object):

    def __init__(self):
        # type: () -> None
        self.gateDetail = {}

    def set_gate_details(self, gate_details):
        # type: (dict) -> None
        self.gateDetail = gate_details


class HGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super(HGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'H'


class XGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super(XGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'X'


class YGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super(YGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'Y'


class ZGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super(ZGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'Z'


class SGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super(SGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'S'


class RxGate(Gate):

    def __init__(self, x, y, angle):
        # type: (int, int, int) -> None
        assert (angle in range(0, 361))
        super(RxGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'RX_{}'.format(angle)


class RyGate(Gate):

    def __init__(self, x, y, angle):
        # type: (int, int, int) -> None
        assert (angle in range(0, 361))
        super(RyGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'RY_{}'.format(angle)


class RzGate(Gate):

    def __init__(self, x, y, angle):
        # type: (int, int, int) -> None
        assert (angle in range(0, 361))
        super(RzGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'RZ_{}'.format(angle)


# PHASE
class CPhase(Gate):
    text = 'CP'

    def __init__(self, x, y):
        # type: (List[int], List[int]) -> None
        super(CPhase, self).__init__()
        self.x = x
        self.y = y
        self.text = 'CP'
        self.dict()

    def dict(self):
        obj = {'text': self.text, 'gateDetail': self.gateDetail}
        for index, value in enumerate(self.x):
            obj['x{}'.format('' if index == 0 else index)] = value
        for value, index in enumerate(self.y):
            obj['y{}'.format('' if index == 0 else index)] = value
        self.__dict__ = obj


class CCPhase(Gate):
    text = 'CCP'

    def __init__(self, x, y):
        # type: (List[int], List[int]) -> None
        super(CCPhase, self).__init__()
        self.x = x
        self.y = y
        self.text = 'CCP'
        self.dict()

    def dict(self):
        obj = {'text': self.text, 'gateDetail': self.gateDetail}
        for index, value in enumerate(self.x):
            obj['x{}'.format('' if index == 0 else index)] = value
        for index, value in enumerate(self.y):
            obj['y{}'.format('' if index == 0 else index)] = value
        self.__dict__ = obj


class Measure(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super(Measure, self).__init__()
        self.x = x
        self.y = y
        self.text = 'M'
