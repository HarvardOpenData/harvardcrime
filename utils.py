import csv
import json
from importlib import reload

import incident
reload(incident)
from incident import Incident

def dump_csv(incidents):
    """
    Dumps a list of Incident objects to CSV.
    """
    with open('harvard_crime_incidents.csv', 'w') as csvfile:
        fieldnames = Incident.CSV_FIELDS
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for inc in incidents:
            writer.writerow(inc.to_dict_for_csv())
