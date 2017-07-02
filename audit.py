#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re

FULL_DATASET = 'amman_jordan.osm'


# Auditing the full dataset for street names and city names in both Arabic and English languages 

arabic = re.compile(ur'[ا-ي]|[١-٩]', re.UNICODE) 
street_type_re_en = re.compile(r'\b\S+\.?$', re.IGNORECASE)
street_type_re_ar = re.compile(r'[^\s]+')

expected_en = ["Road", "Street", "Highway", "Autostrad"]
expected_ar = ["شارع" , "طريق"]

def audit_street_type_en(street_types_en, street_name):
    m = street_type_re_en.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected_en:
            street_types_en[street_type].add(street_name)

def audit_street_type_ar(street_types_ar, street_name):
    m = street_type_re_ar.search(street_name)
    if m:
        street_type = m.group()
        if street_type.encode('utf-8') not in expected_ar:
            street_types_ar[street_type].add(street_name)

def audit_city_name_en(city_names_en, city_name):
    if city_name != "Amman":
        city_names_en[city_name].add(city_name)

def audit_city_name_ar(city_names_ar, city_name):
    if city_name.encode('utf-8') != "عمان":
        city_names_ar[city_name].add(city_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")

def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types_en = defaultdict(set)
    street_types_ar = defaultdict(set)

    city_names_ar = defaultdict(set)
    city_names_en = defaultdict(set)
    
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city_name(tag):
                    #print tag.attrib['v']
                    a = arabic.search(tag.attrib['v'])
                    if a:
                        audit_city_name_ar(city_names_ar, tag.attrib['v'])
                    else:
                        audit_city_name_en(city_names_en, tag.attrib['v'])
                elif is_street_name(tag):
                    a = arabic.search(tag.attrib['v'])
                    if a:
                        audit_street_type_ar(street_types_ar, tag.attrib['v'])
                    else:
                        audit_street_type_en(street_types_en, tag.attrib['v'])
    osm_file.close()
    return street_types_en, street_types_ar, city_names_ar, city_names_en

st_types_e, st_types_a, city_names_a, city_names_e = audit(FULL_DATASET)

pprint.pprint(dict(st_types_e))
#pprint.pprint(dict(st_types_a))
for key, value in st_types_a.iteritems(): 
    print "Word: " + key
    for v in value:
        print "     Occurrence: " + v

pprint.pprint(dict(city_names_e))
#pprint.pprint(dict(city_names_a))
for key, value in city_names_a.iteritems(): 
    print "Word: " + key
    for v in value:
        print "     Occurrence: " + v
