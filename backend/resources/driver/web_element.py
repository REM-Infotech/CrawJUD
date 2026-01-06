"""Module for managing WebDriver instances and related utilities."""

from __future__ import annotations

import platform
from contextlib import suppress
from pathlib import Path
from time import sleep
from typing import TYPE_CHECKING, Self, TypedDict

from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.webdriver.common.by import By
from selenium.webdriver.common.utils import keys_to_typing
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webelement import (
    WebElement as SEWebElement,
)
from selenium.webdriver.support.ui import Select

from backend.common.raises import raise_execution_error

if TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver
    from seleniumwire.webdriver import Chrome


class RectWebElement(TypedDict):
    """Dict Rect Webelement."""

    height: float
    width: float
    x: float
    y: float


class WebElement(SEWebElement):
    """Gerencie e interaja com elementos web personalizados."""

    _current_driver: WebDriver = None
    _action: ActionChains = None
    parent: WebDriver | Chrome

    def __call__(self, *args: Any, **kwargs: Any) -> None:
        """Execute um clique no elemento ao chamar a instância.

        Args:
            *args (Any): Argumentos posicionais.
            **kwargs (Any): Argumentos nomeados.

        """
        return super().click()

    @classmethod
    def set_driver(cls, _driver: WebDriver) -> type[Self]:
        """Defina o driver atual para a classe e inicialize ActionChains.

        Args:
            _driver (WebDriver): Instância do driver a ser utilizada.

        Returns:
            type[Self]: Classe atual com driver configurado.

        """
        cls._current_driver = _driver
        cls._action = ActionChains(_driver)

        return cls

    @property
    def rect(self) -> RectWebElement:
        """Obtenha o retângulo do elemento na página."""
        return super().rect

    @property
    def location(self) -> RectWebElement:
        """Obtenha a posição do elemento na página."""
        return super().location

    @property
    def current_driver(self) -> WebDriver | Chrome:
        """Obtenha o driver atual associado ao elemento web."""
        return self._current_driver

    def double_click(self) -> None:
        """Execute um duplo clique no elemento web."""
        self._action.double_click(self).perform()

    def select_item(self, item: str) -> None:
        """Selecione um item em um elemento select pelo valor.

        Args:
            item (str): Valor do item a ser selecionado.

        """
        Select(self).select_by_value(item)

    def click(self) -> None:
        """Perform a click action on a web element with brief pauses.

        Args:
            element (WebElement): The target web element.

        Implements a click with pre- and post-click delays.

        """
        sleep(0.05)
        super().click()
        sleep(0.05)

    def clear(self) -> None:
        """Limpe o conteúdo do elemento web após clicar e aguardar."""
        self.click()
        sleep(0.5)
        super().clear()
        sleep(1)

    def scroll_to(self) -> None:
        """Scroll the view to the specified web element."""
        self._action.scroll_to_element(self)
        sleep(0.5)

    def find_element(
        self,
        by: str = By.ID,
        value: Any | None = None,
    ) -> WebElement:
        """Localize e retorne um elemento filho deste elemento.

        Args:
            by (str): Estratégia de localização (ex: By.ID).
            value (Any | None): Valor a ser buscado.

        Returns:
            WebElement: Elemento encontrado.

        """
        return super().find_element(by=by, value=value)

    def find_elements(
        self,
        by: str = By.ID,
        value: Any | None = None,
    ) -> list[WebElement]:
        """Localize e retorne uma lista de elementos filhos deste elemento.

        Args:
            by (str): Estratégia de localização (ex: By.ID).
            value (Any | None): Valor a ser buscado.

        Returns:
            list[WebElement]: Lista de elementos encontrados.

        """
        return super().find_elements(by=by, value=value)

    def send_keys(self, word: Any) -> None:
        """Envie teclas ou texto para o elemento web.

        Args:
            word (Any): Tecla ou texto a ser enviado.

        """
        send = False
        for key in dir(Keys):
            if getattr(Keys, key) == word:
                send = True
                super().send_keys(word)
                break

        if not send:
            for c in str(word):
                sleep(0.01)
                super().send_keys(c)

    def send_file(self, file: str | Path) -> None:
        """Envie um arquivo para o elemento input do tipo file.

        Args:
            file (str | Path): Caminho do arquivo a ser enviado.

        """
        file_ = file
        if isinstance(file, Path):
            file_ = file.as_posix() if platform.system() == "Linux" else str(file)
        self._execute(
            Command.SEND_KEYS_TO_ELEMENT,
            {
                "text": "".join(keys_to_typing(file_)),
                "value": keys_to_typing(file_),
            },
        )

    def display_none(self) -> None:
        """Wait for an element's display style to change to 'none'.

        Args:
            elemento (WebElement): The element to monitor.

        """
        while True:
            style = self.get_attribute("style")
            if "display: none;" not in style:
                sleep(0.01)
                break

    def select2(self, to_search: str) -> None:
        r"""Select an option from a Select2 dropdown based on a search text.

        Args:
            to_search (str): The option text to search and select.

        """
        items = self.find_elements(By.TAG_NAME, "option")
        opt_itens: dict[str, str] = {}

        id_select = self.get_attribute("id")

        for item in items:
            value_item = item.get_attribute("value")

            cms = f"select[id='{id_select}'] > option[value='{value_item}']"
            text_item = self.parent.execute_script(
                f'return $("{cms}").text();',
            )

            text_item = " ".join([
                item for item in str(text_item).strip().split(" ") if item
            ]).upper()
            opt_itens.update({text_item: value_item})

        to_search = " ".join(to_search.split(" ")).upper()
        value_opt = opt_itens.get(to_search)

        if value_opt:
            select_element = self.parent.find_element(
                By.CSS_SELECTOR,
                f"select[id='{id_select}']",
            )
            command = """
            const selector = $(arguments[0]);
            selector.val([arguments[1]]);
            selector.trigger("change");
            """
            self.parent.execute_script(
                command,
                select_element,
                value_opt,
            )
            sleep(5)
            return

        raise_execution_error(
            message=f'Opção "{to_search}" não encontrada!',
        )

    def scroll_from_origin(
        self,
        delta_x: int,
        delta_y: int,
        origin: Self | None = None,
    ) -> None:
        """Role a partir de uma origem específica no elemento web.

        Args:
            delta_x (int): Deslocamento horizontal.
            delta_y (int): Deslocamento vertical.
            origin (Self | None): Elemento de origem do scroll.

        """
        if not origin:
            origin = self

        location = origin.location
        scroll_origin = ScrollOrigin.from_element(
            origin,
            x_offset=location["x"],
            y_offset=location["y"],
        )

        self._action.scroll_to_element()

        with suppress(Exception):
            return self._action.scroll_from_origin(
                scroll_origin=scroll_origin,
                delta_x=0,
                delta_y=delta_y,
            ).perform()

    def scroll_to_element(self) -> None:
        """Scroll to element.

        If the element is outside the viewport, scrolls the bottom of the
        element to the bottom of the viewport.

        Args:
            element: Which element to scroll into the viewport.

        """
        self._action.scroll_to_element(self).perform()

    def blur(self) -> None:
        """Remova o foco do elemento web usando JavaScript.

        Remove o foco do elemento utilizando o id, se existir,
        ou o próprio elemento como fallback.
        """
        command = "arguments[0].blur();"
        self.parent.execute_script(command, self)
