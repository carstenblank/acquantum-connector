import os
import re
import sys
import time
from os import listdir, remove
from unittest import TestCase

from acquantumconnector.connector.acquantumconnector import AcQuantumConnector
from acquantumconnector.credentials.credentials import AcQuantumCredentials
from acquantumconnector.model.backendtype import AcQuantumBackendType
from acquantumconnector.model.errors import AcQuantumRequestForbiddenError, AcQuantumRequestError
from acquantumconnector.model.gates import XGate, YGate, CCPhase, Measure, Gate


class TestAlibabaQuantum(TestCase):
    api = None

    @classmethod
    def setUpClass(cls):
        cls.api = AcQuantumConnector()
        cls.api.create_session(AcQuantumCredentials(os.environ['ACQ_USER'], os.environ['ACQ_PWD']))

    @classmethod
    def tearDownClass(cls):
        for filename in listdir('.'):
            if filename.endswith('.xls') or filename == 'session':
                remove(filename)

    def setUp(self):
        self._delete_all_experiments()

    def tearDown(self):
        self._delete_all_experiments()

    def _delete_all_experiments(self):
        try:
            res = self.api.get_experiments()
        except AcQuantumRequestForbiddenError:
            self.api.reconnect_session()
            res = self.api.get_experiments()

        exp_ids = [exp.experiment_id for exp in res]
        for exp_id in exp_ids:
            self.api.delete_experiment(exp_id)

    def test_create_session(self):
        self.api.create_session(AcQuantumCredentials(os.environ['ACQ_USER'], os.environ['ACQ_PWD']))

    def test_save_session(self):
        self.api.save_session()

    def test_load_session(self):
        self.api.save_session()
        csrf = self.api._session.csrf
        cookies = self.api._session.cookies
        self.api = AcQuantumConnector()
        self.api.load_session()
        self.assertEqual(self.api._session.csrf, csrf)
        self.assertEqual(self.api._session.cookies, cookies)

    def test_create_experiment(self):
        try:
            exp_id = self.api.create_experiment(11, AcQuantumBackendType.SIMULATE, 'UnitTesting')
            self.assertTrue(type(exp_id) is int)
        except AcQuantumRequestError as e:
            self.fail(e)

    def test_update_experiment(self):
        experiment_id = self._create_experiment()
        gates = [XGate(1, 2), YGate(2, 2), CCPhase([3, 3, 3], [1, 2, 3]), Measure(4, 4)]
        g_dict = {}
        for gate in gates:
            g_dict[gate.text] = gate
        try:
            self.api.update_experiment(experiment_id, gates)
        except AcQuantumRequestError as e:
            self.fail(e)

        response = self.api.get_experiment(experiment_id)
        res_gates = response.data
        for g in res_gates:
            self.assertEqual(g['text'], g_dict[g['text']].text)
            self.assertEqual(g['x'], g_dict[g['text']].x)
            self.assertEqual(g['y'], g_dict[g['text']].y)

    def _create_experiment(self, bit_width=11, exp_type=AcQuantumBackendType.SIMULATE, name='UnitTesting'):
        # type: (int, str, str) -> int

        response = self.api.create_experiment(bit_width, exp_type, name)
        return response

    def _create_experiment_with_gates(self, gates, bit_width=11, exp_type=AcQuantumBackendType.SIMULATE,
                                      name='UnitTesting'):
        # type: ([Gate], int, str, str) -> int

        experiment_id = self._create_experiment(bit_width, exp_type, name)
        self.api.update_experiment(experiment_id, gates)
        return experiment_id

    def test_get_experiment(self):
        experiment_id = self._create_experiment()
        try:
            experiment = self.api.get_experiment(experiment_id)
            self.assertEqual(experiment.detail.name, 'UnitTesting')
            self.assertEqual(experiment.detail.experiment_type, 'SIMULATE')
            self.assertEqual(experiment.detail.bit_width, 11)
        except AcQuantumRequestError as e:
            self.fail(e)

    def test_get_experiment_with_gate(self):
        gates = [YGate(1, 1), XGate(2, 2)]
        experiment_id = self._create_experiment_with_gates(gates)

        experiment = self.api.get_experiment(experiment_id)
        self.assertEqual(experiment.detail.name, 'UnitTesting')
        self.assertEqual(experiment.detail.experiment_type, 'SIMULATE')
        self.assertEqual(experiment.detail.bit_width, 11)
        body_gates = experiment.data
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
        experiments = self.api.get_experiments()
        self.assertEqual(experiments[0].name, 'UnitTesting2')
        self.assertEqual(experiments[1].name, 'UnitTesting1')
        self.assertEqual(experiments[2].name, 'UnitTesting0')

    def test_get_result_real(self):
        gates = [XGate(1, 1), YGate(2, 2), Measure(1, 2)]
        experiment_id = self._create_experiment_with_gates(gates)
        self.api.run_experiment(experiment_id, AcQuantumBackendType.REAL, bit_width=4, shots=100)

        time.sleep(1)
        results = self.api.get_result(experiment_id)
        self.assertIsNotNone(results.real_result[0])
        real_result = results.real_result[0]
        if real_result:
            self.assertIsNone(real_result.finish_time)
        else:
            self.assertIsNotNone(real_result.finish_time)
            self.assertIsNotNone(real_result.process)

    def test_get_result_simulated(self):
        gates = [XGate(1, 1), YGate(2, 2), Measure(1, 2)]
        experiment_id = self._create_experiment_with_gates(gates)
        self.api.run_experiment(experiment_id, AcQuantumBackendType.SIMULATE, bit_width=11, shots=100)

        time.sleep(1)
        results = self.api.get_result(experiment_id)
        simulate_result = results.simulated_result[0]
        self.assertIsNotNone(simulate_result.start_time)
        self.assertIsNotNone(simulate_result.finish_time)
        self.assertIsNotNone(simulate_result.data)

    def test_download_result(self):
        pass

    def test_run_experiment(self):
        gates = [XGate(1, 1), YGate(2, 2), Measure(1, 2)]
        experiment_id = self._create_experiment_with_gates(gates)
        try:
            self.api.run_experiment(experiment_id, AcQuantumBackendType.SIMULATE, bit_width=11, shots=100)
        except AcQuantumRequestError as e:
            self.fail(e)

    def test__request_csrf_token(self):
        token = self.api._request_csrf_token()
        if sys.version_info[0] == 3:
            self.assertRegex(token, re.compile('[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?'))
        else:
            self.assertRegexpMatches(token, re.compile('[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?'))

    def test_delete_experiment(self):
        experiment_id = self._create_experiment()
        try:
            self.api.delete_experiment(experiment_id)
        except AcQuantumRequestError as e:
            self.fail(e)

    def test_delete_all_experiments(self):
        exp_ids = []
        for i in range(3):
            name = 'UnitTesting{}'.format(i)
            bit_width = 11 + i
            exp_ids.append(self._create_experiment(bit_width=bit_width, name=name))
        for exp_id in exp_ids:
            try:
                self.api.delete_experiment(exp_id)
            except AcQuantumRequestError as e:
                self.fail(e)

    def test_get_backend_config(self):
        config = self.api.get_backend_config()
        status = config.system_status.config_value.status
        self.assertTrue(status in ['ONLINE', 'OFFLINE'])
