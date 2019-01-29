from typing import List, Union


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
        if x <= 0:
            raise ValueError('x - coordinate must be greater 0')
        if y <= 0:
            raise ValueError('y - coordinate must be greater 0')
        super(HGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'H'


class XGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        if x <= 0:
            raise ValueError('x - coordinate must be greater 0')
        if y <= 0:
            raise ValueError('y - coordinate must be greater 0')
        super(XGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'X'


class YGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        if x <= 0:
            raise ValueError('x - coordinate must be greater 0')
        if y <= 0:
            raise ValueError('y - coordinate must be greater 0')
        super(YGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'Y'


class ZGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        if x <= 0:
            raise ValueError('x - coordinate must be greater 0')
        if y <= 0:
            raise ValueError('y - coordinate must be greater 0')
        super(ZGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'Z'


class SGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        if x <= 0:
            raise ValueError('x - coordinate must be greater 0')
        if y <= 0:
            raise ValueError('y - coordinate must be greater 0')
        super(SGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'S'


class RxGate(Gate):

    def __init__(self, x, y, angle):
        # type: (int, int, int) -> None
        if angle not in range(0, 361):
            raise ValueError('Angle is not between 0 - 360')
        if x <= 0:
            raise ValueError('x - coordinate must be greater 0')
        if y <= 0:
            raise ValueError('y - coordinate must be greater 0')
        super(RxGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'RX_{}'.format(angle)


class RyGate(Gate):

    def __init__(self, x, y, angle):
        # type: (int, int, int) -> None
        if angle not in range(0, 361):
            raise ValueError('Angle is not between 0 - 360')
        if x <= 0:
            raise ValueError('x - coordinate must be greater 0')
        if y <= 0:
            raise ValueError('y - coordinate must be greater 0')
        super(RyGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'RY_{}'.format(angle)


class RzGate(Gate):

    def __init__(self, x, y, angle):
        # type: (int, int, int) -> None
        if angle not in range(0, 361):
            raise ValueError('Angle is not between 0 - 360')
        if x <= 0:
            raise ValueError('x - coordinate must be greater 0')
        if y <= 0:
            raise ValueError('y - coordinate must be greater 0')
        super(RzGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'RZ_{}'.format(angle)


# PHASE
class CPhase(Gate):
    text = 'CP'

    def __init__(self, x, y):
        # type: (Union[List[int], int, (int, int)], Union[List[int], (int,int)]) -> None
        super(CPhase, self).__init__()
        if isinstance(x, int):
            self.x = self.x1 = x
        else:
            if len(set(x)) != 1:
                raise ValueError('X - coordinates not equal or empty')
            if len(x) == 1:
                self.x = self.x1 = x[0]
            else:
                if len(x) is not 2:
                    raise ValueError('X - coordinates greater 2')
                self.x, self.x1 = x

        if len(y) is not 2:
            raise ValueError('number of Y - coordinates unequal 2')
        if len(set(y)) is not 2:
            raise ValueError('Y - coordinates can not be equal')

        self.y, self.y1 = y
        self.text = 'CP'


class CCPhase(Gate):
    text = 'CCP'

    def __init__(self, x, y):
        # type: (Union[List[int], int, (int, int)], Union[List[int], (int,int)]) -> None
        super(CCPhase, self).__init__()
        if isinstance(x, int):
            if x <= 0:
                raise ValueError('x - coordinate must be greater 0')
            self.x = self.x1 = self.x2 = x
        else:
            if len(set(x)) is not 1:
                raise ValueError('X - coordinates not equal or empty')
            if not all(value > 0 for value in x):
                raise ValueError('X - coordinate must be greater 0')
            if len(x) == 1:
                self.x = x[0]
                self.x1 = x[0]
            else:
                if len(x) is not 3:
                    raise ValueError('X - coordinates greater 3')
                self.x, self.x1, self.x2 = x
        if len(y) is not 3:
            raise ValueError('number of Y - coordinates unequal 2')
        if len(set(y)) is not 3:
            raise ValueError('Y - coordinates can not be equal')
        if not all(value > 0 for value in y):
            raise ValueError('Y - coordinate must be greater 0')
        self.y, self.y1, self.y2 = y
        self.text = 'CCP'


class Measure(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        if x <= 0:
            raise ValueError('x - coordinate must be greater 0')
        if y <= 0:
            raise ValueError('y - coordinate must be greater 0')
        super(Measure, self).__init__()
        self.x = x
        self.y = y
        self.text = 'M'


class SDag(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        if x <= 0:
            raise ValueError('x - coordinate must be greater 0')
        if y <= 0:
            raise ValueError('y - coordinate must be greater 0')
        super(SDag, self).__init__()
        self.x = x
        self.y = y
        self.text = 'S†'


class TGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        if x <= 0:
            raise ValueError('x - coordinate must be greater 0')
        if y <= 0:
            raise ValueError('y - coordinate must be greater 0')
        super(TGate, self).__init__()
        self.x = x
        self.y = y
        self.text = 'T'


class TDag(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        if x <= 0:
            raise ValueError('x - coordinate must be greater 0')
        if y <= 0:
            raise ValueError('y - coordinate must be greater 0')
        super(TDag, self).__init__()
        self.x = x
        self.y = y
        self.text = 'T†'
