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

def fishbase_init(base_url='http://www.fishbase.us/'):
    info_container = nvsoli.new_info_container()
    info_container['base_url'] = base_url
    info_container['url'] = base_url
    info_container['method'] = 'GET'
    req_head_str = '''Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36\r\nAccept-Encoding: gzip,deflate,sdch\r\nAccept-Language: en;q=1.0, zh-CN;q=0.8'''
    info_container['req_head'] = nvhead.build_headers_dict_from_str(req_head_str,'\r\n')
    info_container['req_head']['Connection'] = 'close'
    #### init records_container
    records_container = nvsoli.new_records_container()
    info_container = nvsoli.walkon(info_container,records_container=records_container)
    info_container = nvsoli.auto_redireced(info_container,records_container)
    return((info_container,records_container))

def get_printed_str(obj,with_color=1,display=1):
    s = obj.__str__()
    pls = print_j_str(s,with_color=with_color,display=display)
    ps = ''
    for n in pls:
        ps = ''.join((ps,pls[n],'\n'))
    return(ps)

def get_etree_root(info_container):
    html_text = info_container['resp_body_bytes'].decode('utf-8')
    root = etree.HTML(html_text)
    return(root)

def get_country_island_dict(root,database_parent_dir='../'):
    d = {}
    eles_country= root.xpath('//select[@name="Country"]/option')
    for i in range(1,eles_country.__len__()):
        code = eles_country[i].get('value')
        country = eles_country[i].text
        d[code] = country
        d[country] = code
    exact_dir = ''.join((database_parent_dir,'INFOS/'))
    if(os.path.exists(exact_dir)):
        pass
    else:
        os.makedirs(exact_dir)
    exact_dir = ''.join((database_parent_dir,'INFOS/country.dict'))
    nvft.write_to_file(fn=exact_dir,content=json.dumps(d),op='w+')
    exact_dir = ''.join((database_parent_dir,'INFOS/country.info'))
    info = get_printed_str(d,with_color=0,display=0)
    nvft.write_to_file(fn=exact_dir,content=info,op='w+')
    return(d)

def get_country_island_dict(root,database_parent_dir='../',display=0):
    d = {}
    eles_country= root.xpath('//select[@name="Country"]/option')
    for i in range(1,eles_country.__len__()):
        code = eles_country[i].get('value')
        country = eles_country[i].text
        d[code] = country
        d[country] = code
    exact_dir = ''.join((database_parent_dir,'INFOS/'))
    if(os.path.exists(exact_dir)):
        pass
    else:
        os.makedirs(exact_dir)
    exact_dir = ''.join((database_parent_dir,'INFOS/country.dict'))
    nvft.write_to_file(fn=exact_dir,content=json.dumps(d),op='w+')
    exact_dir = ''.join((database_parent_dir,'INFOS/country.info'))
    info = get_printed_str(d,with_color=0,display=display)
    nvft.write_to_file(fn=exact_dir,content=info,op='w+')
    return(d)

def gen_CI_post_body(**kwargs):
    query_dict = {}
    if('Language' in kwargs):
        query_dict['Language'] = kwargs['Language']
    else:
        query_dict['Language'] = 'English'
    if('Country_required' in kwargs):
        query_dict['Country_required'] = kwargs['Country_required']
    else:
        query_dict['Country_required'] = 'Choose country/island to proceed.'
    if('region' in kwargs):
        query_dict['region'] = kwargs['region']
    else:
        query_dict['region'] = ''
    if('c_code_onclick' in kwargs):
        query_dict['c_code_onclick'] = kwargs['c_code_onclick']
    else:
        query_dict['c_code_onclick'] = ''
    if('Country' in kwargs):
        query_dict['Country'] = kwargs['Country']
    else:
        query_dict['Country'] = 458
    if('group' in kwargs):
        query_dict['group'] = kwargs['group']
    else:
        query_dict['group'] = 'allfishes'
    return(urllib.parse.urlencode(query_dict))

