import os
import re
import requests
from typing import List

DEFAULT_OUTPUT_FILE: str = f'{os.path.splitext(os.path.realpath(__file__))[0]}.txt'  # Path of the output file

def traverseText(nodeArray: List[str], text: str) -> None:
    matchText : re.Match[str] | None = re.search(r'((vmess)|(vless)|(ssr)|(ss)|(trojan))(:\/\/)(.+)', text)
    if matchText:
            indexEndPos : int = matchText[8].find('<')
            if indexEndPos > 0:
                node : str = matchText[1] + matchText[7] + matchText[8][:indexEndPos]
                restPartText: str = text[indexEndPos:]
                try:
                    nodeArray.index(node)
                except ValueError as err:
                    nodeArray.append(node)  
                traverseText(nodeArray, restPartText)

def fetchNodes() -> None:
    BASE_URL : str = 'https://t.me/s/wz2023jd'
    # Send a GET request to the URL
    response: requests.Response = requests.get(
        BASE_URL, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
            }
        )
    # Check if the request was successful
    if response.status_code == 200:
        htmlLines: List[str] = response.text.replace(' ', '').split('\n');
        nodeList: List[str] = []
        for line in htmlLines:
            traverseText(nodeList, line)
        if len(nodeList) > 0:
            try:
                with open(DEFAULT_OUTPUT_FILE, 'w') as f:
                    for node in nodeList:
                        f.write(node + '\n')
                print(f'[SUCCEED] {len(nodeList)} Nodes saved to: {DEFAULT_OUTPUT_FILE}')
            except Exception as err:
                print(f'[FAILED] {err}')
    else:
        print(f'[ERROR] Response returned code {response.status_code}, returned text {response.text}')

if __name__ == '__main__':
    fetchNodes()
