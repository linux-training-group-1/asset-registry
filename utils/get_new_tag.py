import os
import sys

env_file = os.getenv('GITHUB_ENV')
new_tag_with_name = sys.argv[1]


def set_actions_env_var(var_name, value):
    with open(env_file, "a") as my_file:
        my_file.write(str(var_name) + "=" + str(value) + "\n")


ver = new_tag_with_name.split(":")[1]
set_actions_env_var("DOCKER_NEW_TAG", ver)
