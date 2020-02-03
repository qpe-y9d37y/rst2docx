#!/bin/bash

# For debugging purpose.
# set -x

########################################################################
# Bash                                                   Quentin Petit #
# January 2020                                 <petit.quent@gmail.com> #
#                                                                      #
#                                                                      #
#                                                                      #
#                              install.sh                              #
#                                                                      #
#                                                                      #
#                                                                      #
# Current version: 0.2                                                 #
# Status: Development in progress                                      #
#                                                                      #
# This script purpose it to create the file tree to use the different  #
# tools for NIR and install the required dependencies.                 #
#                                                                      #
#                                                                      #
#                                                                      #
# Version history:                                                     #
# +----------+------------+------+-----------------------------------+ #
# |   Date   |   Author   | Vers | Comment                           | #
# +----------+------------+------+-----------------------------------+ #
# | 20200128 | Quentin P. | 0.1  | Starting development              | #
# +----------+------------+------+-----------------------------------+ #
# | 20200203 | Quentin P. | 0.2  | Python pkg + install dir          | #
# +----------+------------+------+-----------------------------------+ #
#                                                                      #
########################################################################

#                                                                      #
#                               FUNCTIONS                              #
#                                                                      #

# Function to print the usage.
function usage {
  echo "usage: install.sh [-h]

install the dependencies and create the file tree for NIR

arguments:
  -h, --help      show this help message and exit
  "
}

# Function to ask if user wants to continue when error
function shouldweproceed {
  ANSWER=""
  echo "Do you want to continue? [y/N] "
  read ANSWER
  case ${ANSWER} in
    [yY][eE][sS]|[yY] ) ;;
    * ) echo "bye" && exit 1 ;;
  esac
}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               VARIABLES                              #
#                                                                      #

# Files and directories
DIR_GIT=$(dirname $(readlink -f $0))
DIR_NIR="/home/tools/nir"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                                                      #
#                               BEGINNING                              #
#                                                                      #

# Check if help is requested.
if [[ ${1} == "-h" ]] || [[ ${1} == "--help" ]]; then
  usage && exit 0
fi

# Check prerequisites
if [[ ! $(python3 --version) ]]; then
  echo "error: python3 is required, bye"
  exit 1
fi
if [[ ! $(pip3 --version) ]]; then
  echo "error: pip3 is required, bye"
  exit 1
fi

# Installing required pyton3 packages
pip3 install --upgrade pip setuptools
if [[ $? != "0" ]]; then
  echo "warning: something's wrong with the update of pip/setuptools."
  shouldweproceed
fi
pip3 install python-docx
if [[ $? != "0" ]]; then
  echo "warning: something's wrong with the installation of python-docx"
  shouldweproceed
fi

# Ask for installation directory
echo "Installation directory: [${DIR_NIR}] "
read CHOSEN_DIR

# Set installation directory
if [[ ${CHOSEN_DIR} != "" ]]; then
  DIR_NIR=${CHOSEN_DIR}
fi

# Create file tree
mkdir -p ${DIR_NIR}/tmp
mkdir -p ${HOME}/.vim/{ftdetect,syntax}

# Copy NIR utils and dependancies
for directory in utils ini; do
  cp -r ${DIR_GIT}/${directory} ${DIR_NIR}/
done

# Copy vim configuration
cp ${DIR_GIT}/vim/ftdetect-nir.vim ${HOME}/.vim/ftdetect/nir.vim
cp ${DIR_GIT}/vim/syntax-nir.vim ${HOME}/.vim/syntax/nir.vim

# Set correct permissions
chmod 755 ${DIR_NIR}/{tmp,utils,ini,tmplt}
chmod 644 ${DIR_NIR}/{ini,tmplt}/*
chmod 755 ${DIR_NIR}/utils/*
chmod -R 644 ${HOME}/.vim

# Check if .vimrc exists
if [[ -e ${HOME}/.vimrc ]]; then
  if [[ ! $(grep "FileType nir" ${HOME}/.vimrc) ]]; then
    echo -e "\" Settings for nir files\nau FileType nir setlocal tw=72 cuc et ai" >> ${HOME}/.vimrc
  fi 
else
  cp ${DIR_GIT}/vim/vimrc ${HOME}/
fi

#                                  END                                 #
#                                                                      #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
