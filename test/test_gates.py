from unittest import TestCase

from acquantumconnector.model.gates import RzGate, RxGate, RyGate, CPhase, CCPhase


class TestGates(TestCase):

    def setUp(self):
        pass

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

        with self.assertRaises(AssertionError):
            RzGate(1, 1, 361)

        with self.assertRaises(AssertionError):
            RzGate(1, 1, -1)

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

        with self.assertRaises(AssertionError):
            RxGate(1, 1, 361)

        with self.assertRaises(AssertionError):
            RxGate(1, 1, -1)

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

        with self.assertRaises(AssertionError):
            RyGate(1, 1, 361)

        with self.assertRaises(AssertionError):
            RyGate(1, 1, -1)

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

        with self.assertRaises(AssertionError):
            CPhase([1, 2], [1, 2])

        with self.assertRaises(AssertionError):
            CPhase([1, 1], [1, 2, 3])

        with self.assertRaises(AssertionError):
            CPhase(1, (1, 2, 3))

        with self.assertRaises(AssertionError):
            CPhase((1, 2), (1, 3))

        with self.assertRaises(AssertionError):
            CPhase((1, 2), 1)

        with self.assertRaises(AssertionError):
            CPhase(1, (3, 3))

        with self.assertRaises(AssertionError):
            CPhase(1, [3, 3])

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

        with self.assertRaises(AssertionError):
            CCPhase([1, 2, 3], [1, 2, 3])

        with self.assertRaises(AssertionError):
            CCPhase([1, 1, 1], [1, 2, 2])

        with self.assertRaises(AssertionError):
            CCPhase(1, (1, 2, 2))

        with self.assertRaises(AssertionError):
            CCPhase((1, 2), (1, 2, 3))

        with self.assertRaises(AssertionError):
            CCPhase((1, 2), 1)

        with self.assertRaises(AssertionError):
            CCPhase(1, (3, 3, 3))
