#!/usr/bin/env python3

########################################################################
# Python 3                                               Quentin Petit #
#                                              <petit.quent@gmail.com> #
#                                                        December 2019 #
#                                                                      #
#                                                                      #
#                                                                      #
#                              nir2txt.py                              #
#                                                                      #
#                                                                      #
#                                                                      #
# Current version: 1.2                                                 #
# Status: Work in progress                                             #
#                                                                      #
# This script purpose it to format NIR notes to documentation.         #
#                                                                      #
#                                                                      #
#                                                                      #
# Version history:                                                     #
# +----------+------------+------+-----------------------------------+ #
# |   Date   |   Author   | Vers | Comment                           | #
# +----------+------------+------+-----------------------------------+ #
# | 20191219 | Quentin P. | 0.1  | Starting development              | #
# +----------+------------+------+-----------------------------------+ #
# | 20191220 | Quentin P. | 1.0  | First stable version              | #
# +----------+------------+------+-----------------------------------+ #
# | 20191221 | Quentin P. | 1.1  | Light optimization                | #
# +----------+------------+------+-----------------------------------+ #
# | 20200127 | Quentin P. | 1.2  | Author and doc var are now in ini | #
# +----------+------------+------+-----------------------------------+ #
# | 20200131 | Quentin P. | 1.3  | Nb of empty lines /w disclaimer   | #
# +----------+------------+------+-----------------------------------+ #
#                                                                      #
########################################################################

#                                                                      #
#                              LIBRAIRIES                              #
#                                                                      #

import argparse
import datetime
import os
import shutil
import sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               VARIABLES                              #
#                                                                      #

# Files and directories
dir_current = os.path.abspath(os.path.dirname(sys.argv[0]))
dir_root = dir_current.rsplit('/', 1)[0]
dir_ini = dir_root + "/ini/"
dir_tmp = dir_root + "/tmp/"
toc = dir_tmp + "ops_format-ietf.toc"
tmp = dir_tmp + "ops_format-ietf.tmp"

# Date
date = datetime.datetime.now().strftime("%B %Y")

# Additional variables
page_nb = 2
sub_index = 1
found = ""

# Import all variables from file
sys.path.append(dir_ini)
from var_nirutils import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               FUNCTIONS                              #
#                                                                      #



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               BEGINNING                              #
#                                                                      #

# Retrieve arguments.
parser = argparse.ArgumentParser(description='Format documentation')
parser.add_argument('-s', action="store", 
                    dest="src", help="source file")
parser.add_argument('-T', action="store", dest="title", help="title")
parser.add_argument('-t', action="store",
                    dest="title_short", help="short title")
parser.add_argument('-p', action="store",
                    dest="project", help="project")
parser.add_argument('-c', action="store", dest="cust", help="customer")
parser.add_argument('-g', action="store", dest="team", help="team")
args = parser.parse_args()

# Check if all arguments are set.
if len(sys.argv) > 1 and \
   None in (args.src, args.title, args.title_short,
            args.project, args.cust, args.team):
    print("error: one or more argument is missing")
    parser.print_help()
    sys.exit(1)
# If no argument is set, interactive session.
elif len(sys.argv) <= 1:
    src = input("Source document: ")
    title = input("Document title: ")
    title_short = input("Short title: ")
    project = input("Project: ")
    cust = input("Customer: ")
    team = input("Team: ")
else:
    src = args.src
    title = args.title
    title_short = args.title_short
    project = args.project
    cust = args.cust
    team = args.team

# Print error and quit if file doesn't exist.
if not os.path.isfile(src):
    print("error: file " + src + " doesn't exist, bye")
    sys.exit(1)

# Set output filename
out = dir_tmp + os.path.basename(src).replace('.nir', '.txt')

# Create directories if not existing.
if not os.path.isdir(dir_tmp):
    os.makedirs(dir_tmp)
file_toc = open(toc, "w")

# Create output file.
file_out = open(out, "w")
file_out.write("\n" * 3)
file_out.write('{0:<36}{1:>36}'.format(cust, author_short) + "\n")
file_out.write('{0:<36}{1:>36}'.format(team, corp) + "\n")
file_out.write('{0:<36}{1:>36}'.format(doctype, date) + "\n")
file_out.write("\n" * 2 + '{:^72}'.format(args.title) + "\n")
file_out.write("\n" * 2 + "Notice" + "\n")
file_out.write(disclaimer + "\n")
file_out.write("\n" * (43 - disclaimer.count('\n')))
file_out.write('{0:<24}{1:^24}{2:>24}'.format(corp,
               doctype, "[Page 1]") + "\n")
file_out.write('{0:<24}{1:^24}{2:>24}'.format(project,
               title_short, date) + "\n")
