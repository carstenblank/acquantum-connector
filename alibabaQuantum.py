import pickle
import re
import requests
from typing import List, Any

from Gates import Gate
from Model import AcResponse, AcErrorResponse, AcExperiment, AcExperimentDetail, AcRequestError, \
    AcRequestForbiddenError, AcResult, AcResultResponse


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
        # type: (int, str, str) -> int
        uri = '{}/experiment/infosave'.format(self._base_uri)
        params = {self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1]}
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf, 'Content-Type': 'application/json'}
        payload = {
            'bitWidth': bit_width,
            'type': experiment_type,
            'name': experiment_name
        }
        response = self.handle_ac_response(self._req.post(uri, params=params, headers=headers, json=payload))
        return response.data

    def update_experiment(self, experiment_id, gates, code=None, override=True):
        # type: (int, List[Gate], str, bool) -> None
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
        # type: (int) -> AcExperiment or AcErrorResponse
        uri = '{}/experiment/detail'.format(self._base_uri)
        params = {
            'experimentId': experiment_id,
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[0]
        }
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf}

        response = self.handle_ac_response(self._req.get(uri, params=params, headers=headers))
        body = response.data
        exp_detail = AcExperimentDetail(body['experimentName'], body['version'], int(experiment_id),
                                        body['experimentType'], body['execution'], bit_width=body['bitWidth'])
        experiment = AcExperiment(detail=exp_detail, data=body['data'], code=body['code'])
        return experiment

    def get_experiments(self):
        # type: () -> [AcExperimentDetail] or AcErrorResponse
        uri = '{}/experiment/list'.format(self._base_uri)
        params = {
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1]
        }
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf, 'Content-Type': 'application/json'}

        response = self.handle_ac_response(self._req.get(uri, params=params, headers=headers))
        body = response.data
        experiment_list = [
            AcExperimentDetail(exp['name'], exp['version'], exp['experimentId'], exp['type'],
                               exp['execution']) for exp in body]
        return experiment_list

    def run_experiment(self, experiment_id, experiment_type, bit_width, shots, seed=None):
        # type: (int, str, int, int, str) -> None
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
        self.handle_ac_response(self._req.post(uri, headers=headers, params=params))

    def get_result(self, experiment_id):
        # type: (int) -> AcResultResponse
        uri = '{}/experiment/resultlist'.format(self._base_uri)
        params = {
            'experimentId': experiment_id,
            self._CHARSET_PARAM[0]: self._CHARSET_PARAM[1]
        }
        headers = {self._TOKEN_HEADER_KEY: self._session.csrf}

        response = self.handle_ac_response(self._req.get(uri, params=params, headers=headers))
        body = response.data
        simulated_result = [
            AcResult(res['id'], res['seed'], res['shots'], res['startTime'], res['measureQubits'], res['finishTime'],
                     res['process'], res['data']) for res in body['simulateResult']]
        real_result = [
            AcResult(res['id'], res['seed'], res['shots'], res['startTime'], res['measureQubits'], res['finishTime'],
                     res['process'], res['data']) for res in body['realResult']]
        return AcResultResponse(simulated_result, real_result)

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

    def handle_ac_response(self, response):
        # type: (requests.Response) -> AcResponse
        r"""
        :param response: requests.Response
        :return: AcResponse
        :raises: AcRequestError, AcRequestForbiddenError
        """
        try:
            if response.status_code == 200:
                json = response.json()
                if json['success']:
                    try:
                        data = json['data']
                        return AcResponse(success=json['success'], exception=json['exception'], data=data)
                    except KeyError:
                        return AcResponse(success=json['success'], exception=json['exception'])
                else:
                    raise AcRequestError(json['exception'])
            else:
                error = response.json()
                if response.status_code == 403:
                    raise AcRequestForbiddenError()
                raise AcRequestError(error['exception'], status_code=response.status_code)
        except ValueError as err:
            raise AcRequestError(err.__str__())
