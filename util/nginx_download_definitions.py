from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import json

def convert_syntax_name_to_directive_class_name(s):
    _s = s[0].upper() + s[1:]
    while True:
        if '_' in _s:
            _s = _s[:_s.index('_')] + _s[1 + _s.index('_')].upper() + _s[2 + _s.index('_'):]
        else:
            break
    return _s + "Directive"

def get_contexts_for_directive(s):
    return s.replace("Context: ","").split(", ")

def get_strings_for_row(s):
    try:
        syntax = re.findall("Syntax:\s*([^;\n]*)", s)[0]
    except:
        syntax = []
    try:
        default = re.findall("Default:\s*([^;\n]*)", s)[0]
    except:
        default = []
    try:
        contexts = re.findall("Syntax:\s*([^;\n]*)", s)[0]
    except:
        contexts = []
    
    return {
        "syntax": syntax,
        "default": default,
        "contexts": contexts
    }
    
driver = webdriver.Chrome()

driver.get('http://nginx.org/en/docs/http/ngx_http_core_module.html')

directives = driver.find_elements_by_xpath('//div[@class="directive"]')

table_rows = [d.find_elements_by_tag_name("tr") for d in directives]

directives = [get_strings_for_row('\n'.join([_row.text for _row in row])) for row in table_rows]

print(json.dumps(directives, indent=2))

