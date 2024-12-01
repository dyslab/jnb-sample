'''
    b64decoder.py   用于解码经过 base64 编码的 v2ray 节点信息文件
'''
import os
import sys
import base64
import argparse


def decodeBase64File(input_filename, output_filename, urlsafe_mode):
    try:
        finput = open(input_filename, 'r')
        with open(output_filename, 'w', encoding='utf-8') as foutput:
            if urlsafe_mode:
                foutput.write(base64.urlsafe_b64decode(finput.read().encode()).decode())
            else:
                foutput.write(base64.b64decode(finput.read().encode()).decode())
            foutput.close()
        finput.close()
        print(f'Decoding mode: \033[33m{"url-safe" if urlsafe_mode else "base64"}\033[0m')
        print(f'File \033[32;3m{input_filename}\033[0m has been decoded to \033[34;3m{output_filename}\033[0m')
    except IOError as err:
        print(f'Error occured.\n{err}')
        exit(1)

def generateOutputFilename(input_filename):
    base_name, base_ext = os.path.splitext(os.path.basename(input_filename))
    return os.path.join(os.path.dirname(input_filename), f'{base_name}_output{base_ext}')


if __name__ == '__main__':
    # 针对 Windows 平台上的 CMD 命令行终端设置彩色字符输出
    if os.name == 'nt':
        os.system('color') 

    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.description = 'Decode a base64 encoded file'
        parser.add_argument('file', help='the file to be decoded')
        parser.add_argument('-U', '--url', default=False, action='store_true', help='url-safe decoding')
        args = parser.parse_args()
        input_name = args.file
        decode_mode = args.url
    else:
        input_name = 'example.txt'
        decode_mode = False

    if os.path.exists(input_name):
        decodeBase64File(input_name, generateOutputFilename(input_name), decode_mode)
    else:
        print(f'File \033[31;3m{args.file}\033[0m does not exist.')
        exit(1)
