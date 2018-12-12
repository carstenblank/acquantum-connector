from Gates import XGate, Measure
from alibabaQuantum import AlibabaQuantum, AcCredentials, AcExperimentType

api = AlibabaQuantum()

api.create_session(AcCredentials('sebboer', 'qnpwzHyIIFw33Nw2PBx'))

# Create Experiment
response = api.create_experiment(bit_width=4, experiment_type=AcExperimentType.SIMULATE, experiment_name='Demo').json()
experiment_id = response['data']

# Update Experiment
gates = [XGate(1, 1), Measure(2, 1)]
response = api.update_experiment(experiment_id, gates).json()

# List Experiments
exp_list = api.get_experiments().json()
print(exp_list)

exp_res = api.get_result(experiment_id).json()
print(exp_res)

# api.delete_experiment(experiment_id)

api.save_session()
