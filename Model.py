from typing import Any


class AcRequestError(Exception):
    def __init__(self, message, status_code=None):
        # type: (str, int) -> None
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return 'AcRequestError: \'{}\''.format(self.message)

    def __repr__(self):
        return 'AcRequestError: \'{}\''.format(self.message)


class AcRequestForbiddenError(AcRequestError):
    def __init__(self, message='403 Forbidden'):
        # type: (str) -> None
        self.message = message

    def __str__(self):
        return '403 - AcRequestForbiddenError: \'{}\''.format(self.message)

    def __repr__(self):
        return '403 - AcRequestForbiddenError: \'{}\''.format(self.message)


class AcResponse:
    def __init__(self, success=True, data=None, exception=None):
        # type: (bool,Any, Any) -> None
        self.success = success
        self.data = data
        self.exception = exception

    def __str__(self):
        return 'AcResponse: {{ success: {}, exception: {} }}'.format(self.success, self.exception)

    def __repr__(self):
        return 'AcResponse: {{ success: {}, exception: {} }}'.format(self.success, self.exception)


class AcExperimentDetail:

    def __init__(self, name, version, experiment_id, experiment_type, execution, bit_width=None):
        # type: (str, int, int, str, int, int) -> None
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


class AcExperiment:

    def __init__(self, detail, data, code=''):
        # type: (AcExperimentDetail, Any, str) -> None
        self.detail = detail
        self.data = data
        self.code = code

    def __str__(self):
        return 'AcExperiment: {{ data: {}, code: {}, detail: {} }}'.format(self.data, self.code, self.detail)

    def __repr__(self):
        return 'AcExperiment: {{ data: {}, code: {}, detail: {} }}'.format(self.data, self.code, self.detail)


class AcResultResponse:

    def __init__(self, simulated_result=None, real_result=None):
        # type: ([AcResult], [AcResult]) -> None
        self.simulated_result = simulated_result
        self.real_result = real_result

    def get_result(self):
        # type: () -> [AcResult] or ([AcResult], [AcResult])
        if self.simulated_result:
            if self.real_result:
                return self.real_result, self.simulated_result
            return self.simulated_result
        else:
            return self.real_result

    def __str__(self):
        return 'AcResultResponse {{ simulated_result: {}, real_result: {} }}'.format(self.simulated_result,
                                                                                     self.real_result)

    def __repr__(self):
        return 'AcResultResponse {{ simulated_result: {}, real_result: {} }}'.format(self.simulated_result,
                                                                                     self.real_result)


class AcResult:

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
        self.data = data
        self.exception = exception

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