def search_via_country(c_code,info_container,records_container):
    req_body = gen_CI_post_body(Country=c_code)
    ciurl = info_container['base_url']+ 'country/CountrySearchList.php'
    info_container['req_head']['Referer'] = info_container['base_url']
    info_container['req_head']['Upgrade-Insecure-Requests'] = 1
    info_container['req_head']['Content-Type'] = 'application/x-www-form-urlencoded'
    info_container['url'] = ciurl
    info_container['method'] = 'POST'
    info_container['req_body'] = req_body
    info_container = nvsoli.walkon(info_container,records_container=records_container)
    info_container['method'] = 'GET'
    info_container = nvsoli.auto_redireced(info_container,records_container)
    html_text = info_container['resp_body_bytes'].decode('utf-8')
    root = etree.HTML(html_text)
    return(root)

def get_all_tables(root,base_url):
    d = {0:'present',1:'possible',2:'absent',3:'reported','present':0,'possible':1,'absent':2,'reported':3}
    tables = {}
    eles = root.xpath('//div[@class="info"]/a')
    for i in range(0,eles.__len__()):
        href = eles[i].get('href')
        href = href.lstrip('/')
        href = base_url + href
        tables[i] = href
        tables[d[i]] = href
        tables[href] = d[i]
    return(tables)

def mirror_dict(d):
    nd = {}
    for k in d:
        nd[d[k]] = k
        nd[k] = d[k]
    return(nd)


def get_sortby():
    # sortby = {}
    # eles = root.xpath('//input[@name="sortby"]')
    # for i in range(0,eles.__len__()):
        # ele = eles[i]
        # value = ele.get('value')
        # text = ele.text()
        # sortby[value] = text
        # sortby[text] = value
    # return(sortby)
    sortby = {
        'Species': 'alpha2', 
        'Phylogenetic': 'phylo',  
        'Extended checklist': 'ext_CL', 
        'Show photos': 'ext_pic',  
        'Family': 'alpha',  
        'Occurrence': 'status'
    }
    pobj(sortby)
    return(sortby)

def get_vhabitat():
    # vhabitat = {}
    # eles = root.xpath('//input[@name="vhabitat"]')
    # for i in range(0,eles.__len__()):
        # ele = eles[i]
        # value = ele.get('value')
        # text = ele.text()
        # vhabitat[value] = text
        # vhabitat[text] = value
    # return(vhabitat)
    vhabitat = {
        'All': 'alpha2', 
        'Freshwater': 'fresh',  
        'Saltwater': 'saltwater', 
        'Introduced': 'introduced',  
        'Endemic': 'endemic',  
        'Threatened': 'threatened',
        'Dangerous': 'dangerous', 
        'Reef-associated': 'reef',  
        'Pelagic': 'pelagic',  
        'Deep-water': 'deepwater',
        'Game fishes': 'sports',  
        'Commercial': 'commercial'
    }
    pobj(vhabitat)
    return(vhabitat)

def dict_merge_update(d1,d2):
    for k in d2:
        v = d2[k]
        d1[k] = v
    return(d1)
            

def get_query_url(info_container,kwargs):
    query_dict = {}
    if('sortby' in kwargs):
        sb = kwargs['sortby']
    else:
        sb = 'Species'
    sortby = get_sortby()
    if(sb in sortby):
        sb = sortby[sb]
    else:
        sb = sb
    if(sb == None):
        pass
    else:
        query_dict['sortby'] = sb
    if('ext_pic' in kwargs):
        ep = kwargs['ext_pic']
    else:
        ep = 'on'
    if(ep == None):
        pass
    else:
        query_dict['ext_pic'] = ep
    if('ext_CL' in kwargs):
        ec = kwargs['ext_CL']
    else:
        ec = 'on'
    if(ec == None):
        pass
    else:
        query_dict['ext_CL'] = ec
    if('vhabitat' in kwargs):
        vh = kwargs['vhabitat']
    else:
        vh = 'saltwater'
    vhabitat = get_vhabitat()
    if(vh in vhabitat):
        vh = vhabitat[vh]
    else:
        vh = vh
    if(vh == None):
        pass
    else:
        query_dict['vhabitat'] = vh
    if('resultPage' in kwargs):
        rp = kwargs['resultPage']
    else:
        rp = None
    if(rp == None):
        pass
    else:
        query_dict['resultPage'] = rp
    url_dict = nvurl.url_to_dict(info_container['url'])
    qd = nvurl.urldecode(url_dict['query'])
    nqd = dict_merge_update(qd,query_dict)
    nqd['what'] = 'list'
    nqd['trpp'] = 999999
    if('cpresence' in kwargs):
        nqd['cpresence'] = kwargs['cpresence']
    else:
        nqd['cpresence'] = 'present'
    if('showAll' in kwargs):
        nqd['showAll'] = kwargs['showAll']
    else:
        nqd['showAll'] = 'yes'
    if(nqd['showAll'] == None):
        del nqd['showAll']
    else:
        pass
    qurl = url_dict['scheme'] +'://' + url_dict['netloc']+url_dict['path']+'/?'+nvurl.urlencode(qd)
    return(qurl)

