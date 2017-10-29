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
#-picname
picname = sys.argv[2]
#-country
country = sys.argv[4]
#-cpresence 
cpresence = sys.argv[6]
#-vhabitat
vhabitat = sys.argv[8]

country_info_dir = "./INFOS/COUNTRYANDISLAND/"+country + "/" + cpresence + "/" + vhabitat + "/"

def read_and_loads_json(country_info_dir,fn):
    fd = open(country_info_dir+fn,'r')
    content = fd.read()
    d = json.loads(content)
    return(d)

dir_image = read_and_loads_json(country_info_dir,'dir_image.dict')
dir_thumb = read_and_loads_json(country_info_dir,'dir_thumb.dict')
fishes = read_and_loads_json(country_info_dir,'fishes.dict')
image_dir = read_and_loads_json(country_info_dir,'image_dir.dict')
thumb_dir = read_and_loads_json(country_info_dir,'thumb_dir.dict')

def get_fishname_from_imagename(imagename):
    fishname = imagename.split('__')[0].replace('_',' ')
    return(fishname)

pobj(fishes[get_fishname_from_imagename(picname)])

#####################
#python3 show_fishinfo_via_country.py -picname Solenostomus_paradoxus__1343207904_82.243.202.40.jpg -country Malaysia -cpresence present -vhabitat saltwater
####################





