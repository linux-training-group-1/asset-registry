import os
import sys

env_file = os.getenv('GITHUB_ENV')


def set_actions_env_var(var_name, value):
    with open(env_file, "a") as my_file:
        my_file.write(str(var_name) + "=" + str(value) + "\n")


string = sys.argv[1]
set_actions_env_var("VERSION", string.split(":")[-1])
