<!-- TOC -->
* [OpenStudioLandscapesUtil-ReadmeGenerator](#openstudiolandscapesutil-readmegenerator)
  * [Requirements](#requirements)
    * [venv](#venv)
  * [Installation](#installation)
  * [Usage](#usage)
<!-- TOC -->

---

# OpenStudioLandscapesUtil-ReadmeGenerator

The `generate-readme` CLI dynamically creates `README.md`
files for an [OpenStudioLandscapes](https://github.com/michimussato/OpenStudioLandscapes) 
Feature.

This facilitates maintenance of `README.md` files
across multiple OpenStudioLandscapes Feature repositories.

## Requirements

- `python3.11`

### venv

```shell
python3 -m venv .venv
source .venv/bin/activate
```

## Installation

`pip install git+https://github.com/michimussato/OpenStudioLandscapesUtil-ReadmeGenerator.git`

## Usage

```
$ generate-readme --help
usage: generate-readme [-h] [--version] [-v] [-vv] --versions VERSIONS [VERSIONS ...]

A tool to generate a README.md

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         set loglevel to INFO
  -vv, --very-verbose   set loglevel to DEBUG
  --versions VERSIONS [VERSIONS ...]
                        Python version(s) to use for testing. You can supply multiple versions (i.e. 3.11), separated by spaces.
```
