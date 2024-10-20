# jnb-sample: A Miscellany Of Jupyter Notebook Learning 🔊

[![Jupyter notebook v7](./assets/jupyter-notebook-v7.svg)](https://jupyter.org/) &nbsp;&nbsp;[![My Stackshare](./assets/stackshare-dyslab.svg)](https://stackshare.io/dyslab)

## Prerequisites

1. Python venv environment (v3.7 or above)

2. Jupyter Notebook v7

## Installation(venv mode)

```bash
# Create virtual environment
python3 -m venv venv

# Activate venv mode in current folder
. venv/bin/activate

# Install packages for this project in venv mode
pip install -r requirements.txt

# BTW: Exporting `requirements.txt` by CLI `pip freeze > requirements.txt`
```

## Running app in venv mode

```bash
# Start notebook in venv mode under current (working) folder.
jupyter notebook # Command prompt added a prefix '(venv)'

# Or use shell script file below. Type `chmod +x ./nbstart` at first to make the file executable
./nbstart
```

***Project history***

· Last modified date: 20 Oct 2024

· Project creation date: 28 May 2019
