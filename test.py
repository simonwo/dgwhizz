import json
import ckantoolkit # Actually the local version, ho ho ho!
from ckanext.dcat.processors import RDFParser, RDFSerializer

with ckantoolkit.config.parameterize({'ckanext.dcat.base_uri': 'https://data.gov.uk'}):
    with open('../package_show.json', 'r') as metadata:
        with open('../metadata.xml', 'wb') as output:
            serializer = RDFSerializer()
            output.write(serializer.serialize_dataset(json.loads(metadata.read()), _format='xml'))

