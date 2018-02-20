import timing
from importlib import reload
reload(timing)

class Incident(object):

    def __init__(self, data_row):
        # `data_row` is something like:
        #
        #  ['11/28/17',
        #   '1:48 PM',
        #   'FIELD INTERVIEW',
        #   '11/28/17',
        #   '1:48 PM - 2:31 PM',
        #   'ALDRICH HALL',
        #   '35 HARVARD WAY',
        #   'ALLSTON',
        #   'CLOSED'],
        #
        # The rows correspond to:
        # 1. Date Reported
        # 2. Time Reported
        # 3. Incident Type
        # 4. Date Occurred
        # 5. Time Occurred
        # 6. Location
        # 7. Street Address
        # 8. City (in Massachusetts)
        # 9. "Disposition Type", per HUPD (whether the case is open or closed)
        self.incident_type = data_row[2]
        self.location = data_row[5]
        self.street_address = data_row[6]
        self.city = data_row[7]
        self.disposition = data_row[8]

        # convert date and time reported into a datetime
        # this returns a range of times (start, end), but these will be the
        # same because we're only passing a singular time. So just consider
        # the "start" time, which is the 0th element of the tuple.
        self.reported = timing.parse_raw_occurrence_data([data_row[0],data_row[1]])[0]

        # what about timing? well, there are 3 ways for date and time occurred to represented! (left of /// is data_row[3], right of /// is data_row[4])
        """
        11/28/17 /// 4:20 PM
        11/21/17 /// 2:00 PM - 6:00 PM
        11/27/17 - 5:45 PM /// 11/28/17 - 9:00 AM
        """
        # The first & second ways are used if the start and end of the incident
        # are on the same date. The third way is used if it spans multiple
        # dates.

        # now, parse data_row[3] and [4] into a start and end time.
        (self.occurred_start, self.occurred_end) = timing.parse_raw_occurrence_data(
            [data_row[3], data_row[4]])



    # static
    # this is the list of fields that are exported to CSV
    # see to_dict_for_csv()
    CSV_FIELDS = [
        'reported',
        'incident_type',
        'occurred_start',
        'occurred_end',
        'location',
        'street_address',
        'city',
        'disposition',
        'lat',
        'long'
    ]

    def to_dict_for_csv(self):
        # returns a nicer-formatted dict ready for insertion into a csv
        # so that means any arrays need to be flattened to scalars
        # also everything needs to be converted to ascii

        # TODO: extract to utils module
        def to_ascii(unicode_str):
            if unicode_str is None:
                return None
            return unicode_str.encode("ascii","replace")

        return dict(
            reported=str(self.reported),
            incident_type=str(self.incident_type),
            occurred_start=str(self.occurred_start),
            occurred_end=str(self.occurred_end),
            location=str(self.location),
            street_address=str(self.street_address),
            city=str(self.city),
            disposition=str(self.disposition)
        )
