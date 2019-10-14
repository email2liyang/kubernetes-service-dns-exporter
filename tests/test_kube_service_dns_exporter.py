import os

import boto3
from moto import mock_route53
import pytest
from kube_service_dns_exporter import route53_dns


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['domain_name'] = 'test.com'
    os.environ['aws_access_key_id'] = 'testing'
    os.environ['aws_secret_access_key'] = 'testing'


@pytest.fixture(scope='function')
def route53(aws_credentials):
    with mock_route53():
        yield boto3.client('route53')


def test_route53(route53):
    assert os.getenv('domain_name') == 'test.com'
    resp = route53.create_hosted_zone(Name=os.getenv('domain_name'), CallerReference='xxx')
    zone_id = resp['HostedZone']['Id']
    os.environ['hosted_zone_id'] = zone_id
    dns_name, record = route53_dns('CREATE', 'test_service', '127.0.0.2')
    assert dns_name == 'kube-test_service.test.com'
    assert record['ResponseMetadata']['HTTPStatusCode'] == 200
