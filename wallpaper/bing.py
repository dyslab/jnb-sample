import os
import re
import requests
from httpcore import URL
from datetime import date

BASE_OUTPUT_DIR: str = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')  # Output directory

def createDirIfNotExists(dir: str) -> None:
    if not os.path.exists(dir):
        os.makedirs(dir)

def fetchBingImage() -> None:
    BASE_URL : str = 'https://www.bing.com'
    # Send a GET request to the URL
    response: requests.Response = requests.get(
        BASE_URL, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
            }
        )
    # Check if the request was successful
    if response.status_code == 200:
        pattern: str = r'"Image":(\{.+\}),"Head'
        match: re.Match[str] | None = re.search(pattern, response.text)
        if match:
            try:
                matchText: str = match.group()
                jsonStartPos: int = matchText.index('{')
                jsonEndPos: int = matchText.index('}') + 1
                jsonText: str = matchText[jsonStartPos:jsonEndPos]
                jsonObj: dict = eval(jsonText, {'true': True, 'false': False})
                if jsonObj and jsonObj['Url']:
                    print(f'Found image: {jsonObj["Url"]}')
                    urlPattern : str | None = re.search(r'^http[s]?://', jsonObj["Url"])
                    if urlPattern is None:
                        if jsonObj["Url"].startswith('/'):
                            jsonObj['Url'] = f'{BASE_URL}{jsonObj["Url"]}'
                        else:
                            jsonObj['Url'] = f'{BASE_URL}/{jsonObj["Url"]}'
                    imageFile: requests.Response = requests.get(jsonObj['Url'])
                    urlObj: URL = URL(jsonObj['Url'])
                    # Get the file name
                    fileName: str = urlObj.target.decode('utf-8').split('=')[-1]
                    # Get the file basename and extension
                    baseName, extension = os.path.splitext(fileName)
                    # Write to file
                    outputFilename: str = os.path.join(BASE_OUTPUT_DIR, f'[{date.today():%Y-%m-%d}]{baseName}{extension}')
                    with open(outputFilename, 'wb') as f:
                        f.write(imageFile.content)
                    print(f'[SUCCEED] Image downloaded successfully and saved to: {outputFilename}')
            except Exception as e:
                print(f'[ERROR] {e}')
        else:
            # Write to file
            outputFilename: str = os.path.join(BASE_OUTPUT_DIR, f'[{date.today():%Y-%m-%d}]bing_content_log.html')
            with open(outputFilename, 'w') as log:
                log.write(response.text)
            print(f'[FAILED] Unable to match the RegEx pattern {pattern} in response text. Check log file {outputFilename} 🤓')
    else:
        print(f'[ERROR] Response returned code {response.status_code}, returned text {response.text}')

if __name__ == '__main__':
    createDirIfNotExists(BASE_OUTPUT_DIR)
    fetchBingImage()