file_out.write("\n" * 2 + "Table of Contents" + "\n\n")

# Populate TOC.
line_count = 6
index = 1
with open(src, "r") as src_file:
    for line in src_file:
        if line.startswith("."):
            if line.startswith(".."):
                file_out.write(line.replace('..  ',
                     '      ' + str(index - 1)
                     + '.' + str(sub_index) + '. '))
                sub_index += 1
            else:
                file_out.write(line.replace('.  ',
                    '   ' + str(index) + '. '))
                sub_index = 1
                index += 1
            line_count += 1
            if line_count == 55:
                file_out.write("\n\n")
                file_out.write('{0:<24}{1:^24}{2:>24}'.format(corp,
                           doctype,
                           "[Page " + str(page_nb) + "]") + "\n")
                file_out.write('{0:<24}{1:^24}{2:>24}'.format(project,
                           title_short, date) + "\n")
                file_out.write("\n\n")
                page_nb += 1
                line_count = 4

# Insert spacing after TOC.
if line_count < 43:
    file_out.write("\n" * 3)
    line_count = line_count + 3
else:
    empty_lines_nb = 57 - (line_count - 4)
    file_out.write("\n" * empty_lines_nb)
    file_out.write('{0:<24}{1:^24}{2:>24}'.format(corp,
               doctype, "[Page " + str(page_nb) + "]") + "\n")
    file_out.write('{0:<24}{1:^24}{2:>24}'.format(project,
               title_short, date) + "\n")
    file_out.write("\n\n")
    page_nb += 1
    line_count = 4

# Insert content.
index = 1
with open(src, "r") as src_file:
    for line in src_file:
        if line.startswith("."):
            if line.startswith(".."):
                line = line.replace('..  ',
                    str(index - 1) + '.' + str(sub_index) + '.  ')
                line_toc = "      " + line.rstrip().replace('  ', ' ')
                sub_index += 1
            else:
                line = line.replace('.  ', str(index) + '.  ')
                line_toc = "   " + line.rstrip().replace('  ', ' ')
                sub_index = 1
                index += 1
            linetoc_char_nb = len(line_toc)
            pagenb_char_nb = len(str(page_nb))
            dot_nb = 71 - linetoc_char_nb - pagenb_char_nb
            file_toc.write(line_toc + " " + "." * dot_nb + str(page_nb) + "\n")
        file_out.write(line)
        line_count += 1
        if line_count == 55:
            file_out.write("\n\n")
            file_out.write('{0:<24}{1:^24}{2:>24}'.format(corp,
                       doctype, "[Page " + str(page_nb) + "]") + "\n")
            file_out.write('{0:<24}{1:^24}{2:>24}'.format(project,
                       title_short, date) + "\n")
            file_out.write("\n\n")
            page_nb += 1
            line_count = 4

# Insert spacing after content.
if line_count < 43:
    file_out.write("\n" * 4)
    line_count = line_count + 4
else:
    empty_lines_nb = 57 - ((line_count))
    file_out.write("\n" * empty_lines_nb)
    file_out.write('{0:<24}{1:^24}{2:>24}'.format(corp,
               doctype, "[Page " + str(page_nb) + "]") + "\n")
    file_out.write('{0:<24}{1:^24}{2:>24}'.format(project,
               title_short, date) + "\n")
    file_out.write("\n\n")
    page_nb += 1
    line_count = 4

# Insert authors' addresses.
file_out.write("Authors' Addresses \n")
file_out.write("\n")
file_out.write("   " + fname + " " + lname + " (editor)\n")
file_out.write("   " + corp + "\n")
file_out.write("   " + corpad + "\n")
file_out.write("\n")
file_out.write("   EMail: " + email)
line_count = line_count + 7

# Insert spacing after authors' addresses.
empty_lines_nb = 57 - ((line_count) - 1)
file_out.write("\n" * empty_lines_nb)
file_out.write('{0:<24}{1:^24}{2:>24}'.format(corp,
           doctype, "[Page " + str(page_nb) + "]") + "\n")

# Replace TOC to insert page numbers.
file_tmp = open(tmp, 'w')
with open(out, 'r') as file_out:
    for line_out in file_out:
        line_out = line_out.rstrip()
        with open(toc, 'r') as file_toc:
            for line_toc in file_toc:
                if line_out:
                    if line_out in line_toc:
                        found = "yes"
                        break
                    else:
                        found = "no"
                else:
                    found = "no"
            if found == "yes":
                file_tmp.write(line_toc)
            else:
                file_tmp.write(line_out + "\n")

# Clean up.
os.remove(toc)
os.remove(out)
shutil.move(tmp, out)

#                                                                      #
#                                  END                                 #
#                                                                      #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
