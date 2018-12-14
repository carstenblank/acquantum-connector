from Gates import XGate, Measure
from alibabaQuantum import AlibabaQuantum, AcCredentials, AcExperimentType

api = AlibabaQuantum()

api.create_session(AcCredentials('sebboer', 'qnpwzHyIIFw33Nw2PBx'))

# Create Experiment
experiment_id = api.create_experiment(bit_width=4, experiment_type=AcExperimentType.SIMULATE, experiment_name='Demo')
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
api.run_experiment(experiment_id, AcExperimentType.SIMULATE, 2, 100)

# Get Result
api.get_result(experiment_id)

# Download Result
api.download_result(experiment_id)

api.save_session()
