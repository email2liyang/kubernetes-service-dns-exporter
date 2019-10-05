import kopf
import pykube
import logging


@kopf.on.create('', 'v1', 'services')
def create_fn(meta, spec, logger, **kwargs):
    api = pykube.HTTPClient(pykube.KubeConfig.from_file())
    print(f"creating service with {meta}")
    print(f"cluster ip is {spec['clusterIP']}")
    logger.info(f"creating dns for service {meta['name']} which point to ip {spec['clusterIP']}")


@kopf.on.delete('', 'v1', 'services')
def delete_fn(meta, spec, logger, **kwargs):
    print(f"deleting service with {meta}")
    print(f"cluster ip is {spec['clusterIP']}")
    logger.info(f"deleting dns for service {meta['name']} which point to ip {spec['clusterIP']}")


def create_dns(service_name, ip):
    logging.debug(f"creating dns for service {service_name} which point to ip {ip}")

