# kubernetes-service-dns-exporter
export kubernetes service ip as a DNS record e.g in Route53

# design
see design doc from 
* https://www.vipmind.me/infra/kube/writing-kubernetes-operator-in-python-with-kopf.html
* https://www.vipmind.me/infra/kube/deploy-kubernetes-operator-into-aws-eks-cluster.html
# setup
* install python 3.7.4 `pyenv install 3.7.4`
* set local python `pyenv 3.7.4`
* upgrade pip `pip install --upgrade pip`
* install pipenv `pip install pipenv`
* install kopf `pipenv install kopf`

# usage
* provide `hosted_zone_id`,`aws_access_key_id`,`aws_secret_access_key` in https://github.com/email2liyang/kubernetes-service-dns-exporter/blob/master/yaml/secrets.yaml.example
* rename `secrets.yaml.example` to `secrets.yaml`
* override `domain_name` in https://github.com/email2liyang/kubernetes-service-dns-exporter/blob/master/yaml/deployment.yaml
* apply it to kubernetes
```bash
kubectl apply -f yaml/rbac.yml
kubectl apply -f yaml/secrets.yaml
kubectl apply -f yaml/deployment.yaml
```