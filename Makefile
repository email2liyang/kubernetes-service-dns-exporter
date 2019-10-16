freeze:
	pipenv lock -r > requirements.txt

init:
	kubectl apply -f tests/yaml/

add-svc:
	kubectl apply -f tests/yaml/service.yaml

rm-svc:
	kubectl delete -f tests/yaml/service.yaml

get-svc:
	kubectl get svc -n test

start:
	export hosted_zone_id=xxxxxxx && \
	export domain_name=vipmind.me && \
	export domain_prefix=kube && \
	export aws_access_key_id=xxxxx && \
	export aws_secret_access_key=xxxxxxxxxx && \
	kopf run kube_service_dns_exporter.py --verbose

kill:
	ps -ef | grep kube_service_dns_exporter.py | grep -v  grep | awk '{print $$2}' | xargs kill -9

version = latest
build:
	docker build -t email2liyang/kube_service_dns_exporter:$(version) .

run:
	docker run \
	-d email2liyang/kube_service_dns_exporter:$(version)

clean:
	docker ps -qa | xargs docker rm -f