def itertext(ele):
    it = ele.itertext()
    texts = list(it)    
    text = ''
    for i in range(0,texts.__len__()):
        text = text + texts[i]
    return(text)

def get_fish_info(fishes,ele_fish,fish,info_container,records_container):
    new_fish = copy.deepcopy(fish)
    eles = ele_fish.getchildren()
    new_fish['Family'] = eles[0].text
    new_fish['Species'] = {}
    new_fish['Species']['name'] = eles[1].xpath("i/a")[0].text
    nfs_name = new_fish['Species']['name'].replace(' ','_')
    ####
    print(new_fish['Species']['name'])
    ####
    if(new_fish['Species']['name'] in fishes):
        ####
        print('----return None----')
        ####
        return(None)
    else:
        ####
        print('------continue new fish------')
        ####
        pass
    new_fish['Species']['id'] = int(nvurl.urldecode(eles[1].xpath("i/a")[0].get('href'))['id'])
    new_fish['Species']['url'] = info_container['base_url']+'country/'+ eles[1].xpath("i/a")[0].get('href')
    new_fish['Author'] = eles[2].text
    new_fish['Info'] = eles[3].text
    regex = re.compile('[\r\n\t]+')
    new_fish['Info'] = regex.sub('',new_fish['Info'])
    new_fish['Occurrence'] = eles[4].text.strip('\xa0').strip(' ').strip('\xa0')
    names = eles[5].text.split(',')
    new_fish['Common names'] = []
    for i in range(0,names.__len__()):
        new_fish['Common names'].append(names[i].strip('').strip('\xa0').strip(''))
    new_fish['Abundance'] = eles[6].text.strip('\xa0').strip(' ').strip('\xa0')
    new_fish['Max length'] = eles[7].text.strip('\xa0').strip(' ').strip('\xa0')
    new_fish['Maturity'] = eles[8].text.strip('\xa0').strip(' ').strip('\xa0')
    new_fish['Remark'] = eles[9].text.strip('\xa0').strip(' ').strip('\xa0')
    new_fish['Photo'] = {}
    if(eles.__len__()>=10):
        temp = eles[10].xpath('a')
        if(temp.__len__()>0):
            new_fish['Photo']['url'] = info_container['base_url']+temp[0].get('href')
        else:
            new_fish['Photo']['url'] = None
        #####
        new_fish['Presenting-Photo'] = {}
        try:
            new_fish['Presenting-Photo']['ID'] = int(nvurl.urldecode(eles[10].xpath('a')[0].get('href'))['/photos/ThumbnailsSummary.php?ID'])
            new_fish['Presenting-Photo']['thumbnail-url'] = info_container['base_url'].rstrip('/') + eles[10].xpath('a/img')[0].get('src')
        except:
            new_fish['Presenting-Photo']['ID'] = None
            new_fish['Presenting-Photo']['thumbnail-url'] = None
        else:
            pass
    else:
        new_fish['Photo']['url'] = None
        new_fish['Presenting-Photo'] = {}
        new_fish['Presenting-Photo']['ID'] = None
        new_fish['Presenting-Photo']['thumbnail-url'] = None
    new_fish['All-Photos'] = []
    info_container['url'] = new_fish['Photo']['url']
    if(info_container['url'] == None):
        pass
    else:
        info_container = nvsoli.walkon(info_container,records_container=records_container)
        html_text = info_container['resp_body_bytes'].decode('utf-8','ignore')    
        root = etree.HTML(html_text)
        #eles = root.xpath("//tr[@class='t_value1']")
        #eles = root.xpath("//tr[@align]")
        eles = root.xpath("//td[(@align) and (@width)]")
        for i in range(0,eles.__len__()):
            ele = eles[i]
            #photo_eles = ele.xpath('td')
            photo_eles = [ele]
            for j in range(0,photo_eles.__len__()):
                photo = {}
                photo_ele = photo_eles[j]
                tooltip = photo_ele.xpath("a[@class='tooltip']")
                if(tooltip.__len__()>0):
                    rel_sum_url = tooltip[0].get('href')
                    if(rel_sum_url.strip(' \t\r\n')== '#'):
                        photo['summary-url'] = '#'
                    else:
                        if('http' in rel_sum_url):
                            photo['summary-url'] = rel_sum_url.strip('.').strip('/').strip('.')
                        else:
                            photo['summary-url'] = info_container['base_url']+ 'photos/' + rel_sum_url.strip('.').strip('/').strip('.')
                else:
                    rel_sum_url = None
                    photo['summary-url'] = None
                #regex = re.compile('what=(.*)')
                #m = regex.search(photo['summary-url'])
                if(photo['summary-url'] == None):
                    photo['type'] = None
                    photo['external-url'] = None
                    photo['colaborator-url'] = None
                    photo['thumbnail-url'] = None
                    photo['img-url'] = None
                    photo['photographer'] = None
                elif(photo['summary-url'] == '#'):
                    photo['external-url'] = None
                    photo['colaborator-url'] = None
                    photo['thumbnail-url'] = info_container['base_url']+ 'photos/' + tooltip[0].xpath('img')[0].get('src')
                    photo['img-url'] = tooltip[0].xpath('span/img')[0].get('src')
                    photo['type'] = 'uploads'
                    text = itertext(tooltip[0].xpath('span')[0])
                    regex = re.compile('<.*>')
                    photo['photographer'] = regex.sub('',text).strip('\r\n\t ')
                    regex = re.compile('.*/(.*)')
                    m = regex.search(photo['img-url'])
                    img_name = nfs_name + '__' + m.group(1)
                    regex = re.compile('.*\.(.*)')
                    try:
                        img_type = regex.search(m.group(1)).group(1)
                    except:
                        img_type = None
                        img_name = None
                        photo['img-url'] = None
                        photo['thumbnail-url'] = None
                    else:
                        pass
                    photo['img-type'] = img_type
                    photo['img-name'] = img_name
                else:
                    if('http' in rel_sum_url):
                        photo['external-url'] = photo['summary-url']
                        photo['type'] = None
                    else:
                        photo['external-url'] = None
                        if('/Diseases/' in photo['summary-url']):
                            photo['type'] = 'Diseases'
                        else:
                            photo['type'] = nvurl.urldecode(photo['summary-url'])['what']
                        if('http' in photo_ele.xpath("a[not(@class)]")[0].get('href')):
                            photo['colaborator-url'] = photo_ele.xpath("a[not(@class)]")[0].get('href')
                        else:
                            photo['colaborator-url'] = info_container['base_url'].strip('/') + photo_ele.xpath("a[not(@class)]")[0].get('href')
                        if('http' in photo_ele.xpath('a/img')[0].get('src')):
                            photo['thumbnail-url'] = photo_ele.xpath('a/img')[0].get('src').strip('.')
                        else:
                            photo['thumbnail-url'] = info_container['base_url'].strip('/') + photo_ele.xpath('a/img')[0].get('src').strip('.')
                        if('http' in photo_ele.xpath('a/span/img')[0].get('src')):
                            photo['img-url'] = photo_ele.xpath('a/span/img')[0].get('src').strip('.')
                        else:
                            photo['img-url'] = info_container['base_url'].strip('/') + photo_ele.xpath('a/span/img')[0].get('src').strip('.')
                        regex = re.compile('.*/(.*)')
                        m = regex.search(photo['img-url'])
                        img_name = nfs_name + '__' + m.group(1)
                        regex = re.compile('.*\.(.*)')
                        try:
                            img_type = regex.search(m.group(1)).group(1)
                        except:
                            img_type = None
                            img_name = None
                            photo['img-url'] = None
                            photo['thumbnail-url'] = None
                        else:
                            pass
                        photo['img-type'] = img_type
                        photo['img-name'] = img_name
                        photo['photographer'] = itertext(photo_ele.xpath('a/span')[0])
                        regex = re.compile('[\r\n\t]+')
                        photo['photographer'] = regex.sub('',photo['photographer'])
                new_fish['All-Photos'].append(photo)
    return(new_fish)




