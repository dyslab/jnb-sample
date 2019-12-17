'''
    This is a Python3 app which runs in venv mode.

    Prerequisite:
        Python 3.x
        Pillow
        Jinja2

    Purpose: Website generator, generate html pages for gallery folder automatically.

    Usage: python3 agsm.py
'''
from ags import AGSM

app = AGSM()
app.geneGalleryAndIndex()
# repr(app)
# app.initConfigJsonAndTemplate()
# app.listVariables()
