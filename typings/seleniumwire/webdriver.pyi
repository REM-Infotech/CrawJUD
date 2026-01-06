from selenium.webdriver import Chrome as _Chrome
from seleniumwire.inspect import InspectRequestsMixin

from typings import Any

class DriverCommonMixin:
    def _setup_backend(self, seleniumwire_options: dict[str, Any]) -> dict[str, Any]: ...
    @property
    def proxy(self) -> dict[str, Any]: ...
    @proxy.setter
    def proxy(self, proxy_conf: dict[str, Any]) -> None: ...

class Chrome(InspectRequestsMixin, DriverCommonMixin, _Chrome):
    @property
    def is_closed(self) -> bool: ...
