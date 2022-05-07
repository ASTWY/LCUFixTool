# -*- coding: utf-8 -*-
import os
from urllib.request import urlopen

import requests
from rich.progress import Progress


def download_from_url(url, dst):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    while True:
        res = requests.head(url)
        if res.status_code != 200:
            url = res.headers['location']
        else:
            break
    file_size = int(urlopen(url).info().get('Content-Length', -1))

    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    with Progress() as progress:
        task1 = progress.add_task("[green]Downloading...", total=file_size)
        while not progress.finished:
            req = requests.get(url, headers=header, stream=True)
            with (open(dst, 'ab')) as f:
                for chunk in req.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                    progress.update(task1, advance=1024)
    return file_size


if __name__ == '__main__':
    url = "http://share.astwy.top/s/khd/9.22_5407a252cb2a082e6dfac5901fd8f678.zip"
    download_from_url(url, "./a.exe")