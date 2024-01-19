# jnb-sample: A Miscellany Of Jupyter Notebook Learning 🔊 

[![Powered by Jupyter notebook v6.5](./imgs/powered-by-notebook-v6.svg)](https://jupyter.org/) &nbsp;&nbsp;[![My Stackshare](./imgs/stackshare-dyslab.svg)](https://stackshare.io/dyslab)

## Prerequisites

1. Python3 venv environment (v3.6 or above)

2. Jupyter Notebook v6.4 or v6.5

3. Conda with BeakerX

## Venv mode creation

1. Create the **working directory**. (named it as you wish)

2. Run the following command line in **working directory** to create a new Python 'venv' environment. 

```
$ python3 -m venv venv
```

## Install packages list in venv mode

```bash
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

# Or use shell script file below. Type `chmod a+x ./nbstart` at first to make the file executable
./nbstart
```

## Main module list:

- Jupyter

- IPython

- jupyter-contrib-nbextensions

```bash
# Remember to make the extensions enable
jupyter contrib nbextension install --user
```

- Pandas (along with numpy)

- xlrd

- matplotlib

- Pillow

- pyecharts

- ipyleaflet

- autopep8

Check out [requirements.txt](requirements.txt) for more details.

## Notice For BeakerX App Launching.

1. BeakerX is basing on conda environment . Check out [Conda](https://www.anaconda.com/distribution/) and [BeakerX ](http://beakerx.com/documentation) for more details about their installations.

```bash
(base) $ beakerx
```

2. All BeakerX samples saved in the folder `./beakerx_samples/`.

3. Packages list (conda mode): See [pip_list_beakerx.txt](pip_list_beakerx.txt)

Note: It seems that certain conflicts existed in my jupyter / nbextensions configuration between venv mode and conda mode. It's not a big deal though, still fine to work.

---

__*Project history*__

*· Last modified date: 19 Jan 2024*

*· Project creation date: 28 May 2019*
