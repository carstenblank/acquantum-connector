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

from typing import Any, List


class AcQuantumResponse(object):
    def __init__(self, success=True, data=None, exception=None):
        # type: (bool, Any, Any) -> None
        self.success = success
        self.data = data
        self.exception = exception

    def __str__(self):
        return 'AcResponse: {{ success: {}, exception: {} }}'.format(self.success, self.exception)

    def __repr__(self):
        return 'AcResponse: {{ success: {}, exception: {} }}'.format(self.success, self.exception)


class AcQuantumErrorResponse(AcQuantumResponse):

    def __init__(self, success=False, exception=None, status_code=None):
        # type: (bool, Any, int) -> None
        super(AcQuantumErrorResponse, self).__init__()
        self.status_code = status_code
        self.success = success
        self.exception = exception

    def __str__(self):
        return 'AcErrorResponse: {{ success: {}, exception: {}, status_code: {} }}'.format(self.success, self.exception,
                                                                                           self.status_code)

    def __repr__(self):
        return 'AcErrorResponse: {{ success: {}, exception: {}, status_code: {} }}'.format(self.success, self.exception,
                                                                                           self.status_code)


class AcQuantumExperimentDetail:

    def __init__(self, name, version, experiment_id, experiment_type, execution, bit_width=None):
        # type: (str, int, int, 'AcQuantumBackendType', int, int) -> None
        self.name = name
        self.version = version
        self.experiment_id = experiment_id
        self.experiment_type = experiment_type
        self.execution = execution
        self.bit_width = bit_width

    def __str__(self):
        return 'AcExperimentDetail: {{ name: {}, version: {}, experiment_id: {}, experiment_type: {}, execution: {}, ' \
               'bit_width {} }}' \
            .format(self.name, self.version, self.experiment_id, self.experiment_type, self.execution, self.bit_width)

    def __repr__(self):
        return 'AcExperimentDetail: {{ name: {}, version: {}, experiment_id: {}, experiment_type: {}, execution: {}, ' \
               'bit_width {} }}' \
            .format(self.name, self.version, self.experiment_id, self.experiment_type, self.execution, self.bit_width)


class AcQuantumExperiment:

    def __init__(self, detail, data, code=''):
        # type: (AcQuantumExperimentDetail, Any, str) -> None
        self.detail = detail
        self.data = data
        self.code = code

    def __str__(self):
        return 'AcExperiment: {{ data: {}, code: {}, detail: {} }}'.format(self.data, self.code, self.detail)

    def __repr__(self):
        return 'AcExperiment: {{ data: {}, code: {}, detail: {} }}'.format(self.data, self.code, self.detail)


class AcQuantumResultResponse:

    def __init__(self, simulated_result=None, real_result=None):
        # type: (List[AcQuantumResult], List[AcQuantumResult]) -> None
        self.simulated_result = simulated_result
        self.real_result = real_result

    def get_results(self):
        # type: () -> List[AcQuantumResult]
        if self.simulated_result:
            return self.simulated_result
        elif self.real_result:
            return self.real_result
        else:
            return None

    def __str__(self):
        return 'AcResultResponse {{ simulated_result: {}, real_result: {} }}'.format(self.simulated_result,
                                                                                     self.real_result)

    def __repr__(self):
        return 'AcResultResponse {{ simulated_result: {}, real_result: {} }}'.format(self.simulated_result,
                                                                                     self.real_result)


class AcQuantumResult:

    def __init__(self, result_id, seed, shots, start_time, measure_qubits, finish_time=None, process=None, data=None,
                 exception=None):
        # type: (int, int, int, str, [int], str, str, dict, Any) -> None
        self.result_id = result_id
        self.seed = seed
        self.shots = shots
        self.start_time = start_time
        self.measure_qubits = measure_qubits
        self.finish_time = finish_time
        self.process = process
        self.exception = exception
        if data:
            self.data = {k: float(v) for k, v in data.items()}

    def __str__(self):
        return 'AcResult: {{ result_id: {}, seed: {}, shots: {}, start_time: {}, measure_qubits: {},  ' \
               'finish_time: {}, process: {}, data: {} }} '.format(self.result_id, self.seed, self.shots,
                                                                   self.start_time, self.measure_qubits,
                                                                   self.finish_time, self.process, self.data)

    def __repr__(self):
        return 'AcResult: {{ result_id: {}, seed: {}, shots: {}, start_time: {}, measure_qubits: {}, ' \
               'finish_time: {}, process: {}, data: {} }} '.format(self.result_id, self.seed, self.shots,
                                                                   self.start_time, self.measure_qubits,
                                                                   self.finish_time, self.process, self.data)
