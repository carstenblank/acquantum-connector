
help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "test			to run unit test"

test:
	@echo "Launching unittests with arguments python -m unittest discover -s /home/basti/PycharmProjects/qiskit-ali/test -t /home/basti/PycharmProjects/qiskit-ali"
	python -m unittest