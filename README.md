# jnb-sample: A Miscellany Of Jupyter Notebook Learning 🔊

[![Jupyter notebook v7](./assets/jupyter-notebook-v7.svg)](https://jupyter.org/) &nbsp;&nbsp;[![My Stackshare](./assets/stackshare-dyslab.svg)](https://stackshare.io/dyslab) &nbsp;&nbsp;[![.github/workflows/fetch-bing-wallpaper.yml](https://github.com/dyslab/jnb-sample/actions/workflows/fetch-bing-wallpaper.yml/badge.svg)](https://github.com/dyslab/jnb-sample/actions/workflows/fetch-bing-wallpaper.yml)

## Prerequisites

1. Python venv environment (v3.7 or above)

2. Jupyter Notebook v7

## Installation(venv mode)

```bash
# Create virtual environment
python3 -m venv venv

# Activate venv mode in current folder
. venv/bin/activate       # On Linux / macOS
# .\venv\Scripts\Activate.ps1   # On Windows (Powershell)
# .\venv\Scripts\activate.bat   # On Windows (cmd)

# Install packages for this project in venv mode
# For Windows: Install Microsoft C++ Build Tools in advance.
#   Ref: https://visualstudio.microsoft.com/visual-cpp-build-tools/
pip install -r requirements.txt

# BTW: Exporting `requirements.txt` by CLI `pip freeze > requirements.txt`
```

## Launch jupyter notebook with venv mode

```bash
# Launch notebook with venv mode in current (working) folder.
jupyter notebook          # Command prompt added a prefix '(venv)'
```

***Project history***

· Last modified date: 15 Dec 2024

· Project creation date: 28 May 2019
