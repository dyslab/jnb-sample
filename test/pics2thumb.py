'''
    This is a Python3 app.

    Usage: python3 pics2thumb.py [src] [dest]

    Run command line 'python3 pics2thumb.py -h' for more information about usage.

    IMPORTANT NOTICE: 
        Dependency library 'Pillow' is needed. 
        Run command line 'pip install Pillow' to install it, as well as
        virtual environment (venv) is recommended.
'''
from pathlib import Path, PurePath
import argparse
from PIL import Image

# Thumbnailing pictures from sPath(Source Path) to dPath(Destination Path)
def thumbPics(sPath, dPath):

    # Get relative path by ignoring exception
    def _getRelativePath(_path):
        try:
            _relativePath = _path.relative_to(Path.cwd())
        except ValueError:
            return _path
        else:
            return _relativePath

    # Thumbnailing a picture with Pillow PIL
    def _thumbPic(_sFilePath, _sBasePath, _dTargetPath, counter):
        if str(_sFilePath).find(str(_dTargetPath)) != 0:
            counter += 1
            sourcePic = _sFilePath
            targetPic = _dTargetPath / _sFilePath.relative_to(_sBasePath)
            im = Image.open(sourcePic).convert("RGB")
            originSize = im.size
            thumbnail_size = (200, 200) # Thumbnail size.
            im.thumbnail(thumbnail_size)
            if not targetPic.parent.exists(): 
                Path.mkdir(targetPic.parent, parents=True, exist_ok=True)
            im.save(targetPic, 'JPEG', quality=90)
            print('\t#{}: {} -> {} OK!'.format(
                counter,
                _getRelativePath(sourcePic), 
                _getRelativePath(targetPic)
            ))
            print('\t\t{} -> {}'.format(originSize, im.size))

        return counter

    p = Path(sPath)
    # Manipulate pictures by extension format '.jpg'/'.jpeg'/'.png'. (Case Sensitive)
    print('Thumbnailing pictures...\nFrom: {} \nTo: {}'.format(sPath, dPath))
    counter = 0
    for x in p.rglob('*.jpg'):
        counter = _thumbPic(x, sPath, dPath, counter)
    for x in p.rglob('*.jpeg'):
        counter = _thumbPic(x, sPath, dPath, counter)
    for x in p.rglob('*.png'):
        counter = _thumbPic(x, sPath, dPath, counter)
    if counter == 0:
        print('No picture found.')

# --------------------------------------------------------------------------
# Main process Separator
# --------------------------------------------------------------------------
parser = argparse.ArgumentParser(description='Thumbnailing pictures for specific folder and its subfolders.')
parser.add_argument('src', type=str, nargs='?', help='Pathname of source folder. default to [working path]')
parser.add_argument('dest', type=str, nargs='?', help='Pathname of destination folder. default to [working path]/_thumnbs_/')
args = parser.parse_args()

# Default values.
if args.src is not None:
    try:
        sPath = Path(args.src).resolve()
    except OSError as e:
        print(e)
        exit()
else:
    sPath = Path.cwd()

if args.dest is not None:
    dPath = PurePath(args.dest)
    if not dPath.is_absolute():
        dPath = Path.cwd() / dPath
else:
    dPath = Path.cwd() / '_thumbs_'

try:
    thumbPics(sPath, dPath)
except OSError as e:
    print(e)

