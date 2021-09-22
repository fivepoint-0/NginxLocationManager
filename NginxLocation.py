#!/usr/bin/python3

class NginxLocation:
    id = 0
    uri = ""
    port = ""
    options = []
    
    def get_location_string(self):
        return f"""
        ##### START LOCATION ID: {str(self.id)} #####
        location ^~ {self.uri} {{
            {chr(9) + (chr(10) + chr(9) + chr(9)).join([option.get_option_text() for option in self.options])}
        }}
        ##### END LOCATION ID: {str(self.id)} #####
        """

    def set_uri(self, uri):
        if uri[0] != '/': self.uri = self.set_uri('/' + uri)
        if uri[-1] != '/': self.uri = self.set_uri(uri + '/')
        self.uri = uri

    def __init__(self, id, uri, options = [], port = "80"):
        self.id = id
        self.uri = uri
        self.port = port
        self.options = options
        if uri[0] != '/': self.uri = '/' + self.uri
        if uri[-1] != '/': self.uri = self.uri + '/'

    

    