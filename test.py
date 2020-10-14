import sys
import json
import ckantoolkit  # Actually the local version, ho ho ho!
from ckanext.dcat.processors import RDFParser, RDFSerializer

with ckantoolkit.config.parameterize({"ckanext.dcat.base_uri": "https://data.gov.uk"}):
    try:
        if sys.argv[1] == "serialize":
            with open(sys.argv[2], "r") as metadata:
                with open(sys.argv[3], "wb") as output:
                    serializer = RDFSerializer()
                    output.write(
                        serializer.serialize_dataset(
                            json.loads(metadata.read()), _format="xml"
                        )
                    )
        elif sys.argv[1] == "parse":
            with open(sys.argv[3], "w") as output:
                with open(sys.argv[2], "r") as metadata:
                    parser = RDFParser()
                    parser.parse(metadata.read(), _format="xml")
                    output.write(json.dumps([a for a in parser.datasets()], indent=4))
        else:
            raise Exception("No option specified")
    except Exception as e:
        print(f"Usage: {sys.argv[0]} (parse|serialize) <input> <output>", file=sys.stderr)
        raise e

