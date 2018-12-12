import pickle
import re
from typing import List, Any

import requests

from Gates import Gate


class AcExperimentType(object):
    SIMULATE = 'SIMULATE'
    REAL = 'REAL'


class AcCredentials(object):

    def __init__(self, user_name, password):
        # type: (str, str) -> None

        self.user_name = user_name
        self.password = password


class AcSession(object):

    def __init__(self, csrf, cookies, credentials):
        # type: (str, Any, AcCredentials) -> None

        self.csrf = csrf
        self.cookies = cookies
        self.credentials = credentials

    def __str__(self):
        # type: () -> str

        return 'AcSession: [cookies: {}, csrf: {}]'.format(self.cookies, self.csrf)


class AlibabaQuantum(object):
    _schema = 'http'
    _base_uri = '{}://quantumcomputer.ac.cn'.format(_schema)
    _CHARSET_PARAM = ('_input_charset', 'utf-8')
    _TOKEN_HEADER_KEY = 'X-CSRF-TOKEN'

    def __init__(self):
        # type: () -> None
        self._req = requests.session()  # type: requests.Session
        self._credentials = None  # type: AcCredentials
        self._session = None  # type: AcSession

    def create_session(self, credentials):
        # type: (AcCredentials) -> None
        self._credentials = credentials
        csrf = self._request_csrf_token()
        cookies = self._req.cookies
        self._session = AcSession(csrf, cookies, credentials)
        response = self._login().json()
        if not response['success']:
            raise Exception('Connection refused: {}'.format(response['message']))

    def reconnect_session(self):
        # type: () -> None
        print('... reconnecting session')
        self.create_session(self._credentials)

    def save_session(self):
        # type: () -> None
        with open('session', 'wb') as f:
            self._session.cookies = self._req.cookies
            pickle.dump(self._session, f)

    def load_session(self):
        # type: () -> None
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
        # type: (int, str, str) -> requests.Response
        uri = '{}/experiment/infosave'.format(self._base_uri)
        params = {self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1]}
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf, 'Content-Type': 'application/json'}
        payload = {
            'bitWidth': bit_width,
            'type': experiment_type,
            'name': experiment_name
        }
        return self._req.post(uri, params=params, headers=headers, json=payload)

    def update_experiment(self, experiment_id, gates, code=None, override=True):
        # type: (str, List[Gate], str, bool) -> requests.Response
        uri = '{}/experiment/codesave'.format(self._base_uri)
        params = {
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1]
        }
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf, 'Content-Type': 'application/json'}
        payload = {
            'experimentId': experiment_id,
            'data': [gate.__dict__ for gate in gates],
            'code': code if code else ''
        }
        if not override:
            response = self.get_experiment(experiment_id)
            response = response.json()
            existing_gates = response['data']['data']
            payload['data'] = payload['data'] + existing_gates

        return self._req.post(uri, json=payload, params=params, headers=headers)

    def get_experiment(self, experiment_id):
        # type: (str) -> requests.Response
        uri = '{}/experiment/detail'.format(self._base_uri)
        params = {
            'experimentId': experiment_id,
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[0]
        }
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf}

        return self._req.get(uri, params=params, headers=headers)

    def get_experiments(self):
        # type: () -> requests.Response
        uri = '{}/experiment/list'.format(self._base_uri)
        params = {
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1]
        }
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf, 'Content-Type': 'application/json'}

        return self._req.get(uri, params=params, headers=headers)

    def get_result(self, experiment_id):
        # type: (str) -> requests.Response
        uri = '{}/experiment/resultlist'.format(self._base_uri)
        params = {
            'experimentId': experiment_id,
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1]
        }
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf}

        return self._req.get(uri, params=params, headers=headers)

    def download_result(self, experiment_id):
        # type: (str) -> None
        uri = '{}/experiment/resultDownload'.format(self._base_uri)
        params = {'id': experiment_id}
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf}
        request = self._req.get(uri, params=params, headers=headers)
        with open('result-{}'.format(experiment_id), 'wb') as f:
            f.write(request.content)

    def run_experiment(self, experiment_id, experiment_type, bit_width, shots, seed=None):
        # type: (str, str, int, int, str) -> requests.Response
        uri = '{}/experiment/submit'.format(self._base_uri)
        headers = {'Content-Type': 'application/json', self._TOKEN_HEADER_KEY: self._session.csrf}
        params = {
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1],
            'experimentId': experiment_id,
            'bitWidth': bit_width,
            'type': experiment_type,
            'shots': shots,
            'seed': seed if seed else ''
        }
        return self._req.post(uri, headers=headers, params=params)

    def _request_csrf_token(self):
        # type: () -> str
        uri = '{}/login'.format(self._base_uri)
        response = self._req.get(uri)
        return re.search('[a-f\d]{8}(-[a-f\d]{4}){3}-[a-f\d]{12}?', response.text).group()

    def delete_experiment(self, experiment_id):
        # type: (str) -> requests.Response
        uri = '{}/experiment/delete'.format(self._base_uri)
        headers = {'Content-Type': 'application/json', self._TOKEN_HEADER_KEY: self._session.csrf}
        params = {
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1],
            'experimentId': experiment_id,
        }

        return self._req.post(uri, headers=headers, params=params)
