
from datetime import datetime, timedelta


# Format number
def format_number(current_number, match_number):

    current_number_string = f"{current_number}"
    match_number_string = f"{match_number}"

    if "." in match_number_string:
        match_decimals = len(match_number_string.split(".")[1])
        current_number_string = f"{current_number:.{match_decimals}f}"
        current_number_string = current_number_string[:]

        return current_number_string
    else:
        return f"{int(current_number)}"


# Format time
def format_time(timestamp):
    return timestamp.replace(microsecond=0).isoformat()


# Get ISO times
def get_ISO_times():

    # Get timestamps
    date_start_0 = datetime.now()
    date_start_1 = date_start_0 - timedelta(hours=100)
    date_start_2 = date_start_1 - timedelta(hours=100)
    date_start_3 = date_start_2 - timedelta(hours=100)
    date_start_4 = date_start_3 - timedelta(hours=100)

    # Format datetimes
    times_dictionary = {
        "range_1": {
            "from_iso": format_time(date_start_1),
            "to_iso": format_time(date_start_0),
        },
        "range_2": {
            "from_iso": format_time(date_start_2),
            "to_iso": format_time(date_start_1),
        },
        "range_3": {
            "from_iso": format_time(date_start_3),
            "to_iso": format_time(date_start_2),
        },
        "range_4": {
            "from_iso": format_time(date_start_4),
            "to_iso": format_time(date_start_3),
        },
    }

    return times_dictionary

