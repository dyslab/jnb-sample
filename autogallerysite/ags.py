'''
    This is a Python3 app which runs in venv mode.

    Prerequisite:
        Python 3.x
        Pillow
        Jinja2

    Purpose: Website generator, generate html pages for gallery folder automatically.

    Usage: python3 ags.py

    IMPORTANT NOTICE: 
        workpath: current working path.
        basepath: the file path where this file located in.
        more information shown by class method 'repr()'.
'''
import os, json, math
from pathlib import Path
from PIL import Image

class AutoGallerySite(object):
    '''
        Automatically generate html pages for gallery folder

        Prerequsite: 
            config.json     # Project configured file
            templates/      # Jinja2 template file, located in the folder as same as this file
    '''
    def __init__(self):
        '''
            Initialize class instance
        '''
        self._workPath = os.getcwd()
        self._basePath, self._baseName = os.path.split(__file__)
        self._templatePath = os.path.join(self._basePath, 'templates')
        self._getConfigJson()
        self._recentAction = None
        # Computed thumbnail image width and height by constant scale
        self._fixedImageScale = 1.3334    
        self._thumbImageSizeW = 200
        self._thumbImageSizeH = math.ceil(self._thumbImageSizeW * self._fixedImageScale)
        self._thumbImageName = 'pix.jpg'
        self._galleyHtmlName = 'galley.html'

    def __repr__(self):
        '''
            Display main variables of the class
        '''
        exp = 'CLASS: {}'.format(self.__class__)
        self.log(exp)
        exp = 'DICT : {}'.format(self.__dict__)
        self.log(exp)
        return str(self.__class__)

    def _getConfigJson(self):
        '''
            Read configuration from config.json
        '''
        jsonFilePath = os.path.join(self._workPath, 'config.json')
        self.log('Read Configured Json File : %s' % jsonFilePath)
        try:
            with open(jsonFilePath) as fjson:
                self._configJson = json.load(fjson)
                fjson.close()
            # 
            self._galleryPath = os.path.abspath(
                os.path.join(self._workPath, self._configJson['gallery_path'])
            )
            self.log('Gallery Source Path: %s' % self._galleryPath)
            self._outputHtmlPath = os.path.abspath(
                os.path.join(self._workPath, self._configJson['output_html_path'])
            )
            self.log('HTML Files Output Path: %s' % self._outputHtmlPath)
        except OSError as e:
            self.log('Error message: %s' % e.strerror, 'error')
            exit(e.errno)
    
    def _isImageFile(self, filepath):
        '''
            Whether the file which indicated by filepath is image file or not
        '''
        try:
            with Image.open(filepath) as im:
                return True
        except IOError as e:
            return False

    def _geneGalleyHtml(self, thumpath, srcpath):
        '''
            Generate gallery index html file to output folder
        '''
        sPath, sName = os.path.split(str(srcpath))
        dPath = os.path.join(thumpath, self._galleyHtmlName)
        self.log('TEST: gallery path [{}]'.format(sPath))
        self.log('TEST: html file path [{}]'.format(dPath))

    def _fixThumbnail(self, im):
        '''
            Generate thumbnail image with a constant scale
        '''
        iW = im.width / self._thumbImageSizeW
        iH = im.height / self._thumbImageSizeH
        resizeW = im.width
        resizeH = im.height
        if iW > iH:
            resizeW = math.ceil(im.width / iW * iH)
        else:
            resizeH = math.ceil(im.height / iH * iW)
        resizeImage = im.crop((
            0,                                              # left
            0,                                              # upper
            im.width - round((im.width - resizeW), 0),      # right
            im.height - round((im.height - resizeH), 0)     # lower
        ))
        resizeImage.thumbnail((self._thumbImageSizeW, self._thumbImageSizeH))
        return resizeImage

    def _geneThumb(self, filepath):
        '''
            Generate thumbnail image file to output folder
        '''
        # Get relative path based on _galleyPath
        fpath, fname = os.path.split(str(filepath.relative_to(self._galleryPath)))
        thumbPath = os.path.join(self._outputHtmlPath, fpath)
        # Thumbnailing action will be skipped if thumbPath equals to the actioned path previously
        if thumbPath != self._recentAction:
            try:
                # Ensure target path is exists
                if not os.path.exists(thumbPath):
                    os.makedirs(thumbPath, exist_ok=True)
                # Generate thumbnail
                thumbFile = os.path.join(thumbPath, self._thumbImageName)
                with Image.open(filepath).convert("RGB") as im:
                    im = self._fixThumbnail(im)
                    im.save(thumbFile, "JPEG", quality=90)
                self.log('Generated thumbnail image file [{}]'.format(
                    Path(thumbFile).relative_to(Path(self._outputHtmlPath).parent)
                    ), 'warning')
                # Generate html index page
                self._geneGalleyHtml(thumbPath, filepath)
                # Save this actioned path
                self._recentAction = thumbPath
            except IOError as e:
                self.log('Error message: %s' % e.strerror, 'error')
                pass


    def log(self, msg, *args):
        '''
            Print formatted string
        '''
        LOG_TYPE = ('DEFAULT', 'INFO', 'WARNING', 'DEBUG', 'ERROR')
        LOG_TYPE_COLOR = (None, 35, 33, 32, 31)
        textColorCode = None
        for arg in args:
            if arg.upper() in LOG_TYPE:
                textColorCode = LOG_TYPE_COLOR[LOG_TYPE.index(arg.upper())]
        if textColorCode is None:
            print('>>> %s' % msg)
        else:
            print('>>> \033[{}m {} \033[0m'.format(textColorCode, msg))

    def geneThumbAndHtml(self):
        '''
            Generate thumbnail image amd html files to output folder 
            by traversing gallery source folder recurtisly
        '''
        srcPaths = sorted(Path(ags._galleryPath).rglob("*"))
        for p in srcPaths:
            if p.is_file():
                isImage = self._isImageFile(p)
                self.log('File: [{}] Type: {}'.format(p.name, 
                    'Image' if isImage else 'non-Image'),
                    'debug')
                # thumbnailing a folder image to output folder
                if isImage:
                    self._geneThumb(p)
            elif p.is_dir():
                self.log('Directory: [{}]'.format(p.name), 'info')
            else:
                self.log('Unknown file or directory [{}]'.format(p.name), 'error')


ags = AutoGallerySite()
# repr(ags)
ags.geneThumbAndHtml()
