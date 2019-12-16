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
import os, json, math, re, datetime
from pathlib import Path
from PIL import Image
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound

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
        # Record last action info
        self._recentAction = None
        # Initlize inside variables, Computed thumbnail image width and height by constant scale
        self._galleryURL = ''
        self._fixedImageScale = 1.3334    
        self._thumbImageSizeW = 200
        self._thumbImageSizeH = math.ceil(self._thumbImageSizeW * self._fixedImageScale)
        self._thumbImageName = 'pix.jpg'
        self._galleryPageName = 'gallery.html'
        self._indexPageName = 'index.html'
        self._templateGalleryPage = os.path.join('default', self._galleryPageName)
        self._templateIndexPage = os.path.join('default', self._indexPageName)
        # Get configured info from config.json
        self._getConfigJson()
        # Setup Jinja2 environment
        self._templatePath = os.path.join(self._basePath, 'templates')
        self._setupJinja2Env()

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
        self._configJsonFile = os.path.join(self._workPath, 'config.json')
        self.log('Read Configured Json File:')
        self.log(self._configJsonFile, 'info')
        try:
            with open(self._configJsonFile) as fjson:
                self._configJson = json.load(fjson)
                fjson.close()

            # Required Parameter: gallery_path
            self._galleryPath = os.path.abspath(
                os.path.join(self._workPath, self._configJson['gallery_path'])
            )
            self.log('Gallery Source Path:')
            self.log(self._galleryPath, 'info')

            # Required Parameter: output_html_path
            self._outputHtmlPath = os.path.abspath(
                os.path.join(self._workPath, self._configJson['output_html_path'])
            )
            self.log('HTML Files Output Path:')
            self.log(self._outputHtmlPath, 'info')

            # Optional Parameter: gallery_url
            if 'gallery_url' in self._configJson:
                self._galleryURL = self._configJson['gallery_url']
            self.log('Gallery URL:')
            self.log(self._galleryURL, 'info')

            # Optional Parameter: template_gallery_page
            if 'template_gallery_page' in self._configJson:
                self._templateGalleryPage = self._configJson['template_gallery_page']
                tmpPath, self._galleryPageName = os.path.split(self._templateGalleryPage)

            # Optional Parameter: template_index_page
            if 'template_index_page' in self._configJson:
                self._templateIndexPage = self._configJson['template_index_page']
                tmpPath, self._indexPageName = os.path.split(self._templateIndexPage)

            # Optional Parameter: thumb_image_width
            if 'thumb_image_width' in self._configJson:
                try:
                    self._thumbImageSizeW = int(self._configJson['thumb_image_width'])
                except OSError:
                    pass

            # Optional Parameter: thumb_image_height
            if 'thumb_image_height' in self._configJson:
                try:
                    self._thumbImageSizeH = int(self._configJson['thumb_image_height'])
                except OSError:
                    pass
        except OSError as e:
            self.log('Error message: %s' % e.strerror, 'error')
            exit(e.errno)

    def _setupJinja2Env(self):
        '''
            Setup Jinja2 environment
        '''
        try:
            self._jinja2Env = Environment(
                loader=FileSystemLoader(self._templatePath),
                autoescape=select_autoescape(enabled_extensions=('html', 'htm'))
            )
            self.log('Jinja2 Environment Created.')
            self.listTemplates()
            self.log('Initializing Templates:')
            self._templateIndexObj = self._jinja2Env.get_template(
                self._templateIndexPage,
                globals = {
                    'title': '图库索引页'
                }
            )
            self.log('Template [%s] initialized OK.' % self._templateIndexPage, 'warning')
            self._templateGalleryObj = self._jinja2Env.get_template(
                self._templateGalleryPage,
                globals = {
                    'title': '图库页'
                }
            )
            self.log('Template [%s] initialized OK.' % self._templateGalleryPage, 'warning')
        except TemplateNotFound as e:
            self.log('Template [%s] not found. initialized FAIL.' % e.message, 'error')
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

    def _fixedPath(self, spath):
        '''
            Ensure the link or path ended without slash
        '''
        if len(spath) > 0:
            if spath[-1] == '/':
                return spath[0:-1]
        return spath


    def _getGalleryContext(self, srcpath, destpath):
        '''
            Get jinja2 template context parameters from gallery source folder
            for galley template page
        '''
        pSourceFolder = srcpath.parent
        pGalleryList = sorted(pSourceFolder.glob("*"))
        # Search all images filename in the target folder
        #   imgCount, imgListString, relativeImgPath, relativeIndexPagePath
        imgList = []
        for p in pGalleryList:
            if p.is_file():
                if self._isImageFile(p):
                    imgList.append(p.name)
        imgCount = len(imgList)
        imgListString = '['
        for img in imgList:
            imgListString += '"' + img + '"'
            if img != imgList[-1]:
                imgListString += ','
        imgListString += ']'
        imgSubPath = str(pSourceFolder.relative_to(self._galleryPath))
        tmpPath = str(destpath.relative_to(Path(self._outputHtmlPath)))
        tmpPath = re.sub(r'[^/]+/', '../', tmpPath)
        tmpPath, tmpName = os.path.split(tmpPath)
        relativeGalleryURI = os.path.join(
            '..',
            tmpPath,
            str(Path(self._galleryPath).relative_to(
                Path(self._galleryPath).parent)
            )
        )
        relativeIndexPagePath = os.path.join(
            tmpPath,
            self._indexPageName
        )
        return {
            'imgBaseUrl': self._fixedPath(self._galleryURL),
            'imgBaseUri': self._fixedPath(relativeGalleryURI),
            'imgPath': self._fixedPath(imgSubPath),
            'indexUrl': relativeIndexPagePath,
            'imgCount': imgCount,
            'imgList': imgListString,
            'genDatetime': datetime.date.today()
        }

    def _geneGalleryPage(self, thumpath, srcpath):
        '''
            Generate gallery html file to output folder
        '''
        sPath, sName = os.path.split(str(srcpath))
        dPath = os.path.join(thumpath, self._galleryPageName)
        try:
            gCtx = self._getGalleryContext(srcpath, Path(dPath))
            self._templateGalleryObj.stream(gCtx).dump(dPath)
            self.log('Generated html file [{}]'.format(
                Path(dPath).relative_to(Path(self._outputHtmlPath).parent)
            ), 'warning')
        except TemplateNotFound as e:
            self.log(e.strerror, 'error')
            pass

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

    def _geneGallery(self, filepath):
        '''
            Generate thumbnail image file and gallery
            html page to output folder
        '''
        # Get relative path based on _galleryPath
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
                self._geneGalleryPage(thumbPath, filepath)
                # Save this actioned path
                self._recentAction = thumbPath
            except IOError as e:
                self.log('Error message: %s' % e.strerror, 'error')
                pass

    def _getIndexContext(self):
        '''
            Get jinja2 template context parameters for 
            galley index template page
        '''
        pGalleryPageList = list(Path(self._outputHtmlPath).rglob(self._galleryPageName))
        galleryPageListString = '['
        for p in pGalleryPageList:
            galleryPageListString += '"' + str(p.relative_to(Path(self._outputHtmlPath))) + '"'
            if p != pGalleryPageList[-1]:
                galleryPageListString += ','
        galleryPageListString += ']'
        return {
            'galleryPage': self._galleryPageName,
            'galleryImage': self._thumbImageName,
            'galleryList': galleryPageListString,
            'genDatetime': datetime.date.today()
        }

    def _geneIndex(self):
        '''
            Generate gallery index html page to output folder
        '''
        dPath = os.path.join(self._outputHtmlPath, self._indexPageName)
        try:
            iCtx = self._getIndexContext()
            self._templateIndexObj.stream(iCtx).dump(dPath)
            self.log('Generated html file [{}]'.format(
                Path(dPath).relative_to(Path(self._outputHtmlPath).parent)
            ), 'warning')
        except TemplateNotFound as e:
            self.log(e.strerror, 'error')
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

    def listTemplates(self):
        '''
            List all available templates
        '''
        if self._jinja2Env is not None:
            self.log('Available Templates:')
            for t in self._jinja2Env.list_templates():
                self.log(t, 'info')
    
    def listVariables(self):
        '''
            List main variables of the instance
        '''
        self.log('Configured json file:')
        self.log('<self._configJsonFile = "{}",\tConfigured json file>'.format(
            self._configJsonFile), 'warning')
        self.log('Inside variables:')
        self.log('<self._galleryPath = "{}",\tGallery source path>'.format(
            self._galleryPath), 'info')
        self.log('<self._outputHtmlPath = "{}",\tHtml and Thumbnail image files output folder path>'.format(
            self._outputHtmlPath), 'info')
        self.log('<self._galleryURL = "{}",\tGallery URL on Internet>'.format(
            self._galleryURL), 'info')
        self.log('<self._thumbImageSizeW = "{}",\tThumbnail image maximum width>'.format(
            self._thumbImageSizeW), 'info')
        self.log('<self._thumbImageSizeH = "{}",\tThumbnail image maximum height>'.format(
            self._thumbImageSizeH), 'info')
        self.log('<self._thumbImageName = "{}",\tThumbnail image output filename>'.format(
            self._thumbImageName), 'info')
        self.log('<self._galleryPageName = "{}",\tGallery html page output filename>'.format(
            self._galleryPageName), 'info')
        self.log('<self._indexPageName = "{}",\tGallery Index html page output filename>'.format(
            self._indexPageName), 'info')
        self.log('<self._templateGalleryPage = "{}",\tInitialized template for Gallery html pages>'.format(
            self._templateGalleryPage), 'info')
        self.log('<self._templateIndexPage = "{}",\tInitialized template for Gallery Index html page>'.format(
            self._templateIndexPage), 'info')
    
    def geneGalleryAndIndex(self):
        '''
            Generate thumbnail image amd html files to output folder 
            by traversing gallery source folder recurtisly
        '''
        srcPaths = sorted(Path(ags._galleryPath).rglob("*"))
        for p in srcPaths:
            if p.is_file():
                isImage = self._isImageFile(p)
                if isImage:
                    self.log('File: [{}] Type: {}'.format(p.name, 
                        'Image' if isImage else 'non-Image'),
                        'debug')
                    # thumbnailing a folder image and generate gallery 
                    # html page to output folder
                    self._geneGallery(p)
            elif p.is_dir():
                self.log('Directory: [{}]'.format(p.name), 'info')
            else:
                self.log('Unknown file or directory [{}]'.format(p.name), 'error')
        # Generate gallery index html page to output folder
        self._geneIndex()

# Main process
ags = AutoGallerySite()
# repr(ags)
ags.geneGalleryAndIndex()
ags.listVariables()
