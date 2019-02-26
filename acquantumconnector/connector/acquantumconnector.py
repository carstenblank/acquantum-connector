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

import pickle
import re
from typing import Any

import requests

from acquantumconnector.credentials.credentials import AcQuantumCredentials
from acquantumconnector.model.backendtype import AcQuantumBackendType
from acquantumconnector.model.config import AcQuantumRawConfig
from acquantumconnector.model.errors import AcQuantumRequestError, AcQuantumRequestForbiddenError
from acquantumconnector.model.gates import Gate
from acquantumconnector.model.response import AcQuantumExperimentDetail, AcQuantumExperiment, AcQuantumResult, \
    AcQuantumResultResponse, AcQuantumResponse


class AcQuantumSession(object):

    def __init__(self, csrf, cookies, credentials):
        # type: (str, Any, AcQuantumCredentials) -> None

        self.csrf = csrf
        self.cookies = cookies
        self.credentials = credentials

    def __str__(self):
        # type: () -> str
        return 'AcSession: [cookies: {}, csrf: {}]'.format(self.cookies, self.csrf)


class AcQuantumConnector(object):
    _schema = 'http'
    _base_uri = '{}://quantumcomputer.ac.cn'.format(_schema)
    _CHARSET_PARAM = ('_input_charset', 'utf-8')
    _TOKEN_HEADER_KEY = 'X-CSRF-TOKEN'

    def __init__(self):
        self._req = requests.session()
        self._credentials = None
        self._session = None

    def create_session(self, credentials):
        # type: (AcQuantumCredentials) -> None

        self._credentials = credentials
        csrf = self._request_csrf_token()
        cookies = self._req.cookies
        self._session = AcQuantumSession(csrf, cookies, credentials)
        response = self._login().json()
        if not response['success']:
            raise Exception('Connection refused: {}'.format(response['message']))

    def reconnect_session(self):
        print('... reconnecting session')
        self.create_session(self._credentials)

    def save_session(self):
        with open('session', 'wb') as f:
            self._session.cookies = self._req.cookies
            pickle.dump(self._session, f)

    def load_session(self):
        with open('session', 'rb') as f:
            self._session = pickle.load(f)
            self._req.cookies.update(self._session.cookies)

    def _login(self):
        # type: () -> requests.Response

        uri = '{}/login'.format(self._base_uri)
        params = {'_input_charset': 'utf-8'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            '_csrf': self._session.csrf,
            'username': self._credentials.user_name,
            'password': self._credentials.password,
        }

        return self._req.post(uri, data=payload, params=params, headers=headers)

    def create_experiment(self, bit_width, experiment_type, experiment_name):
        # type: (int, AcQuantumBackendType, str) -> int

        """
        :param bit_width:  bit width of the experiment
        :param experiment_type: Type of the backend the experiment should run
        :param experiment_name: Name of the experiment
        :return:
        """

        uri = '{}/experiment/infosave'.format(self._base_uri)
        params = {self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1]}
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf, 'Content-Type': 'application/json'}
        payload = {
            'bitWidth': bit_width,
            'type': experiment_type.name,
            'name': experiment_name
        }
        response = self.handle_ac_response(self._req.post(uri, params=params, headers=headers, json=payload))
        return response.data

    def update_experiment(self, experiment_id, gates, code=None, override=True):
        # type: (int, [Gate], str, bool) -> None

        """
        :param experiment_id: ID of created Experiment
        :param gates: Gates object definition that should be submitted
        :param code:
        :param override: Default = True. If False the last project State gets fetched from the Backend and Merged with
                the new Gates Definition
        :return: None
        :raises AcQuantumRequestError
        """

        uri = '{}/experiment/codesave'.format(self._base_uri)
        params = {
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1]
        }
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf, 'Content-Type': 'application/json'}
        payload = {
            'experimentId': str(experiment_id),
            'data': [gate.__dict__ for gate in gates],
            'code': code if code else ''
        }
        if not override:
            exp = self.get_experiment(experiment_id)
            existing_gates = exp.data
            payload['data'] = payload['data'] + existing_gates

        self.handle_ac_response(self._req.post(uri, json=payload, params=params, headers=headers))

    def get_experiment(self, experiment_id):
        # type: (int) -> AcQuantumExperiment
        """
        :param experiment_id: ID of experiment
        :return: AcQuantumExperiment
        """

        uri = '{}/experiment/detail'.format(self._base_uri)
        params = {
            'experimentId': experiment_id,
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[0]
        }
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf}

        response = self.handle_ac_response(self._req.get(uri, params=params, headers=headers))
        body = response.data
        exp_detail = AcQuantumExperimentDetail(body['experimentName'], body['version'], int(experiment_id),
                                               body['experimentType'], body['execution'], bit_width=body['bitWidth'])
        experiment = AcQuantumExperiment(detail=exp_detail, data=body['data'], code=body['code'])
        return experiment

    def get_experiments(self):
        # type: () -> [AcQuantumExperimentDetail]

        uri = '{}/experiment/list'.format(self._base_uri)
        params = {
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1]
        }
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf, 'Content-Type': 'application/json'}

        response = self.handle_ac_response(self._req.get(uri, params=params, headers=headers))
        body = response.data
        experiment_list = [
            AcQuantumExperimentDetail(exp['name'], exp['version'], exp['experimentId'], exp['type'],
                                      exp['execution']) for exp in body]
        return experiment_list

    def run_experiment(self, experiment_id, experiment_type, bit_width, shots, seed=None):
        # type: (int, AcQuantumBackendType, int, int, str) -> None

        uri = '{}/experiment/submit'.format(self._base_uri)
        headers = {'Content-Type': 'application/json', self._TOKEN_HEADER_KEY: self._session.csrf}
        params = {
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1],
            'experimentId': experiment_id,
            'bitWidth': bit_width,
            'type': experiment_type.name,
            'shots': shots,
            'seed': seed if seed else ''
        }
        self.handle_ac_response(self._req.post(uri, headers=headers, params=params))

    def get_result(self, experiment_id):
        # type: (int) -> AcQuantumResultResponse

        uri = '{}/experiment/resultlist'.format(self._base_uri)
        params = {
            'experimentId': experiment_id,
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1]
        }
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf}

        response = self.handle_ac_response(self._req.get(uri, params=params, headers=headers))
        body = response.data
        simulated_result = [
            AcQuantumResult(res['id'], res['seed'], res['shots'], res['startTime'], res['measureQubits'],
                            res['finishTime'],
                            res['process'], res['data']) for res in body['simulateResult']]
        real_result = [
            AcQuantumResult(res['id'], res['seed'], res['shots'], res['startTime'], res['measureQubits'],
                            res['finishTime'],
                            res['process'], res['data']) for res in body['realResult']]
        return AcQuantumResultResponse(simulated_result, real_result)

    def download_result(self, experiment_id, file_name=None):
        # type: (int, str) -> None

        uri = '{}/experiment/resultDownload'.format(self._base_uri)
        params = {'id': experiment_id}
        headers = {
            self._TOKEN_HEADER_KEY: self._session.csrf,
            'Accept-Encoding': 'gzip, deflate'
        }
        response = self._req.get(uri, params=params, headers=headers)
        if not file_name:
            file_name = 'result_{}.xls'.format(experiment_id)

        with open(file_name, 'wb') as f:
            f.write(response.content)

    def _request_csrf_token(self):
        # type: () -> str

        uri = '{}/login'.format(self._base_uri)
        response = self._req.get(uri)
        return re.search('[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?', response.text).group()

    def delete_experiment(self, experiment_id):
        # type: (int) -> None

        uri = '{}/experiment/delete'.format(self._base_uri)
        headers = {'Content-Type': 'application/json', self._TOKEN_HEADER_KEY: self._session.csrf}
        params = {
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1],
            'experimentId': experiment_id,
        }

        self.handle_ac_response(self._req.post(uri, headers=headers, params=params))

    def delete_result(self, result_id):
        # type: (int) -> None
        uri = '{}/experiment/result/delete'.format(self._base_uri)
        headers = {'Content-Type': 'application/json', self._TOKEN_HEADER_KEY: self._session.csrf}
        params = {
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1],
            'id': result_id
        }

        self.handle_ac_response(self._req.post(uri, headers=headers, params=params))

    def get_backend_config(self):
        # type: () -> AcQuantumRawConfig

        """

        :return: Backend Configuration
        """

        uri = '{}/computerConfig/query'.format(self._base_uri)
        headers = {'Content-Type': 'application/json', self._TOKEN_HEADER_KEY: self._session.csrf}
        params = {
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1]
        }
        response = self.handle_ac_response(self._req.get(uri, headers=headers, params=params))
        return AcQuantumRawConfig.from_json(response.data)

    def available_backends(self):
        # TODO: implement
        # MOCKING
        return [
            {
                'backend_name': 'SIMULATE',
                'backend_version': '0.0.1',
                'n_qubits': 25,
                'basis_gates': ['x,y,z,h,s,sdg,t,tdg,rx,ry,rz,u1,u2,u3,cx,crz,ccx'],
                'gates': [],
                'local': False,
                'simulator': True,
                'conditional': False,
                'open_pulse': False,
                'memory': False,
                'max_shots': 8192,
                'url': 'http://quantumcomputer.ac.cn'
            },
            {
                'backend_name': 'REAL',
                'backend_version': '0.0.1',
                'n_qubits': 11,
                'basis_gates': ['x,y,z,h,s,sdg,t,tdg,rx,ry,rz,u1,u2,u3,cx,crz,ccx'],
                'gates': [],
                'local': False,
                'simulator': False,
                'conditional': False,
                'open_pulse': False,
                'memory': False,
                'max_shots': 20000,
                'url': 'http://quantumcomputer.ac.cn'
            }
        ]

    @classmethod
    def handle_ac_response(cls, response):
        # type: (requests.Response) -> AcQuantumResponse

        r"""
        :param response: requests.Response
        :return: AcQuantumResponse
        :raises: AcRequestError, AcRequestForbiddenError
        """
        try:
            if response.status_code == 200:
                json = response.json()
                if json['success']:
                    try:
                        data = json['data']
                        return AcQuantumResponse(success=json['success'], exception=json['exception'], data=data)
                    except KeyError:
                        return AcQuantumResponse(success=json['success'], exception=json['exception'])
                else:
                    raise AcQuantumRequestError(json['exception'])
            else:
                error = response.json()
                if response.status_code == 403:
                    raise AcQuantumRequestForbiddenError()
                raise AcQuantumRequestError(error['exception'], status_code=response.status_code)
        except ValueError as err:
            raise AcQuantumRequestError(err.__str__())
