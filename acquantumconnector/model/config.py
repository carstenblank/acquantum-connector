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


class AcQuantumRawConfig:

    def __init__(self, system_config, one_q_gate_fidelities, qubit_parameter, system_status, two_q_gate_fidelity):
        # type: (dict, dict, dict, dict, dict) -> None
        self.system_config = BackendSystemConfig.from_dict(system_config)
        self.one_q_gate_fidelities = OneQGateFidelities.from_dict(one_q_gate_fidelities)
        self.qubit_parameter = QubitParameter.from_dict(qubit_parameter)
        self.system_status = SystemStatus.from_dict(system_status)
        self.two_q_gate_fidelity = TwoQGateFidelity.from_dict(two_q_gate_fidelity)

    @classmethod
    def from_json(cls, values):
        # type: ([dict]) -> AcQuantumRawConfig
        return AcQuantumRawConfig(*values)


class BackendSystemConfig:

    def __init__(self, computer_id, config_key, config_value):
        # type: (str, str, SystemConfigValue) -> None
        self.config_value = config_value  # type: SystemConfigValue
        self.config_key = config_key
        self.computer_id = computer_id

    @classmethod
    def from_dict(cls, values):
        # type: (dict) -> BackendSystemConfig
        config_value = SystemConfigValue.from_dict(json.loads(values['configValue']))
        return BackendSystemConfig(values['computerId'], values['configKey'], config_value)


class SystemConfigValue:

    def __init__(self, one_q_gates, one_q_gates_label, two_q_gates, two_q_gates_label, measure_size_upper_limit):
        # type: ([str], [str], [str], [str], int) -> None
        self.one_q_gates = one_q_gates
        self.one_q_gates_label = one_q_gates_label
        self.two_q_gates = two_q_gates
        self.two_q_gates_label = two_q_gates_label
        self.measure_size_upper_limit = measure_size_upper_limit

    @classmethod
    def from_dict(cls, values):
        # type: (dict) -> SystemConfigValue
        return SystemConfigValue(values['oneQGates'], values['oneQGatesLabel'], values['twoQGates'],
                                 values['twoQGatesLabel'], values['measureSizeUpperLimit'])


class OneQGateFidelities:

    def __init__(self, computer_id, config_key, config_value):
        self.config_value = config_value  # [dict]
        self.config_key = config_key
        self.computer_id = computer_id

    @classmethod
    def from_dict(cls, values):
        # type: (dict) -> OneQGateFidelities
        config_value = json.loads(values['configValue'])
        return OneQGateFidelities(values['computerId'], values['configKey'], config_value)


class QubitParameter:

    def __init__(self, computer_id, config_key, config_value):
        self.config_value = config_value
        self.config_key = config_key
        self.computer_id = computer_id

    @classmethod
    def from_dict(cls, values):
        # type: (dict) -> QubitParameter
        return QubitParameter(values['computerId'], values['configKey'], values['configValue'])


class SystemStatus:

    def __init__(self, computer_id, config_key, config_value):
        # type: (str, str, SystemStatusConfigValue) -> None
        self.config_value = config_value  # type: SystemStatusConfigValue
        self.config_key = config_key
        self.computer_id = computer_id

    @classmethod
    def from_dict(cls, values):
        # type: (dict) -> SystemStatus
        config_value = SystemStatusConfigValue.from_dict(json.loads(values['configValue']))
        return SystemStatus(values['computerId'], values['configKey'], config_value)


class SystemStatusConfigValue:

    def __init__(self, status, fridge_temperature, last_calibration_time):
        # type: (str, str, str) -> None
        self.last_calibration_time = last_calibration_time
        self.fridge_temperature = fridge_temperature
        self.status = status

    @classmethod
    def from_dict(cls, values):
        # type: (dict) -> SystemStatusConfigValue
        return SystemStatusConfigValue(values['status'], values['fridgeTemperature'], values['lastCalibrationTime'])


class TwoQGateFidelity:

    def __init__(self, computer_id, config_key, config_value):
        self.config_value = config_value  # type: [dict]
        self.config_key = config_key
        self.computer_id = computer_id

    @classmethod
    def from_dict(cls, values):
        # type: (dict) -> TwoQGateFidelity
        config_value = json.loads(values['configValue'])
        return TwoQGateFidelity(values['computerId'], values['configKey'], config_value)
