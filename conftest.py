import os
import random
import time

import allure
import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from dotenv import load_dotenv
from opencart.utils import attach
import logging
import datetime

load_dotenv()
OPENCART_URL = os.getenv("OPENCART_LINK")

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--executor", action="store", default="127.0.0.1")
    parser.addoption("--mobile", action="store_true")
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--logs", action="store_true")
    parser.addoption("--video", action="store_true")
    parser.addoption("--bv")
    parser.addoption("--log_level", action="store", default="INFO")


@allure.step("Waiting for availability {url}")
def wait_url_data(url, timeout=10):
    """Метод ожидания доступности урла"""
    while timeout:
        response = requests.get(url)
        if not response.ok:
            time.sleep(1)
            timeout -= 1
        else:
            if "video" in url:
                return response.content
            else:
                return response.text
    return None

@pytest.fixture
def browser(request):
    browser = request.config.getoption("--browser")
    executor = request.config.getoption("--executor")
    vnc = request.config.getoption("--vnc")
    version = request.config.getoption("--bv")
    logs = request.config.getoption("--logs")
    video = request.config.getoption("--video")
    mobile = request.config.getoption("--mobile")

    executor_url = f"http://{executor}:4444/wd/hub"

    log_level = request.config.getoption("--log_level")

    logger = logging.getLogger(request.node.name)
    file_handler = logging.FileHandler(f"logs/{request.node.name}.log")
    file_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    logger.info("===> Test %s started at %s" % (request.node.name, datetime.datetime.now()))

    if browser == "chrome":
        options = ChromeOptions()
    elif browser == "firefox":
        options = FirefoxOptions()
    else:
        raise Exception("Driver not supported")

    caps = {
        "browserName": browser,
        "browserVersion": version,
        "selenoid:options": {
            "enableVNC": vnc,
            "name": request.node.name,
            "screenResolution": "1080x1280",
            "enableVideo": video,
            "enableLog": logs,
            "timeZone": "Europe/Moscow",
            "env": ["LANG=ru_RU.UTF-8", "LANGUAGE=ru:en", "LC_ALL=ru_RU.UTF-8"]

        },
        "acceptInsecureCerts": True,
    }

    for k, v in caps.items():
        options.set_capability(k, v)

    driver = webdriver.Remote(
        command_executor=executor_url,
        options=options
    )

    if not mobile:
        driver.maximize_window()


    driver.get(OPENCART_URL)

    driver.log_level = log_level
    driver.logger = logger
    driver.test_name = request.node.name

    logger.info("Browser %s started" % browser)

    def finalizer():
        video_url = f"http://{executor}:8080/video/{driver.session_id}.mp4"

        if request.node.status == "failed":
            if video:
                allure.attach(
                    body=wait_url_data(video_url),
                    name="video_for_" + driver.session_id,
                    attachment_type=allure.attachment_type.MP4,
                )

        if video and wait_url_data(video_url):
            requests.delete(url=video_url)

        driver.quit()

    request.addfinalizer(finalizer)
    return driver
