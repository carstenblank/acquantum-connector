#  Copyright (c) 2019.  Carsten Blank
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from typing import List, Union


class Gate(object):

    def __init__(self, x, y):
        # type: (int, int) -> None
        if x <= 0:
            raise ValueError('x - coordinate must be greater 0')
        if y <= 0:
            raise ValueError('y - coordinate must be greater 0')
        self.x = x
        self.y = y
        self.gateDetail = {}

    def set_gate_details(self, gate_details):
        # type: (dict) -> None
        self.gateDetail = gate_details


class HGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super().__init__(x, y)
        self.text = 'H'


class XGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super().__init__(x, y)
        self.text = 'X'


class YGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super().__init__(x, y)
        self.text = 'Y'


class ZGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super().__init__(x, y)
        self.text = 'Z'


class SGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super().__init__(x, y)
        self.text = 'S'


class RxGate(Gate):

    def __init__(self, x, y, angle):
        # type: (int, int, float) -> None
        super().__init__(x, y)
        if angle not in range(0, 361):
            raise ValueError('Angle is not between 0 - 360')
        self.text = 'RX_{}'.format(angle)


class RyGate(Gate):

    def __init__(self, x, y, angle):
        # type: (int, int, float) -> None
        super().__init__(x, y)
        if angle not in range(0, 361):
            raise ValueError('Angle is not between 0 - 360')
        self.text = 'RY_{}'.format(angle)


class RzGate(Gate):

    def __init__(self, x, y, angle):
        # type: (int, int, float) -> None
        super().__init__(x, y)
        if angle not in range(0, 361):
            raise ValueError('Angle is not between 0 - 360')
        self.text = 'RZ_{}'.format(angle)


# PHASE
class CPhase(Gate):
    text = 'CP'

    def __init__(self, x, y):
        # type: (Union[List[int], int, (int, int)], Union[List[int], (int,int)]) -> None
        if isinstance(x, int):
            x_gate = self.x1 = x
        else:
            if len(set(x)) != 1:
                raise ValueError('X - coordinates not equal or empty')
            if len(x) == 1:
                x_gate = self.x1 = x[0]
            else:
                if len(x) is not 2:
                    raise ValueError('X - coordinates greater 2')
                x_gate, self.x1 = x

        if len(y) is not 2:
            raise ValueError('number of Y - coordinates unequal 2')
        if len(set(y)) is not 2:
            raise ValueError('Y - coordinates can not be equal')

        y_gate, self.y1 = y
        super().__init__(x_gate, y_gate)
        self.text = 'CP'


class CCPhase(Gate):
    text = 'CCP'

    def __init__(self, x, y):
        # type: (Union[List[int], int, (int, int)], Union[List[int], (int,int)]) -> None
        if isinstance(x, int):
            x_gate = self.x1 = self.x2 = x
        else:
            if len(set(x)) is not 1:
                raise ValueError('X - coordinates not equal or empty')
            if not all(value > 0 for value in x):
                raise ValueError('X - coordinate must be greater 0')
            if len(x) == 1:
                x_gate = x[0]
                self.x1 = x[0]
            else:
                if len(x) is not 3:
                    raise ValueError('X - coordinates greater 3')
                x_gate, self.x1, self.x2 = x
        if len(y) is not 3:
            raise ValueError('number of Y - coordinates unequal 2')
        if len(set(y)) is not 3:
            raise ValueError('Y - coordinates can not be equal')
        if not all(value > 0 for value in y):
            raise ValueError('Y - coordinate must be greater 0')
        y_gate, self.y1, self.y2 = y
        super().__init__(x_gate, y_gate)
        self.text = 'CCP'


class Measure(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super().__init__(x, y)
        self.text = 'M'


class SDag(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super().__init__(x, y)
        self.text = 'S†'


class TGate(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super().__init__(x, y)
        self.text = 'T'


class TDag(Gate):

    def __init__(self, x, y):
        # type: (int, int) -> None
        super().__init__(x, y)
        self.text = 'T†'
