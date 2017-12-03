import datetime
import pytz
import re

def hour_to_24(hour, meridian):
    """
    Converts a 12-hour representation to a 24-hour representation.
    e.g.
        12, "AM" => 0
         6, "AM" => 6
        12, "PM" => 12
         3, "PM" => 15
        11, "PM" => 23
    """

    # first, if it's 12 whatever, subtract the 12 because it's actually 0
    if hour == 12:
        hour -= 12

    # if it's PM, add 12
    if meridian == "PM":
        hour += 12

    return hour

def parse_datetime_tuple(dt_tuple):
    """
    Converts a tuple like ('11', '27', '17', '5', '45', 'PM')
    into a proper Python datetime object.

    It MUST be 6 elements long and have exactly the right
    order of elements.
    """

    if len(dt_tuple) != 6:
        raise ValueError

    # abbreviate for simplicity
    R = dt_tuple

    # convert this to a datetime
    # year is encoded as 2-digit
    year = 2000 + int(R[2])
    month = int(R[0])
    day = int(R[1])
    # need to convert this 12-hour representation to 24-hours
    hour = hour_to_24(int(R[3]), R[5])
    minute = int(R[4])
    # no seconds

    # TODO: set timezone as EST; see
    # https://docs.python.org/2/library/datetime.html#datetime-objects
    # it's something like
    #     timezone = pytz.timezone("America/New_York")
    dt = datetime.datetime(year, month, day, hour, minute)
    return dt

def parse_raw_occurrence_data(occurrence_array):
    """
    Parses a list of 2 elements that represents
    when an incident occurred. The following formats
    are all supported:

    ["11/28/17","4:20 PM"],
    ["11/21/17","2:00 PM - 6:00 PM"],
    ["11/27/17 - 5:45 PM","11/28/17 - 9:00 AM"]

    Transforms this into a timestamp of when it started.
    """
    # concatenate and trim whitespace
    occurrence = (occurrence_array[0] + " | " + occurrence_array[1]).strip()

    print occurrence

    start = None
    end = None


    # CASE I: simplest, occurred at a constant time and not a range
    simple_matcher = re.compile(
        "^(\d{1,2})\/(\d{1,2})\/(\d{2}) \| (\d{1,2}):(\d{2}) ([A|P]M)$")
    simple_result = simple_matcher.findall(occurrence)
    if len(simple_result) > 0:
        # this matches Case I
        # return group length = 6
        # abbreviate this for simplicity
        R = simple_result[0]

        start = parse_datetime_tuple(R)
        # end time is same as start time
        end = start

    # CASE II: range of times on the SAME day
    range_matcher = re.compile(
        "^(\d{1,2})\/(\d{1,2})\/(\d{2}) \| (\d{1,2}):(\d{2}) ([A|P]M) - (\d{1,2}):(\d{2}) ([A|P]M)$")
    range_result = range_matcher.findall(occurrence)
    if len(range_result) > 0:
        # this matches Case II
        # return group length = 9
        # abbreviate this for simplicity
        R = range_result[0]

        # convert to datetime
        # start has R[0, 1, 2, 3, 4, 5]
        # end has R[0, 1, 2, 6, 7, 8]

        start_tuple = R[0:6]
        start = parse_datetime_tuple(start_tuple)
        end_tuple = (R[0], R[1], R[2], R[6], R[7], R[8])
        end = parse_datetime_tuple(end_tuple)

    # CASE III: range of times ACROSS days
    # TODO: break this down across lines
    across_day_matcher = re.compile(
        "^(\d{1,2})\/(\d{1,2})\/(\d{2}) - (\d{1,2}):(\d{2}) ([A|P]M) \| (\d{1,2})\/(\d{1,2})\/(\d{2}) - (\d{1,2}):(\d{2}) ([A|P]M)$")
    across_day_result = across_day_matcher.findall(occurrence)
    if len(across_day_result) > 0:
        # this matches Case III
        # return group length = 12

        # abbreviate this for simplicity
        R = across_day_result[0]

        # convert start and end for datetime
        # start is encoded as elements [0,6); end is [6, 12)
        start = parse_datetime_tuple(R[0:6])
        end = parse_datetime_tuple(R[6:12])

    print start
    print end
    return (start, end)
