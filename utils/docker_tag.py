import os
import sys

import docker
import requests
from packaging import version
import re

app_name = sys.argv[1]
docker_username = sys.argv[2]
docker_password = sys.argv[3]
commit_msg = os.environ['COMMIT_MSG']
docker_host = "https://dock-reg-0001.ml"
docker_api = "/v2/asset-app/tags/list"
"This is an example commit message [version=3.4.6] in github"
"example version string 2.3.5-rc.1"


def get_latest_docker_tag(tags):
    latest = "latest"
    for tag in tags:
        try:
            if version.parse(tag) > version.parse(latest):
                latest = tag
        except Exception as e:
            pass
    return str(latest)


def get_version_from_commit(commit):
    expression = "\[version=(.*?)\]"
    match = re.search(expression, commit)
    if match:
        print("New version defined in commit message")
        print(match.group(0))
        return match.group(0).split("=")[1].strip()


def get_docker_tags():
    session = requests.Session()
    session.auth = (docker_username, docker_password)
    auth = session.get(docker_host)
    response = session.get(docker_host + docker_api)
    return response.json()['tags']


new_ver = get_version_from_commit(commit_msg)
if new_ver:
    if new_ver == "false":
        os.environ["SHOULD_PUSH"] = "0"
        print("Not pushing the image to k8s")
        exit(0)
    else:
        new_tag = app_name + ":" + str(new_ver)
        os.environ["DOCKER_IMAGE_TAG"] = new_tag
        os.environ["SHOULD_PUSH"] = "1"
        print("New tag: " + new_tag)
        exit(0)
else:
    all_images = get_docker_tags()
    print(all_images)
    latest_version_str = get_latest_docker_tag(all_images)
    print()
    latest_version = version.parse(latest_version_str)
    if str(latest_version) == "latest":
        new_tag = app_name + ":" + "0.1.0"
        os.environ["DOCKER_IMAGE_TAG"] = new_tag
        os.environ["SHOULD_PUSH"] = "1"
        print("New tag: " + new_tag)
    else:
        new_tag = app_name + ":" + str(latest_version.major) + "." + str(latest_version.minor) + "." + str(
            latest_version.micro + 1)
        os.environ["DOCKER_IMAGE_TAG"] = new_tag
        os.environ["SHOULD_PUSH"] = "1"
        print("New tag: " + new_tag)
