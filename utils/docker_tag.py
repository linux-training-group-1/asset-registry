import os
import sys

import docker
from packaging import version
import re

app_name = sys.argv[1]
commit_msg = os.environ['COMMIT_MSG']
"This is an example commit message [version=3.4.6] in github"
"example version string 2.3.5-rc.1"


def get_latest_docker_tag(images):
    for image in images:
        for tag in image.tags:
            if app_name in tag:
                return tag.split(":")[1]


def get_version_from_commit(commit):
    expression = "\[version=(.*?)\]"
    match = re.search(expression, commit)
    if match:
        print("New version defined in commit message")
        print(match.group(0))
        return match.group(0).split("=")[1].strip()


def get_docker_images():
    client = docker.from_env()
    imgs = client.images.list()
    return imgs


new_ver = get_version_from_commit(commit_msg)
if new_ver:
    print(app_name + ":" + new_ver)
else:
    all_images = get_docker_images()
    # print(all_images)
    latest_version_str = get_latest_docker_tag(all_images)
    latest_version = version.parse(latest_version_str)
    if str(latest_version) == "false":
        print("false")
        exit(0)
    if str(latest_version) == "latest":
        print("0.1.0")
        exit(0)
    new_tag = app_name + ":" + str(latest_version.major) + "." + str(latest_version.minor) + "." + str(
        latest_version.micro + 1)
    print(new_tag)
