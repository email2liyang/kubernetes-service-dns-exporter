init:
	kubectl apply -f tests/yaml/

add-svc:
	kubectl apply -f tests/yaml/service.yaml

rm-svc:
	kubectl delete -f tests/yaml/service.yaml

get-svc:
	kubectl get svc -n test

curl:
	curl 192.168.99.100:30800

start:
	kopf run kube_service_dns_exporter.py --verbose

kill:
	ps -ef | grep kube_service_dns_exporter.py | grep -v  grep | awk '{print $2}' | xargs kill -9