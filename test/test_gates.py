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

from unittest import TestCase

from acquantumconnector.model.gates import RzGate, RxGate, RyGate, CPhase, CCPhase, XGate, YGate, ZGate, HGate, SGate, \
    TGate, SDag, TDag, Measure, Gate


class TestGates(TestCase):

    def setUp(self):
        pass

    def test_gates(self):
        gates = [XGate(1, 1), CCPhase(1, [1, 2, 3])]  # type: [Gate]
        for gate in gates:
            self.assertNotEqual(gate.x, None)
            self.assertNotEqual(gate.y, None)

    def test_Rz_Gate(self):
        gate = RzGate(1, 1, 360)
        self.assertEqual(gate.text, 'RZ_360')
        self.assertEqual(gate.gateDetail, dict())
        self.assertEqual(gate.x, 1)
        self.assertEqual(gate.y, 1)
        g_dict = gate.__dict__
        self.assertTrue('x' in g_dict)
        self.assertTrue('y' in g_dict)
        self.assertTrue('gateDetail' in g_dict)
        self.assertTrue('text' in g_dict)

        with self.assertRaises(ValueError):
            RzGate(1, 1, 361)

        with self.assertRaises(ValueError):
            RzGate(1, 1, -1)

        with self.assertRaises(ValueError):
            RzGate(0, 1, 350)

        with self.assertRaises(ValueError):
            RzGate(1, 0, 234)

        test_dict = {'x': 1, 'y': 1, 'gateDetail': {}, 'text': 'RZ_234'}
        self.assertEqual(test_dict, RzGate(1, 1, 234).__dict__)

    def test_Rx_Gate(self):
        gate = RxGate(1, 1, 360)
        self.assertEqual(gate.text, 'RX_360')
        self.assertEqual(gate.gateDetail, dict())
        self.assertEqual(gate.x, 1)
        self.assertEqual(gate.y, 1)
        g_dict = gate.__dict__
        self.assertTrue('x' in g_dict)
        self.assertTrue('y' in g_dict)
        self.assertTrue('gateDetail' in g_dict)
        self.assertTrue('text' in g_dict)

        with self.assertRaises(ValueError):
            RxGate(1, 1, 361)

        with self.assertRaises(ValueError):
            RxGate(1, 1, -1)

        with self.assertRaises(ValueError):
            RxGate(0, 1, 350)

        with self.assertRaises(ValueError):
            RxGate(1, 0, 234)

        test_dict = {'x': 1, 'y': 1, 'gateDetail': {}, 'text': 'RX_234'}
        self.assertEqual(test_dict, RxGate(1, 1, 234).__dict__)

    def test_Ry_Gate(self):
        gate = RyGate(1, 1, 360)
        self.assertEqual(gate.text, 'RY_360')
        self.assertEqual(gate.gateDetail, dict())
        self.assertEqual(gate.x, 1)
        self.assertEqual(gate.y, 1)
        g_dict = gate.__dict__
        self.assertTrue('x' in g_dict)
        self.assertTrue('y' in g_dict)
        self.assertTrue('gateDetail' in g_dict)
        self.assertTrue('text' in g_dict)

        with self.assertRaises(ValueError):
            RyGate(1, 1, 361)

        with self.assertRaises(ValueError):
            RyGate(1, 1, -1)

        with self.assertRaises(ValueError):
            RyGate(0, 1, 350)

        with self.assertRaises(ValueError):
            RyGate(1, 0, 234)

        test_dict = {'x': 1, 'y': 1, 'gateDetail': {}, 'text': 'RY_234'}
        self.assertEqual(test_dict, RyGate(1, 1, 234).__dict__)

    def test_CPhase(self):
        phase = CPhase([1], [1, 2])
        self.assertEqual('CP', phase.text)
        self.assertEqual(dict(), phase.gateDetail)
        self.assertEqual(1, phase.x)
        self.assertEqual(1, phase.x1)
        self.assertEqual(1, phase.y)
        self.assertEqual(2, phase.y1)

        phase = CPhase(1, (1, 2))
        self.assertEqual(1, phase.x)
        self.assertEqual(1, phase.x1)
        self.assertEqual(1, phase.y)
        self.assertEqual(2, phase.y1)

        phase = CPhase((1, 1), (1, 2))
        self.assertEqual(1, phase.x)
        self.assertEqual(1, phase.x1)
        self.assertEqual(1, phase.y)
        self.assertEqual(2, phase.y1)

        with self.assertRaises(ValueError):
            CPhase([1, 2], [1, 2])

        with self.assertRaises(ValueError):
            CPhase([1, 1], [1, 2, 3])

        with self.assertRaises(ValueError):
            CPhase(1, (1, 2, 3))

        with self.assertRaises(ValueError):
            CPhase((1, 2), (1, 3))

        with self.assertRaises(ValueError):
            CPhase((1, 2), 1)

        with self.assertRaises(ValueError):
            CPhase(1, (3, 3))

        with self.assertRaises(ValueError):
            CPhase(1, [3, 3])

        test_dict = {'x': 1, 'y': 1, 'x1': 1, 'y1': 2, 'gateDetail': {}, 'text': 'CP'}
        self.assertEqual(test_dict, CPhase(1, (1, 2)).__dict__)

    def test_CCPhase(self):
        phase = CCPhase([1, 1, 1], [1, 2, 3])
        self.assertEqual('CCP', phase.text)
        self.assertEqual(dict(), phase.gateDetail)
        self.assertEqual(1, phase.x)
        self.assertEqual(1, phase.x1)
        self.assertEqual(1, phase.x2)
        self.assertEqual(1, phase.y)
        self.assertEqual(2, phase.y1)
        self.assertEqual(3, phase.y2)

        phase = CCPhase(1, (1, 2, 3))
        self.assertEqual(1, phase.x)
        self.assertEqual(1, phase.x1)
        self.assertEqual(1, phase.x2)
        self.assertEqual(1, phase.y)
        self.assertEqual(2, phase.y1)
        self.assertEqual(3, phase.y2)

        phase = CCPhase((1, 1, 1), (1, 2, 4))
        self.assertEqual(1, phase.x)
        self.assertEqual(1, phase.x1)
        self.assertEqual(1, phase.x2)
        self.assertEqual(1, phase.y)
        self.assertEqual(2, phase.y1)
        self.assertEqual(4, phase.y2)

        with self.assertRaises(ValueError):
            CCPhase([1, 2, 3], [1, 2, 3])

        with self.assertRaises(ValueError):
            CCPhase([1, 1, 1], [1, 2, 2])

        with self.assertRaises(ValueError):
            CCPhase(1, (1, 2, 2))

        with self.assertRaises(ValueError):
            CCPhase((1, 2), (1, 2, 3))

        with self.assertRaises(ValueError):
            CCPhase((1, 2), 1)

        with self.assertRaises(ValueError):
            CCPhase(1, (3, 3, 3))

        with self.assertRaises(ValueError):
            CCPhase(0, (1, 2, 4))

        test_dict = {'x': 1, 'y': 1, 'x1': 1, 'y1': 2, 'x2': 1, 'y2': 4, 'gateDetail': {}, 'text': 'CCP'}
        self.assertEqual(test_dict, CCPhase(1, (1, 2, 4)).__dict__)

    def test_XGate(self):
        gate = XGate(1, 1)
        self.assertEqual(1, gate.x)
        self.assertEqual(1, gate.y)
        self.assertEqual('X', gate.text)

        with self.assertRaises(ValueError):
            XGate(0, 1)

        with self.assertRaises(ValueError):
            XGate(1, 0)

        test_dict = {'x': 1, 'y': 1, 'gateDetail': {}, 'text': 'X'}
        self.assertEqual(test_dict, XGate(1, 1).__dict__)

    def test_YGate(self):
        gate = YGate(1, 1)
        self.assertEqual(1, gate.x)
        self.assertEqual(1, gate.y)
        self.assertEqual('Y', gate.text)

        with self.assertRaises(ValueError):
            YGate(0, 1)

        with self.assertRaises(ValueError):
            YGate(1, 0)

        test_dict = {'x': 1, 'y': 1, 'gateDetail': {}, 'text': 'Y'}
        self.assertEqual(test_dict, YGate(1, 1).__dict__)

    def test_ZGate(self):
        gate = ZGate(1, 1)
        self.assertEqual(1, gate.x)
        self.assertEqual(1, gate.y)
        self.assertEqual('Z', gate.text)

        with self.assertRaises(ValueError):
            ZGate(0, 1)

        with self.assertRaises(ValueError):
            ZGate(1, 0)

        test_dict = {'x': 1, 'y': 1, 'gateDetail': {}, 'text': 'Z'}
        self.assertEqual(test_dict, ZGate(1, 1).__dict__)

    def test_HGate(self):
        gate = HGate(1, 1)
        self.assertEqual(1, gate.x)
        self.assertEqual(1, gate.y)
        self.assertEqual('H', gate.text)

        with self.assertRaises(ValueError):
            HGate(0, 1)

        with self.assertRaises(ValueError):
            HGate(1, 0)

        test_dict = {'x': 1, 'y': 1, 'gateDetail': {}, 'text': 'H'}
        self.assertEqual(test_dict, HGate(1, 1).__dict__)

    def test_SGate(self):
        gate = SGate(1, 1)
        self.assertEqual(1, gate.x)
        self.assertEqual(1, gate.y)
        self.assertEqual('S', gate.text)

        with self.assertRaises(ValueError):
            SGate(0, 1)

        with self.assertRaises(ValueError):
            SGate(1, 0)

        test_dict = {'x': 1, 'y': 1, 'gateDetail': {}, 'text': 'S'}
        self.assertEqual(test_dict, SGate(1, 1).__dict__)

    def test_TGate(self):
        gate = TGate(1, 1)
        self.assertEqual(1, gate.x)
        self.assertEqual(1, gate.y)
        self.assertEqual('T', gate.text)

        with self.assertRaises(ValueError):
            TGate(0, 1)

        with self.assertRaises(ValueError):
            TGate(1, 0)

        test_dict = {'x': 1, 'y': 1, 'gateDetail': {}, 'text': 'H'}
        self.assertEqual(test_dict, HGate(1, 1).__dict__)

    def test_SDag(self):
        gate = SDag(1, 1)
        self.assertEqual(1, gate.x)
        self.assertEqual(1, gate.y)
        self.assertEqual('S†', gate.text)

        with self.assertRaises(ValueError):
            SDag(0, 1)

        with self.assertRaises(ValueError):
            SDag(1, 0)

        test_dict = {'x': 1, 'y': 1, 'gateDetail': {}, 'text': 'S†'}
        self.assertEqual(test_dict, SDag(1, 1).__dict__)

    def test_TDag(self):
        gate = TDag(1, 1)
        self.assertEqual(1, gate.x)
        self.assertEqual(1, gate.y)
        self.assertEqual('T†', gate.text)

        with self.assertRaises(ValueError):
            TDag(0, 1)

        with self.assertRaises(ValueError):
            TDag(1, 0)

        test_dict = {'x': 1, 'y': 1, 'gateDetail': {}, 'text': 'T†'}
        self.assertEqual(test_dict, TDag(1, 1).__dict__)

    def test_Measure(self):
        measure = Measure(1, 1)
        self.assertEqual(1, measure.x)
        self.assertEqual(1, measure.y)
        self.assertEqual(1, measure.y)
        self.assertEqual('M', measure.text)

        with self.assertRaises(ValueError):
            Measure(0, 1)

        with self.assertRaises(ValueError):
            Measure(1, 0)

        test_dict = {'x': 1, 'y': 1, 'gateDetail': {}, 'text': 'M'}
        self.assertEqual(test_dict, Measure(1, 1).__dict__)
