import navegador5 as nv 
import navegador5.url_tool as nvurl
import navegador5.head as nvhead
import navegador5.body as nvbody
import navegador5.cookie 
import navegador5.cookie.cookie as nvcookie
import navegador5.cookie.rfc6265 as nvrfc6265
import navegador5.jq as nvjq
import navegador5.js_random as nvjr
import navegador5.file_toolset as nvft
import navegador5.shell_cmd as nvsh
import navegador5.html_tool as nvhtml
import navegador5.solicitud as nvsoli
import navegador5.content_parser 
import navegador5.content_parser.amf0_decode as nvamf0
import navegador5.content_parser.amf3_decode as nvamf3

from lxml import etree
import lxml.html
import collections
import copy
import re
import urllib
import os
import json
import sys

from xdict.jprint import  pobj
from xdict.jprint import  print_j_str
from xdict import cmdline



print("-cpresence options:")
pobj(['present','possible','absent','reported'])

print('----------------------------------------------')

print("-vhabitat options:")
pobj(['Saltwater', 'Commercial', 'Introduced', 'All', 'Reef-associated', 'Dangerous', 'Game fishes', 'Pelagic', 'Endemic', 'Freshwater', 'Threatened', 'Deep-water'])            
pobj(['saltwater', 'commercial', 'introduced', 'alpha2', 'reef', 'dangerous', 'sports', 'pelagic', 'endemic', 'fresh', 'threatened', 'deepwater'])

print('----------------------------------------------')

print("webcrawler usage:")
print('''
    step1: python3 show_country_code.py Mal       (to get country full name)
    step2: python3 show_country_code.py Malaysia  (to get country_code)
    step3: python3 ./WEBCRAWLER/fishbase.us.country.py -country_code 458 -cpresence present -vhabitat saltwater
'''
)





