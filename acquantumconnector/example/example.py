from acquantumconnector.connector.acquantumconnector import AcQuantumConnector
from acquantumconnector.credentials.credentials import AcQuantumCredentials
from acquantumconnector.model.backendtype import AcQuantumBackendType
from acquantumconnector.model.gates import XGate, Measure

api = AcQuantumConnector()

api.create_session(AcQuantumCredentials('username', 'password'))

# Create Experiment
experiment_id = api.create_experiment(bit_width=4, experiment_type=AcQuantumBackendType.SIMULATE,
                                      experiment_name='Demo')
print(experiment_id)

# Update Experiment
gates = [XGate(1, 1), Measure(2, 1)]
api.update_experiment(experiment_id, gates)

# Get Experiment
exp_res = api.get_experiment(experiment_id)
print(exp_res)

# List Experiments
exp_list = api.get_experiments()
print(exp_list)

# Run Experiment
api.run_experiment(experiment_id, AcQuantumBackendType.SIMULATE, 2, 100)

# Get Result
api.get_result(experiment_id)

# Download Result
api.download_result(experiment_id)

api.save_session()
