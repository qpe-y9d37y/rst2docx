# NIR
NIR - IT documentation format

## Notice

Work in progress

## Files and directories

Here is the file tree of this repository:

```
.
|-- LICENSE
|-- README.md
|-- ini/
|   `-- var_nir2txt.py
|-- utils/
|   |-- nir2txt.py
|   `-- patina.sh
`-- vim/
    |-- ftdetect-nir.vim
    |-- syntax-nir.vim
    `-- vimrc
```

### Quick description

* The `ini` directory contains some initialization files for the scripts.
* The `utils` directory contains some scripts used with NIR.
  - `nir2txt.py` is used to convert NIR files to structured TXT documentation file.
  - `patina.sh` is used to help include elements into a NIR file.
* The `vim` directory contains configuration files to write NIR files on vim.
