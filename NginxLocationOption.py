#!/usr/bin/python3
import re

class NginxLocationOption:
    option_name = "OPTION"

    def __init__(self, option_name="OPTION"):
        self.option_name = option_name

    def __str__(self) -> str:
        return self.get_option_text()
    
    def get_option_text(self) -> str:
        return f"{self.option_name} {self.get_option_expansion()};"

    def get_option_expansion(self) -> str:
        return ""

class SetHeaderOption(NginxLocationOption):
    def __init__(self, header, value):
        super().__init__("proxy_set_header")
        self.header = header
        self.value = value
    
    def get_option_expansion(self) -> str:
        return f"{self.header} {self.value}"
    
class ProxyPassOption(NginxLocationOption):
    url_to_pass_to = "http://127.0.0.1/"

    def __init__(self, url_to_pass_to: str = "http://127.0.0.1/"):
        super().__init__("proxy_pass")
        self.url_to_pass_to = url_to_pass_to
    
    def get_option_expansion(self) -> str:
        return f"{self.url_to_pass_to}"

class ProxyRedirectOption(NginxLocationOption):
    from_pattern = 'http://'
    to_pattern = 'https://'

    def __init__(self, from_pattern = 'http://', to_pattern = 'https://'):
        super().__init__("proxy_redirect")
        self.from_pattern = from_pattern
        self.to_pattern = to_pattern
    
    def get_option_expansion(self) -> str:
        return f"{self.from_pattern} {self.to_pattern}"

class OptionParser:
    def __init__(self):
        pass

    def parse_option(self, option_str: str):
        try:
            splits = re.split("\s+", option_str)
            if len(splits) > 0:
                option_name = splits[0]
                if option_name == 'proxy_redirect': return ProxyRedirectOption(splits[1], splits[2])
                if option_name == 'proxy_set_header': return SetHeaderOption(splits[1], splits[2])
                if option_name == 'proxy_pass': return ProxyPassOption(splits[1])
            return None
        except: 
            return None