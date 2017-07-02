

import xml.etree.cElementTree as ET
from collections import defaultdict

FULL_DATASET = 'amman_jordan.osm'
SAMPLE_DATASET = 'amman_jordan_sample.osm'

# Creating the sample file for initial auditing and validation purposes. 

k = 50 # Parameter: take every k-th top level element

def get_element(filename, tags = ('node', 'way')):
    context = iter(ET.iterparse(filename, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

with open(SAMPLE_DATASET, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n') # xml declaration
    output.write('<response>\n') # this is our root element (opening tag for the whole document)
    # Write every kth element
    for i, element in enumerate(get_element(FULL_DATASET)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding='utf-8'))
    output.write('</response>') # closing tag for the whole document


