import logging
import os
import time

import boto3
import kopf


@kopf.on.create('', 'v1', 'services')
def create_fn(meta, spec, logger, **kwargs):
    print(f"creating service with {meta}")
    print(f"cluster ip is {spec['clusterIP']}")
    logger.info(f"creating dns for service {meta['name']} which point to ip {spec['clusterIP']}")
    result = route53_dns('CREATE', meta['name'], spec['clusterIP'])
    logger.info(f"created dns {result[0]}  point to {spec['clusterIP']}")
    logger.info(f"route53 record {result[1]}")


@kopf.on.delete('', 'v1', 'services')
def delete_fn(meta, spec, logger, **kwargs):
    print(f"deleting service with {meta}")
    print(f"cluster ip is {spec['clusterIP']}")
    logger.info(f"deleting dns for service {meta['name']} which point to ip {spec['clusterIP']}")
    result = route53_dns('DELETE', meta['name'], spec['clusterIP'])
    logger.info(f"deleted dns {result[0]}  point to {spec['clusterIP']}")
    logger.info(f"route53 record {result[1]}")


def route53_dns(action, service_name, ip):
    dns_name = get_dns_name(service_name)
    client = get_route53_client()
    hosted_zone_id = os.getenv('hosted_zone_id')
    if hosted_zone_id is None:
        raise kopf.PermanentError(f"hosted_zone_id needed as System ENV.")

    record = client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            'Comment': f'{action} dns record for {dns_name} point to {ip}',
            'Changes': [
                {
                    'Action': f'{action}',
                    'ResourceRecordSet': {
                        'Name': f'{dns_name}',
                        'Type': 'A',
                        'TTL': 60,
                        'ResourceRecords': [
                            {
                                'Value': f'{ip}'
                            }
                        ]
                    }
                }
            ]
        }
    )
    change_id = record['ChangeInfo']['Id']
    change_status = record['ChangeInfo']['Status']
    while change_status == 'PENDING':
        time.sleep(10)
        record = client.get_change(Id=change_id)
        change_status = record['ChangeInfo']['Status']

    logging.info(f"{action} dns for service {service_name} which point to ip {ip} , result in {record}")
    return dns_name, record


def get_dns_name(service_name):
    domain_name = os.getenv('domain_name')
    if domain_name is None:
        raise kopf.PermanentError(f"domain_name needed as System ENV.")
    domain_prefix = os.getenv('domain_prefix', 'kube')
    # construct the dns_name
    dns_name = f'{domain_prefix}-{service_name}.{domain_name}'
    return dns_name


def get_route53_client():
    # get var from system env
    aws_access_key_id = os.getenv('aws_access_key_id')
    aws_secret_access_key = os.getenv('aws_secret_access_key')
    if aws_access_key_id is None or aws_secret_access_key is None:
        raise kopf.PermanentError(f"aws_access_key_id and aws_secret_access_key needed as System ENV.")
    # create the route53 reecord
    client = boto3.client('route53', aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)
    return client
