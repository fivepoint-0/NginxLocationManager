#!/usr/bin/python3
import re

class Directive:
    directive_name = "DIRECTIVE"

    def __init__(self, directive_name="DIRECTIVE"):
        self.directive_name = directive_name

    def __str__(self) -> str:
        return self.get_directive_text()
    
    def get_directive_text(self) -> str:
        return f"{self.directive_name} {self.get_directive_expansion()};"

    def get_directive_expansion(self) -> str:
        return ""

class SetHeaderDirective(Directive):
    def __init__(self, header, value):
        super().__init__("proxy_set_header")
        self.header = header
        self.value = value
    
    def get_directive_expansion(self) -> str:
        return f"{self.header} {self.value}"
    
class ProxyPassDirective(Directive):
    def __init__(self, url_to_pass_to: str = "http://127.0.0.1/"):
        super().__init__("proxy_pass")
        self.url_to_pass_to = url_to_pass_to
    
    def get_directive_expansion(self) -> str:
        return f"{self.url_to_pass_to}"

class ProxyRedirectDirective(Directive):
    def __init__(self, from_pattern = 'http://', to_pattern = 'https://'):
        super().__init__("proxy_redirect")
        self.from_pattern = from_pattern
        self.to_pattern = to_pattern
    
    def get_directive_expansion(self) -> str:
        return f"{self.from_pattern} {self.to_pattern}"

class RootDirective(Directive):
    def __init__(self, directory="/var/www/html"):
        super().__init__(directive_name="root")
        self.directory = directory

    def get_directive_expansion(self) -> str:
        return self.directory

class IndexDirective(Directive):
    def __init__(self, pattern="$uri $uri/ =404"):
        super().__init__(directive_name="try_files")
        self.pattern = pattern

    def get_directive_expansion(self) -> str:
        return self.pattern

class ListenDirective(Directive):
    pass

class ServerNameDirective(Directive):
    pass

class DirectiveParser:
    def __init__(self):
        pass

    def parse_directive(self, directive_str: str):
        try:
            splits = re.split("\s+", directive_str)
            if len(splits) > 0:
                directive_name = splits[0]
                if directive_name == 'proxy_redirect': return ProxyRedirectDirective(splits[1], splits[2])
                if directive_name == 'proxy_set_header': return SetHeaderDirective(splits[1], splits[2])
                if directive_name == 'proxy_pass': return ProxyPassDirective(splits[1])
            return None
        except: 
            return None