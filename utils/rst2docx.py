#!/usr/bin/env python3

########################################################################
# Python 3                                               Quentin Petit #
# February 2020                                <petit.quent@gmail.com> #
#                                                                      #
#                             rst2docx.py                              #
#                                                                      #
# Current version: 0.1.0                                               #
# Status: Work in progress                                             #
#                                                                      #
# This script purpose it to format reStructuredText notes to MS docx   #
# file.                                                                #
#                                                                      #
# Version history:                                                     #
# +----------+---------+---------------------------------------------+ #
# |   Date   | Version | Comment                                     | #
# +----------+---------+---------------------------------------------+ #
# | 20200207 | 0.1.0   | First development                           | #
# +----------+---------+---------------------------------------------+ #
#                                                                      #
# The prerequisites to use this script are:                            #
#                                                                      #
# o  The Python package python-docx should be installed                #
#                                                                      #
########################################################################

#                                                                      #
#                              LIBRAIRIES                              #
#                                                                      #

import argparse
import os
import re
import shutil
import sys
from docx import Document

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               VARIABLES                              #
#                                                                      #

# Files and directories.
dir_current = os.path.abspath(os.path.dirname(sys.argv[0]))
dir_root = dir_current.rsplit('/', 1)[0]
dir_ini = dir_root + "/ini/"
dir_tmp = dir_root + "/tmp/"
docx_template = dir_ini + "tpl_rst2docx.docx"
file_tmpprgrph = dir_tmp + "tmp_paragraph"
file_tmpprgrphold = dir_tmp + "tmp_paragraph_previous"

#
nonalphanum = ["=","-","`",":","'","\"","~","^","_","*","+","#","<",">"]
header_symbol = []

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               FUNCTIONS                              #
#                                                                      #

# Function to print error when title not found.
def title_notfound():
    print("error: not title found in " + os.path.basename(src))
    print("see https://docutils.readthedocs.io/en/sphinx-docs/user/rst/quickstart.html#document-title-subtitle for more details")
    sys.exit(1)

# Function to write a paragraph from RST.
def write_prgrph():
    file_tmp.close()
    with open(file_tmpprgrph, "r") as tmp_prgrph:
        prgrph = tmp_prgrph.read()
        with open(file_tmpprgrphold, "r") as tmp_prgrphold:
            prgrph_old = tmp_prgrphold.read()
            if prgrph != prgrph_old:
                # Check if prgrph is a header.
                lines = prgrph.split('\n')
                lines.remove('')
                if len(lines) == 2 and re.match('^[=\-`:\'"~^_*+#<>]+$', lines[1]):
                    if lines[1][0] not in header_symbol:
                        header_symbol.append(lines[1][0])
                    header_lvl = header_symbol.index(lines[1][0]) + 1
                    document.add_paragraph(lines[0], 'Header_' + str(header_lvl))
    shutil.copyfile(file_tmpprgrph, file_tmpprgrphold)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               BEGINNING                              #
#                                                                      #

# Retrieve arguments.
parser = argparse.ArgumentParser(description='Format documentation')
parser.add_argument('-s', action="store", 
                    dest="src", help="source file")
args = parser.parse_args()

# Check if all arguments are set.
if len(sys.argv) > 1 and args.src == "":
    print("error: one or more argument is missing")
    parser.print_help()
    sys.exit(1)
# If no argument is set, interactive session.
elif len(sys.argv) <= 1:
    src = input("Source document: ")
else:
    src = args.src

# Print error and quit if file doesn't exist.
if not os.path.isfile(src):
    print("error: file " + src + " doesn't exist, bye")
    sys.exit(1)

# Create directories if not existing.
if not os.path.isdir(dir_tmp):
    os.makedirs(dir_tmp)

# Set output filename.
docx_output = dir_tmp + os.path.basename(src).replace('.rst', '.docx')

# Open docx template.
document = Document(docx_template)

# Retrieve and write title and subtitle.
with open(src, "r") as src_file:
    file_tmp = open(file_tmpprgrph, 'w')
    for line in src_file:
        if line == "\n":
            file_tmp.close()
            count = 0
            with open(file_tmpprgrph, 'r') as tmp_prgrph:
                for line in tmp_prgrph:
                    count += 1
            with open(file_tmpprgrph, 'r') as tmp_prgrph:
                if count == 3:
                    count = 0
                    for line in tmp_prgrph:
                        count += 1
                        if (count % 2) != 0 and line[0] not in nonalphanum:
                            title_notfound()
                        else:
                            title = re.sub(r"^\s+", "", line.rstrip())
                            subtitle = ""
                            document.add_paragraph(title, 'Cover_Title')
                elif count == 6:
                    count = 0
                    for line in tmp_prgrph:
                        count += 1
                        if str(count) in ["1","3","4","6"] and line[0] not in nonalphanum:
                            title_notfound()
                        elif str(count) == "2":
                            title = re.sub(r"^\s+", "", line.rstrip())
                            document.add_paragraph(title, 'Cover_Title')
                        elif count == 5:
                            subtitle = re.sub(r"^\s+", "", line.rstrip())
                            document.add_paragraph(subtitle, 'Cover_Subtitle')
                else:
                    title_notfound()
            shutil.copyfile(file_tmpprgrph, file_tmpprgrphold)
            break
        else:
            file_tmp.write(line)

# Insert page break.
document.add_page_break()

# Insert disclaimer.

# Insert writing conventions.

# Insert content.
with open(src, "r") as src_file:
    file_tmp = open(file_tmpprgrph, 'w')
    for line in src_file:
        if line == "\n":
            write_prgrph()
            file_tmp = open(file_tmpprgrph, 'w')
        else:
            file_tmp.write(line)
write_prgrph()

# Insert authors details.

# Save document.
document.save(docx_output)

#                                                                      #
#                                  END                                 #
#                                                                      #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
