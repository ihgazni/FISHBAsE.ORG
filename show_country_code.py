import json
import sys
from xdict.jprint import pobj
from xdict import cmdline

fd = open('./INFOS/country.dict','r')
cd = fd.read()
cd = json.loads(cd)
fd.close()

cmd = sys.argv[1]

try:
    print(cd[cmd])
except:
    cmdt = cmdline.cmdict(dict=cd)
    cmdt[cmd]
else:
    pass

