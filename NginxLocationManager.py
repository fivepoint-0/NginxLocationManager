#!/usr/bin/python3

import re
from .NginxLocation import NginxLocation
from .NginxDirective import OptionParser, ProxyPassOption, ProxyRedirectOption, SetHeaderOption

class LocationManager:
    config_file = ""
    config_file_data = ""
    locations = []
    regex = {
        "START_LOCATION_CONFIG_REGEX": "##### START LOCATIONS CONFIG #####",
        "END_LOCATION_CONFIG_REGEX": "##### END LOCATIONS CONFIG #####",
        "START_LOCATION_ID_REGEX": "##### START LOCATION ID: \d* #####",
        "END_LOCATION_ID_REGEX": "##### END LOCATION ID: \d* #####",
        "GET_LOCATION_ID_REGEX": "ID: (\d*)",
        "GET_LOCATION_URI_REGEX": "/(.*)/"
    }

    def __init__(self, config_file="/etc/nginx/sites-available/default"):
        self.config_file = config_file
        with open(self.config_file, 'r+') as h:
            self.config_file_data = h.read()

    def parse_locations(self):
        locations_matches = re.findall(f"{self.regex['START_LOCATION_ID_REGEX']}[^#####]*{self.regex['END_LOCATION_ID_REGEX']}", self.config_file_data)
        locations = [line.split("\n") for line in locations_matches]
        
        option_parser = OptionParser()

        for location in locations:            
            _id = re.findall(self.regex['GET_LOCATION_ID_REGEX'], location[0])[0]
            _uri = re.findall(self.regex['GET_LOCATION_URI_REGEX'], location[1])[0]            
            _location = NginxLocation(_id, _uri)
            _location.options = [option_parser.parse_option(option.strip().replace(";", "")) for option in location[1:-1] if option_parser.parse_option(option.strip().replace(";", ""))]
            self.locations.append(_location)

    def get_locations_config_string(self):
        return "\n\n\t" + self.regex['START_LOCATION_CONFIG_REGEX'] + "\n\n" + '\n'.join([location.get_location_string() for location in self.locations]) + "\n\n\t" + self.regex['END_LOCATION_CONFIG_REGEX'] + "\n\n"

    def _update_location_ids(self):
        location_index = 0
        
        for location in self.locations:
            self.locations[self.locations.index(location)].id = location_index
            location_index += 1

    def create_location(self, uri="/uri-location/", options=[
        SetHeaderOption('X-Real-IP', '$remote_addr'),
        SetHeaderOption('X-Forwarded-For', '$http_host'),
        SetHeaderOption('Host', '$remote_addr'),
        SetHeaderOption('X-NginX-Proxy', 'true'),
        ProxyPassOption('http://127.0.0.1:3000/'),
        ProxyRedirectOption('http://', 'https://')
    ]):
        new_id = len(self.locations)
        location = NginxLocation(new_id, uri, options)
        self.locations.append(location)
        return location
    
    def delete_location(self, id):
        self.locations = list(filter((lambda x: x.id != id), self.locations))
        self._update_location_ids()

    def update_location(self, id, uri="", options=[]):
        self._update_location_ids()
        if uri != "": self.locations[id].uri = uri
        if len(options) > 0:
            for option in options:
                if option.option_name in list(map((lambda o: o.option_name), self.locations[id].options)):
                    self.locations[id].options = list(filter((lambda o: o.option_name != option.option_name), self.locations.options))
                self.locations[id].options.append(option)
    
    def get_internal_config_string(self):
        file_lines = self.config_file_data.split("\n")
        stripped_file_lines = [line.strip() for line in file_lines]
        locations_config_start_index = stripped_file_lines.index(self.regex['START_LOCATION_CONFIG_REGEX'])
        locations_config_end_index = stripped_file_lines.index(self.regex['END_LOCATION_CONFIG_REGEX'])
        replaced_line_config_start = '\n'.join(file_lines[:locations_config_start_index])
        replaced_line_config_end = '\n'.join(file_lines[locations_config_end_index + 1:])
        return replaced_line_config_start + self.get_locations_config_string() + replaced_line_config_end
    
    def save_locations(self):    
        with open(self.config_file, 'w+') as h:
            h.write(self.get_internal_config_string())
            