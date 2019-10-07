# kubernetes-service-dns-exporter
export kubernetes service ip as a DNS record e.g in Route53

# design
see design doc from https://www.vipmind.me/infra/kube/writing-kubernetes-operator-in-python-with-kopf.html
# setup
* install python 3.7.4 `pyenv install 3.7.4`
* set local python `pyenv 3.7.4`
* upgrade pip `pip install --upgrade pip`
* install pipenv `pip install pipenv`
* install kopf `pipenv install kopf`

# test
* start minikube `minikube start`