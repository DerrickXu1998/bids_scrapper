import sys, os
import types
import pytest
# Provide a minimal fake selenium package so tests can run without the real selenium
selenium = types.ModuleType("selenium")
sys.modules["selenium"] = selenium
sys.modules["selenium.webdriver"] = types.ModuleType("selenium.webdriver")
sys.modules["selenium.webdriver.support"] = types.ModuleType("selenium.webdriver.support")
sys.modules["selenium.webdriver.support.ui"] = types.ModuleType("selenium.webdriver.support.ui")
sys.modules["selenium.webdriver.support.expected_conditions"] = types.ModuleType("selenium.webdriver.support.expected_conditions")
sys.modules["selenium.common"] = types.ModuleType("selenium.common")
sys.modules["selenium.common.exceptions"] = types.ModuleType("selenium.common.exceptions")
sys.modules["selenium.webdriver.common"] = types.ModuleType("selenium.webdriver.common")
sys.modules["selenium.webdriver.common.by"] = types.ModuleType("selenium.webdriver.common.by")

# Minimal implementations used by our driver
sys.modules["selenium.webdriver.support.ui"].WebDriverWait = lambda driver, timeout: None
sys.modules["selenium.webdriver.support.expected_conditions"].visibility_of_element_located = lambda loc: (lambda d: True)
sys.modules["selenium.common.exceptions"].TimeoutException = Exception
class By:
    CLASS_NAME = "class"
    CSS_SELECTOR = "css"
sys.modules["selenium.webdriver.common.by"].By = By
sys.modules["selenium"].webdriver = types.SimpleNamespace(Chrome=lambda: None)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from python_boilerplate.driver import selenium_driver
from selenium.common.exceptions import TimeoutException

class FakeElement:
    def __init__(self, text="hello"):
        self.text = text


def _mock_driver(monkeypatch, chrome):
    """Instantiate selenium_driver while injecting a fake chrome driver."""
    def fake_init(self):
        self.chrome_driver = chrome

    monkeypatch.setattr(selenium_driver, "_initialize_driver", fake_init)
    return selenium_driver()

class FakeWait:
    def __init__(self, driver, timeout):
        pass
    def until(self, condition):
        return FakeElement("found")

class FakeWaitTimeout:
    def __init__(self, driver, timeout):
        pass
    def until(self, condition):
        raise TimeoutException()

class FakeWaitText:
    def __init__(self, driver, timeout):
        pass
    def until(self, condition):
        return FakeElement("the text")


def test_get_element_returns_element(monkeypatch):
    monkeypatch.setattr('python_boilerplate.driver.WebDriverWait', FakeWait)

    class FakeChrome:
        def get(self, url):
            self.url = url

    sd = _mock_driver(monkeypatch, FakeChrome())
    elem = sd.get_element_by_class_name_from_url("http://example", "cls")
    assert elem is not None
    assert hasattr(elem, 'text')
    assert elem.text == "found"


def test_get_element_timeout_returns_none(monkeypatch):
    monkeypatch.setattr('python_boilerplate.driver.WebDriverWait', TimeoutException)

    class FakeChrome:
        def get(self, url):
            self.url = url

    sd = _mock_driver(monkeypatch, FakeChrome())
    with pytest.raises(TimeoutException):
        sd.get_element_by_class_name_from_url("http://example", "cls", timeout=0)
