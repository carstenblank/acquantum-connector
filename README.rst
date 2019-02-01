AcQuantum Connector
###################################

.. image:: https://img.shields.io/codacy/grade/707d09158742419a9379e9bce6c2510c.svg?style=for-the-badge
   :alt: Codacy Badge
   :target: https://app.codacy.com/app/sebboer/acquantum-connector?utm_source=github.com&utm_medium=referral&utm_content=sebboer/acquantum-connector&utm_campaign=Badge_Grade_Dashboard

.. image:: https://img.shields.io/readthedocs/acquantum-connector.svg?style=for-the-badge
    :target: https://acquantum-connector.readthedocs.io/en/latest/?badge=latest
    :alt: Read the Docs

.. image:: https://img.shields.io/travis/com/carstenblank/acquantum-connector.svg?style=for-the-badge
    :target: https://travis-ci.com/carstenblank/acquantum-connector
    :alt: Travis Build

.. image:: https://img.shields.io/pypi/v/acquantum-connector.svg?style=for-the-badge
    :alt: PyPI
    :target: https://pypi.org/project/acquantum-connector

.. image:: https://img.shields.io/pypi/pyversions/acquantum-connector.svg?style=for-the-badge
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/acquantum-connector

.. example-start-inclusion-marker-do-not-remove

Example
=======

.. code-block:: python

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

.. example-end-inclusion-marker-do-not-remove

.. license-start-inclusion-marker-do-not-remove

License
=======

The AcQuantumConnector is **free** and **open source**, released under
the `Apache License, Version 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_.

.. license-end-inclusion-marker-do-not-remove
