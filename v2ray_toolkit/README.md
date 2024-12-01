# v2ray_toolkit: V2ray Config File Toolkit Samples

## Contents

- `fetch-wz2023jd.py` - Python script for crawl v2ray configs from telegram preview page [WZ2023JD](https://t.me/s/wz2023jd)

  ```shell
  python fetch-wz2023jd.py      # Run in terminal
  # or click `run.b64decoder.py.bat` to go on Windows
  ```

  > NOTE: This script was invoked by GitHub Action _[fetch-v2ray-nodes.yml](../.github\workflows\fetch-v2ray-nodes.yml)_.

- `b64decoder.py` - Python script for decoding v2ray base64-encoded files

  ```shell
  python b64decoder.py         # Run in terminal, with argument '--help' for help 
  # or click `run.b64decoder.py.bat` to go on Windows
  ```

- `b64decoder.ps1` - PowerShell script for decoding v2ray base64-encoded files

  ```powershell
  ./b64decoder.ps1              # Run in PowerShell terminal
  # or click `run.b64decoder.ps1.bat` to go on Windows  
  ```
