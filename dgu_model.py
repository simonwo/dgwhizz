from typing import Tuple, Optional, List, Any
from datetime import date, datetime

class DataGovUkModel:
  """It is the unfortunate responsibility of this class to understand
  how Data.gov.uk translates CKAN data JSONs into actual display parameters."""

  """The topics list is set to these static values."""
  toipcs = [
    ("business-and-economy", "Business and economy"),
    ("environment", "Environment"),
    ("mapping", "Mapping"),
    ("crime-and-justice", "Crime and justice"),
    ("government", "Government"),
    ("society", "Society"),
    ("defence", "Defence"),
    ("government-spending", "Government spending"),
    ("towns-and-cities", "Towns and cities"),
    ("education", "Education"),
    ("health", "Health"),
    ("transport", "Transport"),
  ]

  def __init__(self, ckan_json, owner_org: str = None):
    self.data = ckan_json
    self.owner_org = owner_org

  @property
  def title(self):
    pass

  @property
  def released(self) -> bool:
    """If a dataset is not 'released', DGU will show a little box saying 'Not released'.
    This is controlled by if the dataset has any datafiles or 'docs'. The docs are a DGU-specific
    enterprise just for holding supporting documentation, so they can't be supplied by metadata."""
    return any(self.datafiles)

  @property
  def datafiles(self) -> List[Any]:
    return self.data['resources']

  @property
  def published_by(self) -> Optional[str]:
    """This is marked up as dc:creator, but it's really whoever owns the harvester.
    Comes from 'owner_org' in a CKAN package. There's no way to set this from a DCAT RDF or JSON,
    which is maybe fair enough as it certainly simplifies authorisation. But it also precludes
    departments providing a centralised data gateway for their ALBs that can publish under many names.
    It would be preferable to actually take the creator value from metadata before declaring it dc:creator.
    Note that this is passed through verbatim so depending on DGU config it might be possible to set it
    from a CKAN direct harvest."""
    return self.owner_org

  @property
  def last_updated(self) -> date:
    """The functionality of data.gov.uk is very broken here (probably because the logic is spread
    over about 4 million files). Here's a step-by-step of what actually happens:
    1. The dataset page shows the property `public_updated_at`. (datagovuk_find:/app/views/datasets/_meta_data.html.erb)
    2. This property is either the `inspire_dataset_reference_date` or the `most_recently_updated_datafile_timestamp`, or
       the `updated_at` date of the dataset if there none of these are present. (datagovuk_publish:/app/models/dataset.rb)
    3. But the datafiles always have `updated_at` timestamps, and these are set from the, er, `created` time of the datafile,
       or just the dataset's own `created_at` time. So there's never a case where the datafile ends up without an `updated_at`.
       (datagovuk_publish:/app/services/ckan/v26/link_mapper.rb)
    So the fundamental flaw is that updated dates in the metadata are literally never used."""
    datafile_timestamps = [datetime.fromisoformat(datafile['created']) for datafile in self.datafiles]
    dataset_timestamp = datetime.fromisoformat(self.data['metadata_created'])
    return max(datafile_timestamps) if datafile_timestamps else dataset_timestamp

  @property
  def topic(self) -> Optional[Tuple[str, str]]:
    """Wow, this is even more broken. Data.gov.uk introduced a `theme-primary` option for some reason
    which they use completely instead of `theme` as found in normal CKAN. But none of the metadata parsers
    understand this so basically it's impossible to output standard metadata that will have a theme picked up.
    Maybe CKAN JSON parser can pick it up if the metadata comes with the non-standard `theme-primary` field?"""
    matches = [(slug, name) for (slug, name) in DataGovUkModel.toipcs if slug == self.data['theme-primary']]
    return matches[0] or None

if __name__ == '__main__':
  import json
  with open('../package_show.json', 'r') as metadata:
    model = DataGovUkModel(json.loads(metadata.read()))
    print(model.last_updated)
    print(model.topic)