def get_country_infos(c_code,country_island_dict,info_container,records_container,**kwargs):
    if('display' in kwargs):
        display = int(kwargs['display'])
    else:
        display = 0
    if('new_database' in kwargs):
        newdb = kwargs['new_database']
    else:
        newdb = 0
    ####
    #os.system('date')
    ####
    root = search_via_country(c_code,info_container,records_container)
    tables = get_all_tables(root,info_container['base_url'])
    qurl = get_query_url(info_container,kwargs)
    info_container['url'] = qurl
    info_container['method'] = 'GET'
    info_container['req_body'] = None
    info_container = nvsoli.walkon(info_container,records_container=records_container)
    html_text = info_container['resp_body_bytes'].decode('utf-8')
    root = etree.HTML(html_text)
    eles = root.xpath('//thead/tr/th')
    ####
    ####
    fish = {}
    for i in range(0,eles.__len__()):
        fish[eles[i].text] = None
    url_dict = nvurl.url_to_dict(info_container['url'])
    qd = nvurl.urldecode(url_dict['query'])        
    all_country_eles = root.xpath("//tr[@class='t_value1']")
    country = country_island_dict[str(c_code)]
    fn = '../INFOS/' + 'COUNTRYANDISLAND/' + country + '/' + qd['cpresence']+'/'+qd['vhabitat']+'/'
    if(os.path.exists(fn)):
        pass
    else:
        os.makedirs(fn)
    picfn = '../PICS/' + 'COUNTRYANDISLAND/' + country + '/' + qd['cpresence']+'/'+qd['vhabitat']+'/'
    if(os.path.exists(picfn)):
        pass
    else:
        os.makedirs(picfn)
    thumbfn = '../THUMBNAILS/' + 'COUNTRYANDISLAND/' + country + '/' + qd['cpresence']+'/'+qd['vhabitat']+'/'
    if(os.path.exists(thumbfn)):
        pass
    else:
        os.makedirs(thumbfn)
    ####

    ####
    ####
    if(bool(newdb)):
        fishes = {}
    else:
        fishes_dir = fn + "fishes.dict"
        print(fishes_dir)
        if(os.path.exists(fishes_dir)):
            fd = open(fishes_dir,'r+')
            fishes_text = fd.read()
            fishes = json.loads(fishes_text)
            fd.close()
        else:
            fishes = {}
    ####
    print('--------------------')
    from xdict.jprint import paint_str
    print(paint_str("===============fishes loads completed======================",single_color='yellow'))
    print(fishes.keys())
    print('----------------')
    #os.system('date') 
    ####
    for i in range(0,all_country_eles.__len__()):
        fish_ele = all_country_eles[i]
        nfish = get_fish_info(fishes,fish_ele,fish,info_container,records_container)
        ######
        print(paint_str("===============nfish load completed======================",single_color='green'))
        ######
        if(nfish):
            ####
            print("====handle new nfish========")
            ####
            nfish['eles-seq'] = i
            nfish['images-dir'] = picfn
            nfish['info-dir'] = fn
            fishes[nfish['Species']['name']] = nfish
            nfdir = fn + nfish['Species']['name'] + '/'
            if(os.path.exists(nfdir)):
                pass
            else:
                os.makedirs(nfdir)
            nffn = nfdir + 'fish.dict'
            infofn = nfdir + 'fish.info'
            nvft.write_to_file(fn=nffn,content=json.dumps(nfish),op='w+')
            info = get_printed_str(nfish,with_color=0,display=display)
            nvft.write_to_file(fn=infofn,content=info,op='w+')
            
        else:
            ####
            print("===bypass existed fish====")
            ####
            pass
    #---------------------------------------#
    ####
    print(paint_str("===============all  nfish es load completed======================",single_color='yellow'))
    print(fishes.keys())
    print(fishes.keys().__len__())
    ####
    dfn = fn + 'fishes.dict'
    if(os.path.exists(dfn)):
        pass
    else:
        nvft.write_to_file(fn=dfn,content=json.dumps(fishes),op='w+')
    ldfn = fn + 'fishes.lines'
    if(os.path.exists(ldfn)):
        pass
    else:
        nvft.write_to_file(fn=ldfn,content='',op='w+')
        for key in fishes:
            nfish = fishes[key]
            nvft.write_to_file(fn=ldfn,content=get_printed_str(nfish,with_color=0,display=display),op='a+')
            nvft.write_to_file(fn=ldfn,content='\n',op='a+')
    #---------------------------------------#
    ####
    print("-----get all_photos ready----")
    ####
    apafn = fn + 'pics.array'
    if(os.path.exists(apafn)):
        fd = open(apafn,'r+')
        apa_text = fd.read()
        all_photos = json.loads(apa_text)
        fd.close()
    else:
        all_photos = []
        for name in fishes:
            #all_photos = all_photos + copy.deepcopy(fishes[name]['All-Photos'])
            #all_photos = all_photos + copy.deepcopy(fishes[name]['All-Photos'])
            for photo in fishes[name]['All-Photos']:
                all_photos.append(photo)
    ####
    print("all_photos gotted")
    print(all_photos.__len__())
    ####
    types = []
    for each in all_photos:
        type = each['type']
        if(type in types):
            pass
        else:
            if(type == None):
                pass
            else:
                types.append(type)
    for type in types:
        typefn = picfn + type
        if(os.path.exists(typefn)):
            pass
        else:
            os.makedirs(typefn)
        typefn = thumbfn + type
        if(os.path.exists(typefn)):
            pass
        else:
            os.makedirs(typefn)
    for each in all_photos:
        if(each['type'] == None):
            each['img-dir'] = None
            each['thumb-dir'] = None
        else:
            img_dir = picfn + each['type'] + '/' + each['img-name']
            each['img-dir'] = img_dir
            thumb_dir = thumbfn + each['type'] + '/' + each['img-name']
            each['thumb-dir'] = thumb_dir
    apafn = fn + 'pics.array'
    if(os.path.exists(apafn)):
        pass
    else:
        nvft.write_to_file(fn=apafn,content=json.dumps(all_photos),op='w+')
    lapafn = fn + 'pics.lines'
    if(os.path.exists(lapafn)):
        pass
    else:
        nvft.write_to_file(fn=lapafn,content='',op='w+')
        for each in all_photos:
            nvft.write_to_file(fn=lapafn,content=get_printed_str(each,with_color=0,display=display),op='a+')
            nvft.write_to_file(fn=lapafn,content='\n',op='a+')
    ############################
    print("pics.lines and pics.array ready")
    ############################
    imagename_dir_dict = {}
    dir_imagename_dict = {}
    for each in all_photos:
        if(each['type'] != None):
            imagename = each['img-name']
            dir = each['img-dir']
        else:
            imagename = None
            dir = None
        imagename_dir_dict[imagename] = dir
        dir_imagename_dict[dir] = imagename
    iddfn = fn + 'image_dir.dict'
    didfn = fn + 'dir_image.dict'
    if(os.path.exists(iddfn)):
        pass
    else:
        nvft.write_to_file(fn=iddfn,content=json.dumps(imagename_dir_dict),op='w+')
    liddfn = fn + 'image_dir.lines'
    if(os.path.exists(liddfn)):
        pass
    else:
        nvft.write_to_file(fn=liddfn,content='',op='w+')
        for each in imagename_dir_dict:
            nvft.write_to_file(fn=liddfn,content=get_printed_str(each,with_color=0,display=display),op='a+')
            nvft.write_to_file(fn=liddfn,content='\n',op='a+')
    if(os.path.exists(didfn)):
        pass
    else:
        nvft.write_to_file(fn=didfn,content=json.dumps(dir_imagename_dict),op='w+')
    ldidfn = fn + 'dir_image.lines'
    if(os.path.exists(ldidfn)):
        pass
    else:
        nvft.write_to_file(fn=ldidfn,content=get_printed_str(dir_imagename_dict,with_color=0,display=display),op='w+')
    ###############
    print("==dir_image.dict and dir_image.lines gotted==")
    ##############
    thumb_dir_dict = {}
    dir_thumb_dict = {}
    for each in all_photos:
        if(each['type'] != None):
            imagename = each['img-name']
            dir = each['thumb-dir']
        else:
            imagename = None
            dir = None
        thumb_dir_dict[imagename] = dir
        dir_thumb_dict[dir] = imagename
    iddfn = fn + 'thumb_dir.dict'
    didfn = fn + 'dir_thumb.dict'
    if(os.path.exists(iddfn)):
        pass
    else:
        nvft.write_to_file(fn=iddfn,content=json.dumps(thumb_dir_dict),op='w+')
    liddfn = fn + 'thumb_dir.lines'
    if(os.path.exists(liddfn)):
        pass
    else:
        nvft.write_to_file(fn=liddfn,content='',op='w+')   
        for each in thumb_dir_dict:
            nvft.write_to_file(fn=liddfn,content=get_printed_str(each,with_color=0,display=display),op='a+')
            nvft.write_to_file(fn=liddfn,content='\n',op='a+')
    if(os.path.exists(didfn)):
        pass
    else:
        nvft.write_to_file(fn=didfn,content=json.dumps(dir_thumb_dict),op='w+')
    ldidfn = fn + 'dir_thumb.lines'
    if(os.path.exists(ldidfn)):
        pass
    else:
        nvft.write_to_file(fn=ldidfn,content=get_printed_str(dir_thumb_dict,with_color=0,display=display),op='w+')
    ###############
    print("===dir_thumb.lines and thumb_dir.dict gotted===")
    ###############
    print("begin download images")
    ###############
    for each in all_photos:
        if(each['type'] != None):
            imagename = each['img-name']
            img_dir = each['img-dir']
            img_url = each['img-url']
            thumb_dir = each['thumb-dir']
            thumb_url = each['thumbnail-url']
            
            if(os.path.exists(img_dir)):
                ####
                print(paint_str("pass_by_pic",single_color="red"))
                ####
                pass
            else:
                info_container['url'] = img_url
                info_container = nvsoli.walkon(info_container,records_container=records_container)
                info_container = nvsoli.auto_redireced(info_container,records_container)
                nvft.write_to_file(fn=img_dir,content=info_container['resp_body_bytes'],op='wb+')
                ####
                print("downloaded one pic")
                ####
            if(os.path.exists(thumb_dir)):
                ####
                print(paint_str("pass_by_thumb",single_color="red"))
                ####
                pass
            else:
                info_container['url'] = thumb_url
                info_container = nvsoli.walkon(info_container,records_container=records_container)
                info_container = nvsoli.auto_redireced(info_container,records_container)
                nvft.write_to_file(fn=thumb_dir,content=info_container['resp_body_bytes'],op='wb+')
                ####
                print("downloaded one thumb")
                ####
        else:
            print("---external pics not downloaded in this version,pass--")
            pass
    return((info_container,records_container))

#-country_code 
c_code = sys.argv[2]
#-cpresence 
cpresence = sys.argv[4]
#-vhabitat
vhabitat = sys.argv[6]

try:
    display = sys.argv[8]
except:
    display = 0
else:
    display = int(display)


info_container,records_container = fishbase_init()
root = get_etree_root(info_container)
country_island_dict = get_country_island_dict(root)
#cmdt = cmdline.cmdict(dict=country_island_dict)
info_container,records_container = get_country_infos(c_code,country_island_dict,info_container,records_container,cpresence=cpresence,vhabitat=vhabitat,display=display)

##cd ./WEBCRAWLER/
##python3 fishbase.us.country.py -country_code 458 -cpresence present -vhabitat saltwater

