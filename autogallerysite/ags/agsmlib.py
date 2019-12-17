'''
    This is a Python3 library app which runs in venv mode.

    Prerequisite:
        Inherited from AutoGallerySite in 'agslib.py'. See annotation in 'agalib.py'.

    Purpose: Gallery website generator, Automatically generating thumbnail images 
             and multi-page html files for gallery folder.

    Usage: Import and invoke as library

    Example codes:
        from ags import AGSM
        app = AGSM()
        app.geneGalleryAndIndex()

    NOTICE: 
        more information shown by class method 'repr()' and 'listVariables()'.
'''
from .agslib import AutoGallerySite
from pathlib import Path
import os, math, re, datetime

class AutoGallerySiteMultiplePages(AutoGallerySite):
    def __init__(self):
        '''
            Inherited and extended class method
        '''
        super().__init__()
        # AGSm custom variables
        self._configJsonName = 'mconfig.json'
        self._templatePathName = 'mtemplates'
        self._indexItemsPerPage = 24
        self._galleryItemsPerPage = 8

    def _getConfigJson(self):
        '''
            Inherited and extended class method
        '''
        super()._getConfigJson()
        # Optional Parameter: index_items_per_page
        if 'index_items_per_page' in self._configJson:
            try:
                self._indexItemsPerPage = int(self._configJson['index_items_per_page'])
            except OSError:
                pass
         # Optional Parameter: gallery_items_per_page
        if 'gallery_items_per_page' in self._configJson:
            try:
                self._galleryItemsPerPage = int(self._configJson['gallery_items_per_page'])
            except OSError:
                pass

    def listVariables(self):
        '''
            Inherited and extended class method
        '''
        super().listVariables()
        # List custom variables
        self._showVar('self._galleryItemsPerPage', 'Items per page for Gallery Page. Configured JSON: [gallery_items_per_page] Optional.')
        self._showVar('self._indexItemsPerPage', 'Items per page for Gallery Index Page. Configured JSON: [index_items_per_page] Optional.')

    def _getGalleryContext(self, srcpath, destpath):
        '''
            Override class method
        '''
        pSourceFolder = srcpath.parent
        pGalleryList = sorted(pSourceFolder.glob("*"))
        # Search all images filename in the target folder
        #   imgList, relativeImgPath, relativeIndexPagePath
        imgList = []
        for p in pGalleryList:
            if p.is_file():
                if self._isImageFile(p):
                    imgList.append(p.name)
        imgSubPath = str(pSourceFolder.relative_to(self._galleryPath))
        tmpPath = str(destpath.relative_to(Path(self._outputHtmlPath)))
        tmpPath = re.sub(r'[^/]+/', '../', tmpPath)
        tmpPath, tmpName = os.path.split(tmpPath)
        relativeGalleryURI = os.path.join(
            '../..',
            tmpPath,
            str(Path(self._galleryPath).relative_to(
                Path(self._galleryPath).parent)
            )
        )
        relativeIndexPagePath = os.path.join(
            '..',
            tmpPath,
            self._indexPageName
        )
        return {
            'imgBaseUrl': self._fixedPath(self._galleryURL),
            'imgBaseUri': self._fixedPath(relativeGalleryURI),
            'imgPath': self._fixedPath(imgSubPath),
            'indexUrl': relativeIndexPagePath,
            'imgCount': len(imgList),
            'imgList': imgList
        }

    def _calculateTotalPages(self, count, perpage):
        '''
            Calculate total pages
        '''
        return math.ceil(count / perpage)
    
    def _getPageList(self, allList, curpage, perpage):
        '''
            Get current page list from all
        '''
        startPos = (curpage - 1) * perpage  # include
        endPos = curpage * perpage          # exclude
        startPos = 0 if startPos < 0 else startPos
        endPos = len(allList) if endPos > len(allList) else endPos
        return allList[startPos:endPos]

    def _geneGalleryPage(self, destpath, srcpath):
        '''
            Override class method
        '''
        try:
            sPath, sName = os.path.split(str(srcpath))
            gCtx = self._getGalleryContext(srcpath, Path(destpath))
            totalPages = self._calculateTotalPages(gCtx['imgCount'], self._galleryItemsPerPage)
            gName, gExt = os.path.splitext(self._galleryPageName)
            for p in range(1, totalPages+1):
                suffixName = ('_%s' % p) if p > 1 else ''
                dName = '{}{}{}'.format(gName, suffixName, gExt)
                dPath = os.path.join(destpath, dName)
                pageItemList = self._getPageList(gCtx['imgList'], p, self._galleryItemsPerPage)
                self._templateGalleryObj.stream({
                    'imgBaseUrl': gCtx['imgBaseUrl'],
                    'imgBaseUri': gCtx['imgBaseUri'],
                    'imgPath': gCtx['imgPath'],
                    'indexUrl': gCtx['indexUrl'],
                    'pageName': gName,
                    'pageExt': gExt,
                    'currentPage': p,
                    'totalPages': totalPages,
                    'contentList': pageItemList,
                    'genDatetime': datetime.date.today()
                }).dump(dPath)
                self.log('Generated html file [{}]'.format(
                    Path(dPath).relative_to(Path(self._outputHtmlPath).parent)
                ), 'warning')
        except TemplateNotFound as e:
            self.log(e.strerror, 'error')
            pass

    def _getIndexContext(self):
        '''
            Override class method
        '''
        pGalleryPageList = list(Path(self._outputHtmlPath).rglob(self._galleryPageName))
        galleryList = []
        for p in pGalleryPageList:
            galleryList.append(str(p.relative_to(Path(self._outputHtmlPath))))
        return {
            'galleryCount': len(galleryList),
            'galleryList': galleryList
        }

    def _geneIndex(self):
        '''
            Override class method
        '''
        try:
            iCtx = self._getIndexContext()
            totalPages = self._calculateTotalPages(iCtx['galleryCount'], self._indexItemsPerPage)
            iName, iExt = os.path.splitext(self._indexPageName)
            for p in range(1, totalPages+1):
                suffixName = ('_%s' % p) if p > 1 else ''
                dName = '{}{}{}'.format(iName, suffixName, iExt)
                dPath = os.path.join(self._outputHtmlPath, dName)
                pageItemList = self._getPageList(iCtx['galleryList'], p, self._indexItemsPerPage)
                self._templateIndexObj.stream({
                    'galleryPage': self._galleryPageName,
                    'galleryImage': self._thumbImageName,
                    'pageName': iName,
                    'pageExt': iExt,
                    'currentPage': p,
                    'totalPages': totalPages,
                    'contentList': pageItemList,
                    'genDatetime': datetime.date.today()
                }).dump(dPath)
                self.log('Generated html file [{}]'.format(
                    Path(dPath).relative_to(Path(self._outputHtmlPath).parent)
                ), 'warning')
        except TemplateNotFound as e:
            self.log(e.strerror, 'error')
            pass
