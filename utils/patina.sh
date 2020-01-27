#!/bin/bash

# For debugging purpose.
# set -x

########################################################################
# Bash                                                   Quentin Petit #
# January 2020                                 <petit.quent@gmail.com> #
#                                                                      #
#                                                                      #
#                                                                      #
#                               patina.sh                              #
#                                                                      #
#                                                                      #
#                                                                      #
# Current version: 0.1                                                 #
# Status: Development in progress                                      #
#                                                                      #
# This script purpose it to                                            #
#                                                                      #
#                                                                      #
#                                                                      #
# Version history:                                                     #
# +----------+------------+------+-----------------------------------+ #
# |   Date   |   Author   | Vers | Comment                           | #
# +----------+------------+------+-----------------------------------+ #
# | 20200123 | Quentin P. | 0.1  | Starting development              | #
# +----------+------------+------+-----------------------------------+ #
#                                                                      #
########################################################################

#                                                                      #
#                               FUNCTIONS                              #
#                                                                      #

# Function to print the usage.
function usage {
  echo "usage: patina.sh [-h] [-i OPTION]

...

arguments:
  -h, --help      show this help message and exit
  -i, --insert    insert OPTION
  "
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               BEGINNING                              #
#                                                                      #

# Check if help is requested.
if [[ -z ${1} ]] || [[ ${1} == "-h" ]] || [[ ${1} == "--help" ]]; then
  usage && exit 0
fi

# Check if argument is correct.
if [[ ${1} != "-i" ]] && [[ ${1} != "--insert" ]]; then
  echo "error: \"${1}\" is not a recognized argument."
  usage && exit 1
fi

# Check if option is set.
if [[ -z ${2} ]]; then
  echo "error: option is not set"
  usage && exit 1
fi

# Print option.
case ${2} in
  "note")
    echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    echo "+ Note:                                                          +"
    echo "+   "
    ;;
  "warn")
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo "!! Note:                                                        !!"
    echo "!!   "
    ;;
  *)
    echo "error: \"${2}\" is not a recognized option."
    usage && exit 1
    ;;
esac

#                                  END                                 #
#                                                                      #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
