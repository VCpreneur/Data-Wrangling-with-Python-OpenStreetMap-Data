#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re


FULL_DATASET = 'amman_jordan.osm'
SAMPLE_DATASET = 'amman_jordan_sample.osm'

# Counting all tags in the full dataset 

def count_all_tags(filename):
    tags = defaultdict(int)
    tree = ET.parse(filename)
    root = tree.getroot()
    for element in root.iter():
        tags[element.tag] += 1
    return tags

all_tags = count_all_tags(FULL_DATASET)
pprint.pprint(all_tags)


# Counting primary tags in the full dataset

def count_highest_level_tags(filename):
    tags = defaultdict(int)
    tree = ET.parse(filename)
    root = tree.getroot()
    for element in root.getchildren():
        tags[element.tag] += 1
    return tags

highest_level_tags = count_highest_level_tags(FULL_DATASET)
pprint.pprint(highest_level_tags)


# Counting all tags and primary tags in the sample dataset 

all_tags = count_all_tags(SAMPLE_DATASET)
pprint.pprint(all_tags)

highest_level_tags = count_highest_level_tags(SAMPLE_DATASET)
pprint.pprint(highest_level_tags)


# Exploring naming trends in the full dataset

arabic = re.compile(ur'[ا-ي]|[١-٩]', re.UNICODE)
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+-/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        if lower.search(element.attrib['k']):
            keys['lower'] += 1
            #print "lower: " + element.attrib['k'] # printing the arrtibute for exploring purposes 
        elif lower_colon.search(element.attrib['k']):
            keys['lower_colon'] += 1
            #print "lower_colon: " + element.attrib['k'] # printing the arrtibute for exploring purposes
        elif problemchars.search(element.attrib['k']):
            keys['problemchars'] += 1
            print "problemchars: " + element.attrib['k'] # printing the arrtibute for exploring purposes
        elif arabic.search(element.attrib['k']):
            keys['arabic'] += 1
            #print "arabic: " + element.attrib['k'] # printing the arrtibute for exploring purposes
        else:
            keys['other'] += 1
            #print "other: " + element.attrib['k'] # printing the arrtibute for exploring purposes
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0, "arabic": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys

keys = process_map(FULL_DATASET)
pprint.pprint(keys)


# Counting Arabic tag values

arabic = re.compile(ur'[ا-ي]|[١-٩]', re.UNICODE) 

def value_type(element, values):
    if element.tag == "tag":
        #print element.attrib['v']
        if arabic.search(element.attrib['v']):
            values['arabic'] += 1
            #print "arabic: " + element.attrib['v'] # printing the arrtibute for exploring purposes 
        else:
            values['other'] += 1
            #print "other: " + element.attrib['v'] # printing the arrtibute for exploring purposes
    return values


def process_map(filename):
    values = {"arabic": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        values = value_type(element, values)

    return values


values = process_map(FULL_DATASET)
pprint.pprint(values)


# Counting unique users who contributed to the map's data: 

def get_user(element):
    return element.get('uid')

def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        user = get_user(element)
        if user is not None:
            users.add(user)

    return len(users)

print process_map(FULL_DATASET)




