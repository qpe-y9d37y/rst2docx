# RST2DOCX

RST2DOCX is a tool written in Python used to format reStructuredText documentation to MS Word docx files.

## File Tree

```
.
|-- LICENSE
|-- README.md
|-- ini
|   |-- img
|   |   |-- 488px-Snake-anatomy.svg.png
|   │   `-- EuroLuxemburgo.svg.png
|   |-- rst2docx.ini_OPENSRC
|   `-- tpl_rst2docx.docx
|-- tmp
|   |-- PYTHON-DOCX_Edition.docx
|   `-- PYTHON-DOCX_Edition.rst
`-- utils
    `-- rst2docx.py
```

* The `ini` directory contains the configuration files:
  - `img` directory contains the images used in the MS Word template.
  - `rst2docx.ini_OPENSRC` is the skeleton of a required configuration file.
  - `tpl_rst2docx.docx` is an example of MS Word template.
* The `tmp` directory contains a documentation about python-docx and some details about how to create a MS Word Template. This documentation is also used as an example of reStructuredText documentation and formatted DOCX file.
* The `utils` directory contains the script to format reStructuredText documentation to MS Word docx files.

## Configuration Files

### MS Word Template

The MS Word Template should be named `tpl_rst2docx.docx` and stored under `./ini/`.

To learn more about how to modify this template or create your own, check the `PYTHON-DOCX_Edition` documentation under `./tmp/`.

### Variables File

The configuration `rst2docx.ini` contains required variables for the utility `rst2docx.py`.

The file `./ini/rst2docx.ini_OPENSRC` is a skeleton of this file, copy it or rename it as `./ini/rst2docx.ini` and adapt it with your own values.

## Usage

```
usage: rst2docx.py [-h] [-s SRC]

Format documentation

optional arguments:
  -h, --help  show this help message and exit
  -s SRC      source file
```

The following configuration files are mandatory:

* `./ini/rst2docx.ini`
* `./ini/tpl_rst2docx.docx`

The formated DOCX file will be generated under `./tmp/`.

## Attribution

The images used in the MS Word template example are under the Creative Commons license:

* EuroLuxemburgo: Jlechuga86 [CC BY (https://creativecommons.org/licenses/by/3.0)]. Retrieved from: https://commons.wikimedia.org/wiki/File:EuroLuxemburgo.svg

* Snake-anatomy: Uwe Gille [CC BY-SA (http://creativecommons.org/licenses/by-sa/3.0/)]. Retrieved from: https://commons.wikimedia.org/wiki/File:Snake-anatomy.svg
