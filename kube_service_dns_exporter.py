import os

import kopf
import pykube


@kopf.on.create('', 'v1', 'services')
def create_fn(meta, body, spec, namespace, logger, **kwargs):
    api = pykube.HTTPClient(pykube.KubeConfig.from_file())
    print(f"creating service with {spec}")
    print(f"cluster ip is {spec['clusterIP']}")
    return {'message': 'hello world'}


