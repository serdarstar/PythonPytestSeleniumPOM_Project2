import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from webdriver_manager.firefox import GeckoDriverManager
chromeOptions=webdriver.ChromeOptions()
# Disables push notifications
prefs = {"profile.default_content_setting_values.notifications" : 2}
chromeOptions.add_experimental_option("prefs", prefs)
# Prevents Chrome is being controlled by automated test software message
chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation'])
# Open in headless mode
#chromeOptions.headless = True

from Utilities import configReader


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

@pytest.fixture()
def log_on_failure(request,get_browser):
    yield
    item = request.node
    driver = get_browser
    if item.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(), name="dologin", attachment_type=AttachmentType.PNG)


@pytest.fixture(params=["chrome"],scope="function") # If you want to run your cases on Firefox as well, add Firefox to params here
def get_browser(request):

    if request.param == "chrome":
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chromeOptions)
    if request.param == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    request.cls.driver = driver
    driver.get(configReader.readConfig("basic info","testsiteurl"))
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()