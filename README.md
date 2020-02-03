# NIR
NIR - IT documentation format for UNIX/Linux system administrators

## Files and directories

Here is the file tree of this repository:

```
.
|-- ini/
|   |-- tpl_nir2docx.docx
|   |-- tpl_nir2docx.docx_OPENSRC
|   `-- var_nirutils.py_EMPTY
|-- tmp/
|   |-- PYTHON-DOCX_Edition.docx
|   |-- PYTHON-DOCX_Edition.nir
|   `-- PYTHON-DOCX_Edition.txt
|-- utils/
|   |-- nir2docx.py
|   |-- nir2txt.py
|   `-- patina.sh
|-- vim/
|   |-- ftdetect-nir.vim
|   |-- syntax-nir.vim
|   `-- vimrc
|-- LICENSE
|-- README.md
`-- install.sh
```

### Quick description

* The `ini` directory contains some initialization files for the scripts:
  - `tpl_nir2docx.docx` is the MS Word template that will be used with `nir2docx.py`, it can be a symbolic link of a copy of another one (in this case, it's a copy of `tpl_nir2docx.docx_OPENSRC`
  - `var_nirutils.py_EMPTY` is the structure of the variable file that will be used for both `nir2docx.py` and `nir2txt.py`. Once filled, you need to save it as `var_nirutils.py`.
* The `tmp` directory contains some examples of `.nir`, `.docx` and `.tmp` files.
* The `utils` directory contains some scripts used with NIR.
  - `nir2docx.py` is used to convert NIR files to MS Word DOCX files.
  - `nir2txt.py` is used to convert NIR files to structured TXT documentation files.
  - `patina.sh` is used to help you include elements into a NIR file.
* The `vim` directory contains configuration files to write NIR files on vim.
* `install.sh` is a script used to install the dependencies and copy the files where they should be!
