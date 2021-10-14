#!/usr/bin/python3

from NginxDirective import ProxyPassDirective, ProxyRedirectDirective, SetHeaderDirective


class Location:
    id = 0
    uri = ""
    port = ""
    directives = []

    def set_uri(self, uri):
        if uri[0] != '/':
            self.uri = self.set_uri('/' + uri)
        if uri[-1] != '/':
            self.uri = self.set_uri(uri + '/')
        self.uri = uri

    def __init__(self, id, uri, directives=[], port="80"):
        self.id = id
        self.uri = uri
        self.port = port
        self.directives = directives
        if uri[0] != '/':
            self.uri = '/' + self.uri
        if uri[-1] != '/':
            self.uri = self.uri + '/'

    def get_location_string(self):
        return f"""
        ##### START LOCATION ID: {str(self.id)} #####
        location ^~ {self.uri} {{
            {chr(9) + (chr(10) + chr(9) + chr(9)).join([directive.get_directive_text() for directive in self.directives])}
        }}
        ##### END LOCATION ID: {str(self.id)} #####
        """

    def get_location_string_expansion(self):
        return self.uri


class ProxyLocation(Location):

    def __init__(self, id, uri, port="80"):
        super().__init__(id, uri, directives=[
            SetHeaderDirective("X-Real-IP", "$remote_addr"),
            SetHeaderDirective("X-Forwarded-For", "$http_host"),
            SetHeaderDirective("Host", "$remote_addr"),
            SetHeaderDirective("X-NginX-Proxy", "true"),
            ProxyPassDirective(f"http://127.0.0.1:{port}/"),
            ProxyRedirectDirective("http://", "https://")
        ], port=port)

    def get_location_string_expansion(self):
        return f"^~ {self.uri}"



def get_location_template(template, *args, **kwargs):
    if template == 'html':
        return HTMLLocation(args, kwargs)
    if template == 'proxy':
        return ProxyLocation(args, kwargs)
    return None
