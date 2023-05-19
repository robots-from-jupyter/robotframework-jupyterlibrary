"""Handle working with WebElements."""

from typing import List, Union

from selenium.webdriver.remote.webelement import WebElement
from SeleniumLibrary.base import LibraryComponent, keyword


class WebElementKeywords(LibraryComponent):

    """A component for working with WebElements."""

    @keyword(name="Get WebElement Relative To")
    def get_webelement_relative_to(
        self,
        element: WebElement,
        locator: Union[WebElement, str],
    ) -> WebElement:
        """Get the first WebElement relative to ``element`` matching the given ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        return self.element_finder.find_element(locator=locator, parent=element)

    @keyword(name="Get WebElements Relative To")
    def get_webelements_relative_to(
        self,
        element: WebElement,
        locator: Union[WebElement, str],
    ) -> List[WebElement]:
        """Get a list of WebElement objects relative to ``element` matching the ``locator``.

        See the `Locating elements` section for details about the locator syntax.
        """
        return self.element_finder.find_elements(locator=locator, parent=element)
