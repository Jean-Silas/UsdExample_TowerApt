import os
import pathlib
import json
import pprint

remote_paths = []

def build_remote_path(base_path: str, file_name:str):
    remote_root = "https://usdexample-towerapt.s3.us-west-004.backblazeb2.com/TowerApt/src/tex/"
    return (remote_root + base_path + '/' + file_name).replace("\\", "/")


def traverse(base_path: str):
    paths = os.walk(base_path)
    for path_tuple in paths:
        # if len(path_tuple[1]) > 0:
        #     for inner in path_tuple[1]:
        #         traverse(path_tuple[0] + "/" + inner)

        for file_path in path_tuple[2]:
            remote_paths.append(build_remote_path(path_tuple[0].removeprefix(base_path)[1:], file_path))


traverse("../src/tex")
with open("../src/texture_catalog.json", 'w') as file:
    json.dump({"paths": remote_paths}, file, indent=4)

raw = os.walk("../src/tex")


for remote_path in remote_paths:
    pprint.pprint(remote_path)
