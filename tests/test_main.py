import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import main

def test_string_parsing():
    values = {
        '$2.8 million': 2800000,
        '$1.6 billion': 1600000000,
        '$3.85 billion': 3850000000,
        '$3 million': 3000000,
        '$2,880,000': 2880000
    }

    for string, value in values.iteritems():
        result = main.parse_box_office_gross_str(string)
        print 'Input: ' + string
        print 'Supposed to be: {0}'.format(value)
        print 'Result: ' + result
        print '\n'
        assert result is not None
        assert int(result) == value
