import sys, os
import types

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

    sd = selenium_driver(chrome_driver=FakeChrome())
    elem = sd.get_element_by_class_name_from_url("http://example", "cls")
    assert elem is not None
    assert hasattr(elem, 'text')
    assert elem.text == "found"


def test_get_element_timeout_returns_none(monkeypatch):
    monkeypatch.setattr('python_boilerplate.driver.WebDriverWait', FakeWaitTimeout)

    class FakeChrome:
        def get(self, url):
            self.url = url

    sd = selenium_driver(chrome_driver=FakeChrome())
    elem = sd.get_element_by_class_name_from_url("http://example", "cls", timeout=0)
    assert elem is None


def test_get_text_by_class_name_from_url(monkeypatch):
    monkeypatch.setattr('python_boilerplate.driver.WebDriverWait', FakeWaitText)

    class FakeChrome:
        def get(self, url):
            self.url = url

    sd = selenium_driver(chrome_driver=FakeChrome())
    txt = sd.get_text_by_class_name_from_url("http://example", "cls")
    assert txt == "the text"


def test_js_fallback_returns_element(monkeypatch):
    # WebDriverWait will timeout, but execute_script returns the element
    monkeypatch.setattr('python_boilerplate.driver.WebDriverWait', FakeWaitTimeout)

    class FakeChrome:
        def __init__(self):
            self.page_source = "<html></html>"
        def get(self, url):
            self.url = url
        def execute_script(self, script, selector):
            return FakeElement("from_js")
        def save_screenshot(self, path):
            # simulate saving a file
            with open(path, "wb") as f:
                f.write(b"")

    sd = selenium_driver(chrome_driver=FakeChrome())
    elem = sd.get_element_by_class_name_from_url("http://example", "cls", timeout=0)
    assert elem is not None
    assert elem.text == "from_js"


def test_failure_saves_diagnostics(monkeypatch):
    # WebDriverWait will timeout and execute_script returns None -> diagnostics saved
    monkeypatch.setattr('python_boilerplate.driver.WebDriverWait', FakeWaitTimeout)

    class FakeChrome:
        def __init__(self):
            self.page_source = "<html>no elem</html>"
        def get(self, url):
            self.url = url
        def execute_script(self, script, selector):
            return None
        def save_screenshot(self, path):
            with open(path, "wb") as f:
                f.write(b"X")

    sd = selenium_driver(chrome_driver=FakeChrome())
    elem = sd.get_element_by_class_name_from_url("http://example", "cls", timeout=0)
    assert elem is None

    import tempfile, os, glob
    screenshots = glob.glob(os.path.join(tempfile.gettempdir(), "timeout_screenshot_*.png"))
    pages = glob.glob(os.path.join(tempfile.gettempdir(), "timeout_page_source_*.html"))
    assert screenshots, "screenshot not saved"
    assert pages, "page source not saved"
