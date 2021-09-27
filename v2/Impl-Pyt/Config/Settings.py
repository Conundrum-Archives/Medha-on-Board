import os
import json
import configparser

class Config():
    config_path = os.path.dirname(os.path.realpath(__file__))
    def __init__(self):
        # define properties.json variable
        property_file = os.path.join(self.config_path, "properties.json")

        # define crons.ini variable
        values_file = os.path.join(self.config_path, "values.ini")

        # check if property file exist
        if (not os.path.exists(property_file)):
            # if not exist raise file not found exception
            raise OSError("Config file {filename} not found.".format(filename=property_file))

        # check if crons file exist
        if (not os.path.exists(values_file)):
            # if not exist raise file not found exception
            raise OSError("Config file {filename} not found.".format(filename=values_file))

        # read properties file
        with open(property_file) as props:
            self.property = json.load(props)
        # read cron file
        self.values = configparser.ConfigParser()
        self.values.read(values_file)


class Schema():
    schema_path = os.path.dirname(os.path.realpath(__file__))
    def __init__(self):
        # define properties.json variable
        schema_file = os.path.join(self.schema_path, "SCHEMA_properties.json")

        # check if property file exist
        if (not os.path.exists(schema_file)):
            # if not exist raise file not found exception
            raise OSError("Config file {filename} not found.".format(filename=schema_file))

        # read properties file
        with open(schema_file) as sch:
            self.schema_properties = json.load(sch)