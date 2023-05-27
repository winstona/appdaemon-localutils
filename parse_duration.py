

from datetime import timedelta
import re


def parse_time(time_str):
    regex = re.compile(
                   r'((?P<weeks>[.\d]+?)w)?'
                   r'((?P<days>[.\d]+?)d)?'
                   r'((?P<hours>[.\d]+?)h)?'
                   r'((?P<minutes>[.\d]+?)m)?'
                   r'((?P<seconds>[.\d]+?)s)?'
                   r'((?P<microseconds>[.\d]+?)ms)?'
                   r'((?P<milliseconds>[.\d]+?)us)?$'
                   )
    parts = regex.match(time_str)
    assert parts is not None, "Could not parse any time information from '{}'.  Examples of valid strings: '8h', '2d8h5m20s', '2m4s'".format(time_str)
    time_params = {name: float(param) for name, param in parts.groupdict().items() if param}
    return timedelta(**time_params)
