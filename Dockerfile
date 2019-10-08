FROM python:3.7
COPY kube_service_dns_exporter.py /kube_service_dns_exporter.py
COPY requirements.txt  /tmp
# install extra dependencies specified by developers
RUN pip install -r /tmp/requirements.txt
CMD kopf run /kube_service_dns_exporter.py --verbose