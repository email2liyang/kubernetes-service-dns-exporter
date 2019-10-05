from kube_service_dns_exporter import create_dns


def test_create_dns():
    create_dns("hello-world", "10.100.208.183")
