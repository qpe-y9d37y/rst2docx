#!/usr/bin/env bash

# For debugging purpose.
# set -x

########################################################################
# Bash                                                   Quentin Petit #
# August 2019                                  <petit.quent@gmail.com> #
#                                                                      #
#                            nir_browser.sh                            #
#                                                                      #
# Current version: 2.0.0                                               #
# Status: Work in progress                                             #
#                                                                      #
# This script purpose is to display UNIX documentation.                #
#                                                                      #
# Version history:                                                     #
# +----------+---------+---------------------------------------------+ #
# |   Date   | Version | Comment                                     | #
# +----------+---------+---------------------------------------------+ #
# | 20190827 | 0.1.0   | First development                           | #
# | 20190905 | 1.0.0   | First stable version                        | #
# | 20200204 | 2.0.0   | Redesign for NIR documentations             | #
# +----------+---------+---------------------------------------------+ #
#                                                                      #
# The prerequisites to use this script are:                            #
#                                                                      #
# o  The package dialog should be installed                            #
#                                                                      #
########################################################################

#                                                                      #
#                               VARIABLES                              #
#                                                                      #

# Files and directories.
DIR_CURRENT=$(dirname $(realpath $0))
DIR_ROOT=$(dirname ${DIR_CURRENT})
DIR_INI="${DIR_ROOT}/ini/"
DIR_TMP="${DIR_ROOT}/tmp/"
FILE_IN="${DIR_TMP}input.$$"
FILE_OUT="${DIR_TMP}output.$$"
FILE_SRC="${DIR_INI}src_nirbrowser.txt"
FILE_SUB="${DIR_TMP}sub.$$"
FILE_VAR="${DIR_INI}var_nirbrowser.txt"

# Environment.
IFS=$'\n'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               FUNCTIONS                              #
#                                                                      #

# Function to create the main menu.
function main_menu {

  # Set function variables.
  ROWS=$(echo "$(sort ${FILE_SRC} | awk -F';' '{print $1}' | uniq | wc -l) + 2" | bc)

  # Retrieve list of main topics.
  for HEAD1 in $(sort ${FILE_SRC} | awk -F';' '{print $1}' | uniq); do
    MAIN+=("${HEAD1}" "Help for ${HEAD1}")
  done

  # Print main menu.
  dialog --clear --backtitle "UNIX Help" --title "Main menu" \
    --menu "" 15 50 ${ROWS} \
    ${MAIN[@]} \
    Search "" \
    Exit "Exit to the shell" 2> ${FILE_IN}

  # Set chosen item.
  ITEM=$(<"${FILE_IN}")

  # Launch action depending of choice.
  case ${ITEM} in
#    Search) dialog --title "Search" --inputbox "Search:" 16 51 2> ${FILE_IN};;
    Search) search;;
    "" | Exit) clear; exit 0;;
    * ) sub_menu ${ITEM};;
  esac

}

# Function to create the sub menu.
function sub_menu {

  # Set function variables.
  HEAD1=${1}
  ROWS=$(echo "$(sort ${FILE_SRC} | grep ${HEAD1} | awk -F';' '{print $2}' | wc -l) + 1" | bc)

  # Retrieve list of sub topics.
  if [[ $(sort ${FILE_SRC} | grep ${HEAD1} | awk -F';' '{print $2}') == "" ]]; then
    doc_menu ${HEAD1}
  fi
  for HEAD2 in $(sort ${FILE_SRC} | grep ${HEAD1} | awk -F';' '{print $2}'); do
    SUB+=("${HEAD2}" "Help for ${HEAD2}")
  done

  # Print main menu.
  dialog --clear --backtitle "UNIX Help" --title "${HEAD1} menu" \
    --menu "" 15 50 ${ROWS} \
    ${SUB[@]} \
    Exit "Exit to the shell" 2> ${FILE_IN}

  # Set chosen item.
  ITEM=$(<"${FILE_IN}")

  # Launch action depending of choice.
  case ${ITEM} in
    "" | Exit) clear; exit 0;;
    * ) doc_menu ${ITEM};;
  esac

}

# Function to create the doc menu.
function doc_menu {
  
  # Set function variables.
  PART=${1}
  COUNTER=1

  # Retrieve list of available documentation.
  for file in $(ls -1 ${DIR_DOC}); do
    if [[ ${file} == "${PART}"* ]]; then
      FIELD=$(echo ${file} | awk -F'-' '{print $2}' | tr '_' ' ')
      echo "${COUNTER}|${FIELD}|${file}" >> ${FILE_SUB}
      DOCS+=("${COUNTER}" "${FIELD}")
      ((COUNTER++))
    fi
  done

  # Print dynamic menu with available doc.
  dialog --clear --backtitle "UNIX Help" --title "${PART}" \
    --menu "" 15 50 4 \
    ${DOCS[@]} 2> ${FILE_IN}

  # Set chosen item.
  ITEM=$(<"${FILE_IN}")

  # Print chosen doc.
  case ${ITEM} in
    [0-9]* ) FILE=${DIR_DOC}$(grep "^${ITEM}|" ${FILE_SUB} | awk -F'|' '{print $3}'); dialog --textbox ${FILE} 57 83;;
    * ) clear; exit 0;;
  esac

}

# Function to search in the documentation.
function search {

  # Set function variables.
  COUNTER=1
   
  # Print search box.
  dialog --title "Search" --inputbox "Search:" 16 51 2> ${FILE_IN}

  # Set searched item.
  ITEM=$(<"${FILE_IN}")

  for file in $(grep -li "${ITEM}" ${DIR_DOC}*); do
    echo "${COUNTER}|${file}" >> ${FILE_SUB}
    DOCS+=("${COUNTER}" "$(basename ${file})")
    ((COUNTER++))
  done

  # Print dynamic menu with available doc.
  dialog --clear --backtitle "UNIX Help" --title "Search results" \
    --menu "" 15 50 4 \
    ${DOCS[@]} 2> ${FILE_IN}

  # Set chosen item.
  ITEM=$(<"${FILE_IN}")

  # Print chosen doc.
  case ${ITEM} in
    [0-9]* ) FILE=$(grep "^${ITEM}|" ${FILE_SUB} | awk -F'|' '{print $2}'); dialog --textbox ${FILE} 57 83;;
    * ) clear; exit 0;;
  esac

}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               BEGINNING                              #
#                                                                      #

# Check if ${FILE_VAR} exists.
if [[ ! -e ${FILE_VAR} ]]; then
  echo "Where are your documentations? [${HOME}/doc/] "
  read ANSWER
  if [[ ${ANSWER} == "" ]]; then
    ANSWER="${HOME}/doc/"
  fi
  echo ${ANSWER} > ${FILE_VAR}
fi

# Set ${DIR_DOC}.
DIR_DOC=$(cat ${FILE_VAR})

# Launch menu.
main_menu

#                                  END                                 #
#                                                                      #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#