import os
import time

import gevent
import requests
from locust import HttpUser, task, between
from locust.env import Environment
from locust.log import setup_logging
from locust.stats import stats_printer, stats_history

setup_logging("INFO", None)
"""
This file contains the tests that run on the staging environment
"""

host = "http://" + os.getenv("STAGING_IP", "localhost:5000")
health_endpoint = "/health"
ready_endpoint = "/ready"
health_checks = 0
ready_checks = 0
checks_max = 10


def check_health():
    global health_checks
    while health_checks < checks_max:
        health_checks += 1
        url = host + health_endpoint
        print(url)
        resp = requests.get(url)
        if resp.status_code == 200:
            return True
        time.sleep(1)
    return False


def check_ready():
    global ready_checks
    while ready_checks < checks_max:
        ready_checks += 1
        resp = requests.get(host + ready_endpoint)
        if resp.status_code == 200:
            return True
        time.sleep(1)
    return False


class User(HttpUser):
    wait_time = between(1, 3)
    host = host

    @task
    def my_task(self):
        self.client.get(host)

    @task
    def task_404(self):
        self.client.get(host + "non-existing-path")


def test_load(users=5, spawn_rate=10, time_s=6):
    assert check_health()
    assert check_ready()
    # setup Environment and Runner
    env = Environment(user_classes=[User])
    env.create_local_runner()

    # start a greenlet that periodically outputs the current stats
    gevent.spawn(stats_printer(env.stats))

    # start a greenlet that save current stats to history
    gevent.spawn(stats_history, env.runner)

    # start the test
    env.runner.start(users, spawn_rate=spawn_rate)

    # in 60 seconds stop the runner
    gevent.spawn_later(time_s, lambda: env.runner.quit())

    # wait for the greenlets
    env.runner.greenlet.join()

    assert env.stats.total.avg_response_time < 60
    assert env.stats.total.num_failures == 0
    assert env.stats.total.get_response_time_percentile(0.95) < 100
