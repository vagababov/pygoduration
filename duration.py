# -*- coding: utf-8 -*-

_keys = {"ns":1e-9, "µs": 1e-6, "us":1e-6, "ms":1e-3, "s":1., "m":60., "h":3600.}

def parse_duration(dur):
    """Parses Golang time.Duration string representation.

    parse_duration takes in a possible signed string of golang time.Duration
    and converts it to seconds as a floating point number (akin to time.time()).
    See https://golang.org/pkg/time/#ParseDuration for details.

    Args:
        dur: string expressing duration.
    Returns:
        duration expressed as floating point number of seconds.
    
    """
    def to_secs(val, unit):
        if unit not in _keys:
            raise Exception('invalid unit "{0}"'.format(unit))
        # This will raise value error if the string is not proper FP.
        return float(val)*_keys[unit]

    if not dur:
        return None
    sign = 1
    was_sign = 0
    if dur[0] == '-':
        sign = -1
        was_sign = 1
        dur = dur[1:]
    elif dur[0] == '+':
        dur = dur[1:]
        was_sign = 1
    ret = 0.0
    value = ''
    unit = ''
    for i in xrange(len(dur)):
        c = dur[i]
        isd = c.isdigit() or c == '.' # Golang only supports fractional parts.
        # Not in number and encounter a char.
        if not value and not isd:
            raise Exception('invalid character at position {0}'.format(
                i+was_sign))
        # End of a digit run.
        if value and not isd:
            unit += c
        else: # isd==true
            # unit complete.
            if unit:
                ret += to_secs(value, unit)
                value = ''
                unit = ''
            value += c
    # Number with no unit.
    if value and not unit:
        raise Exception('missing unit in duration {0}'.format(value))
    ret += to_secs(value, unit)
    return ret*sign

