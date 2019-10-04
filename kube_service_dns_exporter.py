import kopf
import pykube


@kopf.on.create('', 'v1', 'services')
def create_fn(spec, logger, **kwargs):
    api = pykube.HTTPClient(pykube.KubeConfig.from_file())
    print(f"creating service with {spec}")
    print(f"cluster ip is {spec['clusterIP']}")


@kopf.on.delete('', 'v1', 'services')
def delete_fn(spec,logger, **kwargs):
    print(f"deleting service with {spec}")
    print(f"cluster ip is {spec['clusterIP']}")
