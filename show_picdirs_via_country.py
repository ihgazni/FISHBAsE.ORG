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





import os
import subprocess
import shlex

def pipe_shell_cmds(shell_CMDs):
    '''
        shell_CMDs = {}
        shell_CMDs[1] = 'netstat -n'
        shell_CMDs[2] = "awk {'print $6'}"
    '''
    len = shell_CMDs.__len__()
    p = {}
    p[1] = subprocess.Popen(shlex.split(shell_CMDs[1]), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    for i in range(2,len):
        p[i] = subprocess.Popen(shlex.split(shell_CMDs[i]), stdin=p[i-1].stdout, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if(len > 1):
        p[len] = subprocess.Popen(shlex.split(shell_CMDs[len]), stdin=p[len-1].stdout, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = p[len].communicate()
    if(len > 1):
        for i in range(2,len+1):
            returncode = p[i].wait()
    else:
        returncode = p[len].wait()
    return(result)


def imageMagick_close():
    shell_CMDs = {}
    shell_CMDs[1] = 'ps -ef'
    shell_CMDs[2] = 'egrep display'
    shell_CMDs[3] = 'egrep -v egrep'
    shell_CMDs[4] = "awk {'print $2'}"
    rslt = pipe_shell_cmds(shell_CMDs)
    rslt = rslt[0].decode('utf-8')
    rslt = rslt.strip('\n')
    rslt = rslt.split('\n')
    for i in range(0,rslt.__len__()):
        os.system('kill ' + rslt[i])


#-fishname
fishname = sys.argv[2]
#-country
country = sys.argv[4]
#-cpresence 
cpresence = sys.argv[6]
#-vhabitat
vhabitat = sys.argv[8]



#country_info_dir = "./INFOS/COUNTRYANDISLAND/Malaysia/present/saltwater/"

country_info_dir = "./INFOS/COUNTRYANDISLAND/"+country + "/" + cpresence + "/" + vhabitat + "/"

def read_and_loads_json(country_info_dir,fn):
    fd = open(country_info_dir+fn,'r')
    content = fd.read()
    d = json.loads(content)
    fd.close()
    return(d)

dir_image = read_and_loads_json(country_info_dir,'dir_image.dict')
dir_thumb = read_and_loads_json(country_info_dir,'dir_thumb.dict')
fishes = read_and_loads_json(country_info_dir,'fishes.dict')
image_dir = read_and_loads_json(country_info_dir,'image_dir.dict')
thumb_dir = read_and_loads_json(country_info_dir,'thumb_dir.dict')

if(fishname in fishes):
    pass
else:
    def search_fishname(fishname):
        shell_CMDs = {}
        shell_CMDs[1] = 'ls -l ' + country_info_dir
        shell_CMDs[2] = 'egrep "' +fishname +'"'
        shell_CMDs[3] = "awk {'print $9 \" \" $10'}"
        rslt = pipe_shell_cmds(shell_CMDs)
        rslt = rslt[0].decode('utf-8')
        rslt = rslt.strip('\n')
        rslt = rslt.split('\n')
        return(rslt)
    pobj(search_fishname(fishname))
    #cmdt = cmdline.cmdict(dict=fishes)
    #cmdt[fishname]
    exit()

all_photos = fishes[fishname]['All-Photos']
picdirs = []
for photo in all_photos:
    if('img-name' in photo):
        imagename = photo['img-name']
        picdirs.append(image_dir[imagename])
    else:
        pass
pobj(picdirs)


##############################################
#-which 
def arr_which(which):
    regex = re.compile('[ ]+')
    which = regex.sub(which,' ')
    arr = which.split(' ')
    return(arr)


try:
    which = sys.argv[10]
except:
    arr = []
    for i in range(0,picdirs.__len__()):
        arr.append(i)
else:
    arr = arr_which(which)
###############################################



imageMagick_close()

from PIL import Image
def get_exif_data(img):
    '''
        http://www.cipa.jp/std/documents/e/DC-008-2012_E.pdf
    '''
    ret = {}
    exifinfo = img._getexif()
    if(exifinfo != None):
        for tag, value in exifinfo.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
    if(50341 in ret):
        ret['PrintImageMatching'] = ret[50341]
        del ret[50341]
    return(ret)








for each in arr:
    img=Image.open('.' + picdirs[each].strip('.'))
    img.show()
    img.close()

#python3 show_picdirs_via_country.py -fishname "Zoramia viridiventer" -country Malaysia -cpresence present -vhabitat saltwater
#python3 show_picdirs_via_country.py -fishname "Zora" -country Malaysia -cpresence present -vhabitat saltwater

