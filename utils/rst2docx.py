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
from docx.shared import Inches

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
bullet_symbol = ["*","-","+"]
header_symbol = []
admonition_drctves = ["ATTENTION","CAUTION","DANGER","ERROR","HINT","IMPORTANT","NOTE","TIP","WARNING","ADMONITION"]
attention_drctves = ["ATTENTION","CAUTION","WARNING"]
danger_drctves = ["DANGER","ERROR"]
hint_drctves = ["HINT","IMPORTANT","TIP"]
note_drctves = ["NOTE","ADMONITION"]
separator = " "

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               FUNCTIONS                              #
#                                                                      #

# Function to print error when title not found.
def title_notfound():
    print("error: not title found in " + os.path.basename(src))
    print("see https://docutils.readthedocs.io/en/sphinx-docs/user/rst/quickstart.html#document-title-subtitle for more details")
    sys.exit(1)

# Function to apply text inside paragraph
def txt_style(p, split_prgrph):
    word_tag = "none"
    for word in split_prgrph:
        if word == split_prgrph[-1] and word.endswith("::"):
            word = word[:-1]
        if word_tag == "none":
            if word.startswith("*"):
                if word.startswith("**"):
                    if word.endswith("**"):
                        p.add_run(word[:-2][2:] + " ").bold = True
                    else:
                        word_tag = "bold"
                        p.add_run(word[2:] + " ").bold = True
                else:
                    if word.endswith("*"):
                        p.add_run(word[:-1][1:] + " ").italic = True
                    else:
                        word_tag = "italics"
                        p.add_run(word[1:] + " ").italic = True
#            elif word.startswith("``"):
#                if word.endswith("``"):
#                    ...
#                else:
#                    word_tag = "code"
#                    ...
            else:
                p.add_run(word + " ")
        elif word_tag == "bold":
            if word.endswith("**"):
                word_tag = "none"
                p.add_run(word[:-2] + " ").bold = True
            else:
                p.add_run(word + " ").bold = True
        elif word_tag == "italics":
            if word.endswith("*"):
                word_tag = "none"
                p.add_run(word[:-1] + " ").italic = True
            else:
                p.add_run(word + " ").italic = True
#        elif word_tab == "code":
#            if word.endswith("``"):
#                word_tag = "none"
#                ...
#            else:
#                ...

# Function to write a paragraph from RST.
def write_prgrph():
    file_tmp.close()
    with open(file_tmpprgrph, "r") as tmp_prgrph:
        prgrph = tmp_prgrph.read()
        with open(file_tmpprgrphold, "r") as tmp_prgrphold:
            prgrph_old = tmp_prgrphold.read()
            if prgrph != prgrph_old:
                # Headers.
                lines = prgrph.split('\n')
                lines.remove('')
                if len(lines) == 2 and re.match('^[=\-`:\'"~^_*+#<>]+$', lines[1]):
                    if lines[1][0] not in header_symbol:
                        header_symbol.append(lines[1][0])
                    header_lvl = header_symbol.index(lines[1][0]) + 1
                    document.add_paragraph(lines[0], 'Header_' + str(header_lvl))
                # Code blocks.
                elif prgrph_old.rstrip('\n')[-2:] == "::":
                    for line in lines:
                        document.add_paragraph(line.strip(), 'Code')
                # Python code blocks.
                elif prgrph.startswith(">>> "):
                    document.add_paragraph(prgrph.rstrip(), 'Code')
                # Bulleted lists.
                elif lines[0].strip()[0] in bullet_symbol and lines[0].strip()[1] == " ":
                    lead_space = len(lines[0]) - len(lines[0].strip())
                    bullet_lvl = int(lead_space / 2) + 1
                    document.add_paragraph(separator.join(lines)[2:], 'Bullet_' + str(bullet_lvl))
                # Enumerated lists.
                # Admonitions.
                elif lines[0].split()[0] == ".." and lines[0].split()[1][:-2] in admonition_drctves:
                    if lines[0].split()[1][:-2] in attention_drctves:
                        p = document.add_paragraph(lines[0].split()[1][:-2] + "\n", 'ATTENTION')
                        split_prgrph = prgrph.split()[2:]
                        txt_style(p, split_prgrph)
                    elif lines[0].split()[1][:-2] in danger_drctves:
                        p = document.add_paragraph(lines[0].split()[1][:-2] + "\n", 'DANGER')
                        split_prgrph = prgrph.split()[2:]
                        txt_style(p, split_prgrph)
                    elif lines[0].split()[1][:-2] in hint_drctves:
                        p = document.add_paragraph(lines[0].split()[1][:-2] + "\n", 'HINT')
                        split_prgrph = prgrph.split()[2:]
                        txt_style(p, split_prgrph)
                    elif lines[0].split()[1][:-2] in note_drctves:
                        p = document.add_paragraph(lines[0].split()[1][:-2] + "\n", 'NOTE')
                        split_prgrph = prgrph.split()[2:]
                        txt_style(p, split_prgrph)
                # Tables.
                # Sources.
                elif lines[0].startswith(".. ["):
                    table = document.add_table(1, 2)
                    table.cell(0, 0).text = prgrph.split()[1]
                    table.cell(0, 0).width = Inches(0.5)
                    table.cell(0, 1).text = separator.join(prgrph.split()[2:])
                    table.cell(0, 1).width = Inches(5.6)
                # Markup for code.
                elif lines[0] == "::" and len(lines) == 1:
                    pass
                # Normal text.
                else:
                    p = document.add_paragraph("", 'Normal')
                    split_prgrph = prgrph.split()
                    txt_style(p, split_prgrph)
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
