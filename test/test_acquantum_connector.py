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

import json
import os
import re
from unittest import TestCase, mock

from acquantumconnector.connector.acquantumconnector import AcQuantumConnector
from acquantumconnector.credentials.credentials import AcQuantumCredentials
from acquantumconnector.model.backendtype import AcQuantumBackendType
from acquantumconnector.model.errors import AcQuantumRequestError
from acquantumconnector.model.gates import XGate


class MockApi:

    def __init__(self):
        self.cookies = None
        self.base_uri = 'http://quantumcomputer.ac.cn'
        self.failed_response = {
            'success': False,
            'exception': None,
            'message': 'error',
            'data': None
        }
        self.base_response = {
            'success': True,
            'exception': None,
            'message': None,
            'data': None
        }

    def get(self, *args, **kwargs):
        if args[0] == '{}/login'.format(self.base_uri):
            file_path = (os.path.dirname(__file__)) + '/resources/login.html'
            with open(file_path, 'r') as file:
                data = file.read().replace('\n', '')
            return MockedResponse({}, 200, data)
        elif args[0] == '{}/experiment/list'.format(self.base_uri):
            exp = [{
                'name': 'UnitTesting',
                'version': 1,
                'experimentId': 234,
                'type': 'SIMULATE',
                'execution': 0
            }, {
                'name': 'UnitTesting1',
                'version': 1,
                'experimentId': 235,
                'type': 'SIMULATE',
                'execution': 0
            }]
            body = self.base_response
            body['data'] = exp

            return MockedResponse(json_data=body)
        elif args[0] == '{}/experiment/detail'.format(self.base_uri):
            if 'params' in kwargs and kwargs['params']['experimentId'] == 123:
                body = self.base_response
                data = {
                    'code': '',
                    'version': 0,
                    'execution': 0,
                    'experimentName': 'UnitTesting',
                    'bitWidth': 10,
                    'experimentType': 'SIMULATE',
                    'data': [XGate(1, 1).__dict__]
                }
                body['data'] = data
                return MockedResponse(json_data=body)
            else:
                return MockedResponse(json_data=self.failed_response)
        elif args[0] == '{}/computerConfig/query'.format(self.base_uri):
            file_path = (os.path.dirname(__file__)) + '/resources/computer-config.json'
            with open(file_path) as f:
                data = json.load(f)
                return MockedResponse(json_data=data)
        elif args[0] == '{}/experiment/resultlist'.format(self.base_uri):
            result = [
                {'startTime': '2019-01-29 17:30:56',
                 'finishTime': '2019-01-29 17:30:57',
                 'process': None,
                 'data': {'1': '1.0'},
                 'id': 9868,
                 'seed': 0,
                 'shots': 100,
                 'measureQubits': [0]}]
            body = self.base_response
            if 'params' in kwargs and kwargs['params']['experimentId'] == 123:
                data = {
                    'realResult': [],
                    'simulateResult': result}
                body['data'] = data
                return MockedResponse(json_data=body)
            elif 'params' in kwargs and kwargs['params']['experimentId'] == 124:
                data = {
                    'realResult': result,
                    'simulateResult': []}
                body['data'] = data
                return MockedResponse(json_data=body)
            else:
                return MockedResponse(json_data=self.failed_response)
        else:
            return MockedResponse({'test': 'test'})

    def post(self, *args, **kwargs):
        if args[0] == '{}/login'.format(self.base_uri):
            if 'data' in kwargs and 'username' in kwargs['data']:
                return MockedResponse(json_data={'success': True})
            else:
                return MockedResponse({}, 403)
        elif args[0] == '{}/experiment/submit'.format(self.base_uri):
            if 'params' in kwargs and kwargs['params']['experimentId'] == 123:
                return MockedResponse(json_data=self.base_response)
        elif args[0] == '{}/experiment/delete'.format(self.base_uri):
            if 'params' in kwargs and kwargs['params']['experimentId'] == 123:
                return MockedResponse(json_data=self.base_response)
        elif args[0] == '{}/experiment/result/delete'.format(self.base_uri):
            if 'params' in kwargs and kwargs['params']['id'] == 123:
                return MockedResponse(json_data=self.base_response)

        return MockedResponse(json_data=self.failed_response)


class MockedResponse:

    def __init__(self, json_data=None, status_code=200, raw_response=None):
        self.json_data = json_data
        self.status_code = status_code
        self.raw_response = raw_response
        self.text = self.raw_response

    def json(self):
        return self.json_data


class AcQuantumConnectorUnitTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.init()

    @classmethod
    @mock.patch('acquantumconnector.connector.acquantumconnector.requests.session', side_effect=MockApi)
    def init(cls, mock_api=None):
        cls.mock_api = mock_api
        cls.api = AcQuantumConnector()

    def setUp(self):
        self.api.create_session(AcQuantumCredentials(os.environ['ACQ_USER'], os.environ['ACQ_PWD']))

    def test_create_session(self):
        self.api.create_session(AcQuantumCredentials(os.environ['ACQ_USER'], os.environ['ACQ_PWD']))
        self.assertRegex(self.api._session.csrf, re.compile('[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?'))

    def test__request_csrf_token(self):
        token = self.api._request_csrf_token()
        self.assertRegex(token, re.compile('[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?'))

    def test_get_experiments(self):
        experiments = self.api.get_experiments()
        self.assertEqual(experiments[0].name, 'UnitTesting')
        self.assertEqual(experiments[1].name, 'UnitTesting1')

    def test_get_experiment(self):
        experiment = self.api.get_experiment(123)
        self.assertEqual('UnitTesting', experiment.detail.name)
        self.assertEqual('SIMULATE', experiment.detail.experiment_type)
        self.assertEqual(10, experiment.detail.bit_width)
        self.assertEqual('X', experiment.data[0]['text'])
        self.assertEqual(1, experiment.data[0]['x'])
        self.assertEqual(1, experiment.data[0]['y'])

    def test_get_experiment_should_fail(self):
        with self.assertRaises(AcQuantumRequestError):
            self.api.get_experiment(124)

    def test_delete_experiment(self):
        try:
            self.api.delete_experiment(123)
        except AcQuantumRequestError as e:
            self.fail(e)

    def test_delete_experiment_should_fail(self):
        with self.assertRaises(AcQuantumRequestError):
            self.api.delete_experiment(124)

    def test_get_backend_config(self):
        config = self.api.get_backend_config()
        status = config.system_status.config_value.status
        self.assertTrue(status in ['ONLINE', 'OFFLINE'])

    def test_run_experiment(self):
        self.api.run_experiment(123, AcQuantumBackendType.SIMULATE, bit_width=11, shots=100)

    def test_run_experiment_should_fail(self):
        with self.assertRaises(AcQuantumRequestError):
            self.api.run_experiment(124, AcQuantumBackendType.SIMULATE, bit_width=11, shots=100)

    def test_get_simulated_result(self):
        results = self.api.get_result(123)
        simulate_result = results.simulated_result[0]
        self.assertIsNotNone(simulate_result.start_time)
        self.assertIsNotNone(simulate_result.finish_time)
        self.assertIsNotNone(simulate_result.data)

    def test_delete_result(self):
        self.api.delete_result(123)

    def test_delete_result_should_fail(self):
        with self.assertRaises(AcQuantumRequestError):
            self.api.delete_result(124)
