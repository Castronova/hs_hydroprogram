__author__ = 'tonycastronova'
"""
Utility functions for parsing science metadata from ini
"""

import ConfigParser
import cPickle as pickle
import datetime

class metadata_type_struct():

    title = 'str'
    type = 'str'
    abstract = 'str'
    language = 'str'
    subject = 'str'
    format = 'str'
    name='str'
    creatorOrder='int'
    organization = 'str'
    email = 'str'
    address = 'str'
    phone = 'str'
    homepage = 'str'
    researcherID = 'str'
    researchGateID = 'str'
    created = '%Y-%m-%d %H:%M:%S'
    modified = '%Y-%m-%d %H:%M:%S'
    valid = '%Y-%m-%d %H:%M:%S'
    rightsStatement = 'str'
    rightsURL =  'str'
    version = 'str'
    releaseDate = '%Y-%m-%d'
    url = 'str'
    description = 'str'


class multidict(dict):
    _unique = 0

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            self._unique += 1
            key += '^'+str(self._unique)
        dict.__setitem__(self, key, val)



def validate(ini_path):

    cparser = ConfigParser.ConfigParser(None, multidict)

     # parse the ini
    cparser.read(ini_path)

    # get the ini sections from the parser
    parsed_sections = cparser.sections()

    # load lookup tables
    var = pickle.load(open('../data/var_cv.dat','rb'))
    unit = pickle.load(open('../data/units_cv.dat','rb'))

    # todo: validate phone numbers using regex
    # todo: validate emails using regex
    # todo: allow dates to have utcoffset embedded
    # todo: validate that format is of a recognized type (application/zip, application/octet-stream)
    # todo: make sure subject is delimited by a semicolon

    # validate
    for section in parsed_sections:
        # get ini options
        options = cparser.options(section)

        # validate units and variables parameters
        if section.split('_')[0] == 'output' or section.split('_')[0] == 'input':
            # check that variable and unit exist
            if 'variable_name_cv' not in options or 'unit_type_cv' not in options:
                raise Exception ('Inputs and Outputs must contain "variable_name_cv" and "unit_type_cv" parameters ')

        # check each option individually
        for option in options:
            val = cparser.get(section,option)

            # validate date format
            if option == 'simulation_start' or option == 'simulation_end':
                try:
                    datetime.datetime.strptime(val, getattr(metadata_type_struct, option))
                except ValueError:
                    raise ValueError("Incorrect data format, should be "+getattr(metadata_type_struct, option))
            else:
                # validate data type
                if not isinstance(val,type(getattr(metadata_type_struct, option))):
                    raise Exception(option+' is not of type '+getattr(metadata_type_struct, option))

                # check variable cv (i.e. lookup table)
                if option == 'variable_name_cv':
                    if val not in var:
                        raise Exception (val+' is not a valid controlled vocabulary term')

                # check unit type cv (i.e. lookup table)
                if option == 'unit_type_cv':
                    if val not in unit:
                        raise Exception (val+' is not a valid controlled vocabulary term')

    return 1