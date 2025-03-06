# CC0 — Please Steal

import urllib
import urllib.request
import pathlib
import json

remote_root = "https://usdexample-towerapt.s3.us-west-004.backblazeb2.com/TowerApt/src/tex/"

with open("../src/texture_catalog.json", 'r') as file:
    urls = json.load(file).get('paths')[1:]
    # print(paths)

    for url in urls:
        save_to: pathlib.Path = pathlib.Path("../src/tex/") / url.removeprefix(remote_root)
        save_to.parent.mkdir(parents=True, exist_ok=True)
        file = urllib.request.urlretrieve(url, filename=save_to)
        print(save_to)