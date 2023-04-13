# Desc. - Creates cyber labs
# Requirements: https://docxtpl.readthedocs.io/en/latest/,
# https://computersciencehub.io/python/python-converting-docx-file-to-text-file/

# Helpful references:
# https://jinja.palletsprojects.com/en/3.0.x/api/

# Needed imports
import docx2txt
import jinja2
import re
import os
from docxtpl import DocxTemplate

# Define a dictionary containing all the Jinjia variables in the template (unused in template defaults to blank)
content = {
    "section": '',
    "term": '',
    "deliverable1": '',
    "deliverable2": '',
    "deliverable3": '',
    "deliverable4": '',
    "deliverable5": '',
    "deliverable6": '',
    "deliverable7": ''
}

# Load my cyber template
template = DocxTemplate('templates/cyber_lab.docx')

# Get input of path to lab, use docx2txt to process it and turn it into string, contain in 'open_lab'
open_lab = docx2txt.process(input('Please enter the path of the lab: '))

# Fill in section and term with input
content["section"] = (input('Please enter the class you are taking: '))
content["term"] = (input('Please enter the term of the class you are taking: '))

# Use re.findall to find all matches for "Deliverable \d[\.|:].*$" regex, r, from open_lab, with looking multi-line
# and ignoring case
all_deliverables = re.findall(r'^Deliverable \d[\.|:].*$', open_lab, re.MULTILINE | re.IGNORECASE)

count = 1
# For each thing in all deliverables, add it to the dict "content"
# and count from 1 (to indicate deliverable1,deliverable2, etc.)
for deliverable in all_deliverables:
    content['deliverable' + str(count)] = deliverable
    count += 1

doc_name = 'test'

# Render content in file, also render Jinjia enviro variables set in "enviroment"
template.render(content)

# Change directory to output file
os.chdir(".\output")

template.save(doc_name + ".docx")

input('PRESS ANY BUTTON TO EXIT...')
# Lab00 - Routing and Windows.docx

"""
Explanation of Jinjia behind the scenes:
Essentially, when rendering a dict, you are allowing the template to use
all of the keys within the dictionary. You call them by thinking in the context
of what would I print from the dictionary.

For example:
If I wanted to get the content in "deliverable1" I would print
print(content['deliverable1'])

And I would use the following in my template:
{{ deliverable1 }}

Essentially render is taking that variable (list, dictionary, etc) and applying it to the template
"""
