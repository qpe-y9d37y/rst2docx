#!/bin/bash

# For debugging purpose.
# set -x

########################################################################
# Bash                                                   Quentin Petit #
# Feburary 2020                                <petit.quent@gmail.com> #
#                                                                      #
#                            nir_profile.sh                            #
#                                                                      #
# Current version: 0.1.0                                               #
# Status: Work in progress                                             #
#                                                                      #
# This script purpose it to                                            #
#                                                                      #
# Version history:                                                     #
# +----------+---------+---------------------------------------------+ #
# |   Date   | Version | Comment                                     | #
# +----------+---------+---------------------------------------------+ #
# | 20200203 | 0.1.0   | First development                           | #
# +----------+---------+---------------------------------------------+ #
#                                                                      #
########################################################################

#                                                                      #
#                               VARIABLES                              #
#                                                                      #

# Files and directories.
DIR_CURRENT=$(dirname $(realpath $0))
DIR_ROOT=$(dirname ${DIR_CURRENT})
DIR_INI="${DIR_ROOT}/ini/"
FILE_VAR="var_nirutils.py"
FILE_TPLT="tpl_nir2docx.docx"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               FUNCTIONS                              #
#                                                                      #

# Function to print the usage.
function usage {
  echo "usage: $(basename $0) [-h] [PROFILE_NAME]

switch to a profile

arguments:
  -h, --help      show this help message and exit
  PROFILE_NAME    name of the profile to use
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

# Set profile variable.
PROFILE=$1

# Check if profile exists.
if [[ ! -e ${DIR_INI}${FILE_VAR}_${PROFILE} ]] || [[ ! -e ${DIR_INI}${FILE_TPLT}_${PROFILE} ]]; then
  echo "error: ${FILE_VAR}_${PROFILE} or ${FILE_TPLT}_${PROFILE} cannot be found, bye"
  usage && exit 1
fi

# Ask if FILE_VAR/FILE_TPLT should be saved.
if [[ -e ${DIR_INI}${FILE_VAR} ]]; then
  ANSWER=""
  echo "Do you want to save current ${FILE_VAR}? [y/N] "
  read ANSWER
  case ${ANSWER} in
    [yY][eE][sS]|[yY] ) cp -p ${DIR_INI}${FILE_VAR}{,$(date +%Y%m%d)};;
    * ) ;;
  esac
  rm ${DIR_INI}${FILE_VAR}
fi
if [[ -e ${DIR_INI}${FILE_TPLT} ]]; then
  ANSWER=""
  echo "Do you want to save current ${FILE_TPLT}? [y/N] "
  read ANSWER
  case ${ANSWER} in
    [yY][eE][sS]|[yY] ) cp -p ${DIR_INI}${FILE_TPLT}{,$(date +%Y%m%d)};;
    * ) ;;
  esac
  rm ${DIR_INI}${FILE_TPLT}
fi

# Set ${PROFILE} as default.
cp -p ${DIR_INI}${FILE_VAR}_${PROFILE} ${DIR_INI}${FILE_VAR}
cp -p ${DIR_INI}${FILE_TPLT}_${PROFILE} ${DIR_INI}${FILE_TPLT}

#                                  END                                 #
#                                                                      #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
