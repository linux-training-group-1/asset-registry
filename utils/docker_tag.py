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
    if new_ver == "false":
        os.environ["SHOULD_PUSH"] = "0"
        print("Not pushing the image to k8s")
        exit(0)
    else:
        new_tag = app_name + ":" + str(new_ver)
        os.environ["DOCKER_IMAGE_TAG"] = new_tag
        print("New tag: " + new_tag)
        exit(0)
else:
    all_images = get_docker_images()
    # print(all_images)
    latest_version_str = get_latest_docker_tag(all_images)
    latest_version = version.parse(latest_version_str)
    if str(latest_version) == "latest":
        new_tag = app_name + ":" + "0.1.0"
        os.environ["DOCKER_IMAGE_TAG"] = new_tag
        os.environ["SHOULD_PUSH"] = "1"
        print("New tag: ")
    else:
        new_tag = app_name + ":" + str(latest_version.major) + "." + str(latest_version.minor) + "." + str(
            latest_version.micro + 1)
        os.environ["DOCKER_IMAGE_TAG"] = new_tag
        os.environ["SHOULD_PUSH"] = "1"
        print("New tag: " + new_tag)
