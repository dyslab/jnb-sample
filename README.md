# jnb-sample

Jupyter Notebook Learning Samples Project. 🔊 

[![StackShare](http://img.shields.io/badge/tech-stack-0690fa.svg?style=flat)](https://stackshare.io/dyslab/my-stack)

## The prerequisites of the project running:

1. Python venv environment (version 3.6 or above).

2. Jupyter Notebook. 

3.  Conda & BeakerX. (the environment for BeakerX app test)


---


## Installation Guide For Venv Mode:

1. Create the **working directory**. (named it as you wish)

2. Run the following command line in **working directory** to create a new Python 'venv' environment. 

    ```
    $ python3 -m venv venv
    ```

## App Running Steps: (Venv  Mode)

1. Jump into the **working directory**.

2. Run the following command lines.

    ```bash
    $ . venv/bin/activate
    (venv) $ jupyter notebook
    ```

    or using below shell script.

    ```bash
    $ ./nbstart
    ```
    *(note: run the command line **`chmod a+x ./nbstart`** before running above shell script)*

3. Installed modules via **pip**:

    - IPython

    - Jupyter

    - jupyter-contrib-nbextensions (note: command line `$ jupyter contrib nbextension install --user` enable notebook extensions)

    - Pandas (along with `numpy`)

    - xlrd

    - matplotlib

    - Pillow

    - pyecharts

    - ipyleaflet

    - autopep8

4. All packages list (venv mode): See [requirements.txt](requirements.txt)

    Then, you were able to install the prerequisite packages by CLI `pip install -U -r requirements.txt` in your virtual environment. (BTW: Exporting requirements.txt by CLI `pip freeze > requirements.txt`)


---


## Notice For BeakerX App Launching.

1. BeakerX is basing on conda environment . Check out [Conda](https://www.anaconda.com/distribution/) and [BeakerX ](http://beakerx.com/documentation) for more details about their installations.

    ```bash
    (base) $ beakerx
    ```

2. All BeakerX samples saved in the folder `./beakerx_samples/`.

3. Packages list (conda mode): See [pip_list_beakerx.txt](pip_list_beakerx.txt)

PS: It seems there's certain conflict existed in my jupyter/nbextensions configuration between my venv mode and conda mode, it's not a big problem though, ok to work.


---


Document Information:

- *Last modified on 27 Nov 2019.*

- *Created on 28 May 2019.*
