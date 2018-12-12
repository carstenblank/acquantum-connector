# from json import JSONDecodeError
import re
import sys
import time
from unittest import TestCase

from Gates import *
from alibabaQuantum import AlibabaQuantum, AcCredentials, AcExperimentType


class TestAlibabaQuantum(TestCase):
    api = None

    @classmethod
    def setUpClass(cls):
        cls.api = AlibabaQuantum()
        cls.api.create_session(AcCredentials('sebboer', 'qnpwzHyIIFw33Nw2PBx'))

    @classmethod
    def tearDownClass(cls):
        cls.api.save_session()

    def setUp(self):
        self._delete_all_experiments()

    def tearDown(self):
        self._delete_all_experiments()

    def _delete_all_experiments(self):
        res = self.api.get_experiments()
        self.assertEqual(res.status_code, 200)
        try:
            res = res.json()
        except Exception:
            self.api.reconnect_session()
            res = self.api.get_experiments()
            res = res.json()

        exp_ids = [exp['experimentId'] for exp in res['data']]
        for id in exp_ids:
            response = self.api.delete_experiment(id)
            self.assertEqual(response.status_code, 200)

    def test_create_session(self):
        self.api.create_session(AcCredentials('sebboer', 'qnpwzHyIIFw33Nw2PBx'))

    def test_save_session(self):
        self.api.save_session()

    def test_load_session(self):
        self.api.load_session()

    def test_create_experiment(self):
        response = self.api.create_experiment(11, AcExperimentType.SIMULATE, 'UnitTesting')
        self.assertEqual(response.status_code, 200)
        json = response.json()
        self.assertTrue(json['success'])
        self.assertTrue(type(json['data'] is int))

    def test_update_experiment(self):
        experiment_id = self._create_experiment()
        gates = [XGate(1, 2), YGate(2, 2), CCPhase([3, 3, 3], [1, 2, 3]), Measure(4, 4)]
        g_dict = {}
        for gate in gates:
            g_dict[gate.text] = gate
        response = self.api.update_experiment(experiment_id, gates)

        self.assertEqual(response.status_code, 200)

        response = self.api.get_experiment(experiment_id)
        response = response.json()
        res_gates = response['data']['data']
        for g in res_gates:
            self.assertEqual(g['text'], g_dict[g['text']].text)
            self.assertEqual(g['x'], g_dict[g['text']].x)
            self.assertEqual(g['y'], g_dict[g['text']].y)

    def _create_experiment(self, bit_width=11, exp_type=AcExperimentType.SIMULATE, name='UnitTesting'):
        # type: (int, str, str) -> str

        response = self.api.create_experiment(bit_width, exp_type, name)
        json = response.json()
        return str(json['data'])

    def _create_experiment_with_gates(self, gates, bit_width=11, exp_type=AcExperimentType.SIMULATE,
                                      name='UnitTesting'):
        # type: ([Gate], int, str, str) -> str

        experiment_id = self._create_experiment(bit_width, exp_type, name)
        self.api.update_experiment(experiment_id, gates)
        return str(experiment_id)

    def test_get_experiment(self):
        experiment_id = self._create_experiment()
        response = self.api.get_experiment(experiment_id)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        data = body['data']
        self.assertEqual(data['experimentName'], 'UnitTesting')
        self.assertEqual(data['experimentType'], 'SIMULATE')
        self.assertEqual(data['bitWidth'], 11)

    def test_get_experiment_with_gate(self):
        gates = [YGate(1, 1), XGate(2, 2)]
        experiment_id = self._create_experiment_with_gates(gates)

        response = self.api.get_experiment(experiment_id)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        data = body['data']
        self.assertEqual(data['experimentName'], 'UnitTesting')
        self.assertEqual(data['experimentType'], 'SIMULATE')
        self.assertEqual(data['bitWidth'], 11)
        body_gates = data['data']
        self.assertEqual(len(body_gates), 2)
        self.assertEqual(body_gates[0]['text'], 'Y')
        self.assertEqual(body_gates[0]['x'], 1)
        self.assertEqual(body_gates[0]['y'], 1)
        self.assertEqual(body_gates[1]['text'], 'X')
        self.assertEqual(body_gates[1]['x'], 2)
        self.assertEqual(body_gates[1]['y'], 2)

    def test_get_experiments(self):
        exp_id = []
        for i in range(3):
            name = 'UnitTesting{}'.format(i)
            bit_width = 11 + i
            exp_id.append(self._create_experiment(bit_width=bit_width, name=name))
        response = self.api.get_experiments()
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body['success'])
        data = body['data']
        self.assertEqual(data[0]['name'], 'UnitTesting2')
        self.assertEqual(data[1]['name'], 'UnitTesting1')
        self.assertEqual(data[2]['name'], 'UnitTesting0')

    def test_get_result_real(self):
        gates = [XGate(1, 1), YGate(2, 2), Measure(1, 2)]
        experiment_id = self._create_experiment_with_gates(gates)
        self.assertEqual(
            self.api.run_experiment(experiment_id, AcExperimentType.REAL, bit_width=4, shots=100).status_code, 200)

        time.sleep(1)
        response = self.api.get_result(experiment_id)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        real_result = body['data']['realResult'][0]
        self.assertIsNotNone(real_result['startTime'])
        if real_result['process']:
            self.assertIsNone(real_result['finishTime'])
        else:
            self.assertIsNotNone(real_result['finishTime'])
            self.assertIsNotNone(real_result['process'])

    def test_get_result_simulated(self):
        gates = [XGate(1, 1), YGate(2, 2), Measure(1, 2)]
        experiment_id = self._create_experiment_with_gates(gates)
        self.assertEqual(
            self.api.run_experiment(experiment_id, AcExperimentType.SIMULATE, bit_width=11, shots=100).status_code, 200)

        time.sleep(1)
        response = self.api.get_result(experiment_id)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        simulate_result = body['data']['simulateResult'][0]
        self.assertIsNotNone(simulate_result['startTime'])
        self.assertIsNotNone(simulate_result['finishTime'])
        self.assertIsNotNone(simulate_result['data'])

    def test_download_result(self):
        pass

    def test_run_experiment(self):
        gates = [XGate(1, 1), YGate(2, 2), Measure(1, 2)]
        experiment_id = self._create_experiment_with_gates(gates)
        response = self.api.run_experiment(experiment_id, AcExperimentType.SIMULATE, bit_width=11, shots=100)
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue(body['success'])
        self.assertEqual(body['data'], 'success')

    def test__request_csrf_token(self):
        token = self.api._request_csrf_token()
        if sys.version_info[0] == 3:
            self.assertRegex(token, re.compile('[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?'))
        else:
            self.assertRegexpMatches(token, re.compile('[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?'))

    def test_delete_experiment(self):
        created = self.api.create_experiment(11, AcExperimentType.SIMULATE, 'UniTestingDelete').json()
        experiment_id = created['data']
        response = self.api.delete_experiment(experiment_id)
        self.assertEqual(response.status_code, 200)

    def test_delete_all_experiments(self):
        res = self.api.get_experiments().json()
        exp_ids = [exp['experimentId'] for exp in res['data']]
        for id in exp_ids:
            response = self.api.delete_experiment(id)
            self.assertEqual(response.status_code, 200)
