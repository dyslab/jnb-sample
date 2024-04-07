'''
    This is a Python3 app.

    Purpose: Parsing text files construction.

    Usage:  python3 txtparser.py [txtfile] [option]

        eg. python3 txtparser.py sample.txt
            python3 txtparser.py -b sample.txt
            python3 txtparser.py -s PCT191231172220.txt > result.txt   # Result output to file 'result.txt'

    Options:
        txtfile         txt file path which will be parsed
        -s, --space     represent space as '[\s]'
        -b, --byte      output byte codes of entire text file

    Run command line 'python3 txtparser.py -h' for help.
'''
import os, argparse

# Parsing text files construction
def parseContent(content, space = False, byte = False):
    bytesCode = bytes()
    spaceCount = 0
    charsCountForEachLine = 0
    totalChars = 0
    bytesCount = 0
    bytesPerUnicode = 1
    print('------------------- BOF -------------------')
    for index, code in enumerate(content):
        bytesCode += bytes([code])
        if byte:
            # output entire text file in bytes
            print('[\\0x%s]' % bytesCode.hex(), end='')
            bytesCode = bytes()
            continue
        bytesCount += 1
        if bytesCount < bytesPerUnicode:
            continue
        else:
            if bytesCount == 1:
                if code>127:
                    # when code was greater than 127, that means it belong to ascii extended code set,
                    # and it need to be decoded by the rules of utf-8 to unicode
                    if code>=192 and code<=223:
                        # 2 bytes
                        bytesPerUnicode = 2
                        continue
                    elif code>=224 and code<=239:
                        # 3 bytes
                        bytesPerUnicode = 3
                        continue
        char = bytesCode.decode(encoding='utf-8')
        charsCountForEachLine += 1
        totalChars += 1
        if char.isprintable():
            if space:
                if code == 32:
                    # Space，represented by '\s'
                    spaceCount += 1
                else:
                    if spaceCount>0:
                        print('[\\s]{%s}' % spaceCount, end='')
                        spaceCount = 0
                    print('%s' % char, end='')
            else:
                print('%s' % char, end='')
        else:
            if space:
                if spaceCount>0:
                    print('[\\s]{%s}' % spaceCount, end='')
                    spaceCount = 0
            if code == 10:
                # LF，represented by '\n'
                print('[\\n]', end='')
                if charsCountForEachLine>0:
                    print('<%s>' % charsCountForEachLine, end='')
                    charsCountForEachLine = 0
                print('\n', end='')
            elif code == 13:
                # CR，represented by '\r'
                print('[\\r]', end='')
            elif code == 9:
                # TAB，represented by '\t'
                print('[\\t]', end='')
            else:
                if bytesCount == 1:
                    # other unrecognized characters，represented to a hex code '\0x..'
                    print('[\\0x%s]' % bytesCode.hex(), end='')
                else:
                    # output double/triple bytes unicode
                    print('%s' % char, end='')
        # Processed a code/unicode, then empty and init
        bytesCode = bytes()
        bytesCount = 0
        bytesPerUnicode = 1
    # Post loop, print brief summary
    if byte:
        print('')
    elif charsCountForEachLine>0:
        print('<%s>' % charsCountForEachLine)
    print('------------------- EOF -------------------')
    print('''
        \nParsing Summary:
        \nBytes: %s, Characters: %s
        \n[..] represent to control character
        \n{..} represent to total number, it means the amount of spaces
        \n<..> represent to total number, it means the quantity of characters for each line
        \n
        \nCheck out http://www.asciitable.com/ for more detailed information about ASCII
        ''' % (index+1, totalChars)
    )

# --------------------------------------------------------------------------
# Main process Separator
# --------------------------------------------------------------------------
aparser = argparse.ArgumentParser(
    prog='Text File Parser - txtparser.py',
    description='Parsing text files construction.'
)
aparser.add_argument(
    'txtfile',
    type=str,
    help='txt file path which will be parsed'
)
aparser.add_argument(
    '-s', '--space',
    action='store_true',
    help='represent space as \'[\s]\''
)
aparser.add_argument(
    '-b', '--byte',
    action='store_true',
    help='output byte codes of entire text file'
)
aparser.add_argument(
    '-v', '--version',
    action='version',
    version='%(prog)s v0.1.0'
)
args = aparser.parse_args()

# Check file existed or not
if not os.path.exists(args.txtfile):
    print('Text file [%s] not found.' % args.txtfile)
    exit(-1)

try:
    with open(args.txtfile, 'rb') as fb:
        parseContent(fb.read(), space=args.space, byte=args.byte)
        fb.close()
except OSError as e:
    print(e)

