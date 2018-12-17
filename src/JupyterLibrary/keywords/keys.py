""" Backport of SeleniumLibrary >3.2.0's `Press Keys`
"""
from robot.utils import plural_or_not

# flake8: noqa
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.utils import is_truthy


class KeysKeywords(LibraryComponent):
    @keyword
    def press_keys(self, locator=None, *keys):
        """Simulates user pressing key(s) to an element or on the active browser.
        If ``locator`` evaluates as false, see `Boolean arguments` for more
        details, then the ``keys`` are sent to the currently active browser.
        Otherwise element is searched and ``keys`` are send to the element
        identified by the ``locator``. In later case, keyword fails if element
        is not found. See the `Locating elements` section for details about
        the locator syntax.
        ``keys`` arguments can contain one or many strings, but it can not
        be empty. ``keys`` can also be a combination of
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html|Selenium Keys]
        and strings or a single Selenium Key. If Selenium Key is combined
        with strings, Selenium key and strings must be separated by the
        `+` character, like in `CONTROL+c`. Selenium Keys
        are space and case sensitive and Selenium Keys are not parsed
        inside of the string. Example AALTO, would send string `AALTO`
        and `ALT` not parsed inside of the string. But `A+ALT+O` would
        found Selenium ALT key from the ``keys`` argument. It also possible
        to press many Selenium Keys down at the same time, example
        'ALT+ARROW_DOWN`.
        If Selenium Keys are detected in the ``keys`` argument, keyword
        will press the Selenium Key down, send the strings and
         then release the Selenium Key. If keyword needs to send a Selenium
        Key as a string, then each character must be separated with
        `+` character, example `E+N+D`.
        `CTRL` is alias for
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#selenium.webdriver.common.keys.Keys.CONTROL|Selenium CONTROL]
        and ESC is alias for
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#selenium.webdriver.common.keys.Keys.ESCAPE|Selenium ESCAPE]
        New in SeleniumLibrary 3.3
        Examples:
        | `Press Keys` | text_field | AAAAA          |            | # Sends string "AAAAA" to element.                                                |
        | `Press Keys` | None       | BBBBB          |            | # Sends string "BBBBB" to currently active browser.                               |
        | `Press Keys` | text_field | E+N+D          |            | # Sends string "END" to element.                                                  |
        | `Press Keys` | text_field | XXX            | YY         | # Sends strings "XXX" and "YY" to element.                                        |
        | `Press Keys` | text_field | XXX+YY         |            | # Same as above.                                                                  |
        | `Press Keys` | text_field | ALT+ARROW_DOWN |            | # Pressing "ALT" key down, then pressing ARROW_DOWN and then releasing both keys. |
        | `Press Keys` | text_field | ALT            | ARROW_DOWN | # Pressing "ALT" key and then pressing ARROW_DOWN.                                |
        | `Press Keys` | text_field | CTRL+c         |            | # Pressing CTRL key down, sends string "c" and then releases CTRL key.            |
        | `Press Keys` | button     | RETURN         |            | # Pressing "ENTER" key to element.                                                |
        """
        parsed_keys = self._parse_keys(*keys)
        if is_truthy(locator):
            self.info("Sending key(s) %s to %s element." % (keys, locator))
        else:
            self.info("Sending key(s) %s to page." % str(keys))
        self._press_keys(locator, parsed_keys)

    def _map_ascii_key_code_to_key(self, key_code):
        map = {
            0: Keys.NULL,
            8: Keys.BACK_SPACE,
            9: Keys.TAB,
            10: Keys.RETURN,
            13: Keys.ENTER,
            24: Keys.CANCEL,
            27: Keys.ESCAPE,
            32: Keys.SPACE,
            42: Keys.MULTIPLY,
            43: Keys.ADD,
            44: Keys.SEPARATOR,
            45: Keys.SUBTRACT,
            56: Keys.DECIMAL,
            57: Keys.DIVIDE,
            59: Keys.SEMICOLON,
            61: Keys.EQUALS,
            127: Keys.DELETE,
        }
        key = map.get(key_code)
        if key is None:
            key = chr(key_code)
        return key

    def _map_named_key_code_to_special_key(self, key_name):
        try:
            return getattr(Keys, key_name)
        except AttributeError:
            message = "Unknown key named '%s'." % (key_name)
            self.debug(message)
            raise ValueError(message)

    def _press_keys(self, locator, parsed_keys):
        if is_truthy(locator):
            element = self.find_element(locator)
        else:
            element = None
        for parsed_key in parsed_keys:
            actions = ActionChains(self.driver)
            special_keys = []
            for key in parsed_key:
                if self._selenium_keys_has_attr(key.original):
                    special_keys = self._press_keys_special_keys(
                        actions, element, parsed_key, key, special_keys
                    )
                else:
                    self._press_keys_normal_keys(actions, element, key)
            for special_key in special_keys:
                self.info("Releasing special key %s." % special_key.original)
                actions.key_up(special_key.converted)
            actions.perform()

    def _press_keys_normal_keys(self, actions, element, key):
        self.info("Sending key%s %s" % (plural_or_not(key.converted), key.converted))
        if element:
            actions.send_keys_to_element(element, key.converted)
        else:
            actions.send_keys(key.converted)

    def _press_keys_special_keys(self, actions, element, parsed_key, key, special_keys):
        if len(parsed_key) == 1 and element:
            self.info("Pressing special key %s to element." % key.original)
            actions.send_keys_to_element(element, key.converted)
        elif len(parsed_key) == 1 and not element:
            self.info("Pressing special key %s to browser." % key.original)
            actions.send_keys(key.converted)
        else:
            self.info("Pressing special key %s down." % key.original)
            actions.key_down(key.converted)
            special_keys.append(key)
        return special_keys

    def _parse_keys(self, *keys):
        if not keys:
            raise AssertionError('"keys" argument can not be empty.')
        list_keys = []
        for key in keys:
            separate_keys = self._separate_key(key)
            separate_keys = self._convert_special_keys(separate_keys)
            list_keys.append(separate_keys)
        return list_keys

    def _parse_aliases(self, key):
        if key == "CTRL":
            return "CONTROL"
        if key == "ESC":
            return "ESCAPE"
        return key

    def _separate_key(self, key):
        one_key = ""
        list_keys = []
        for char in key:
            if char == "+" and one_key != "":
                list_keys.append(one_key)
                one_key = ""
            else:
                one_key += char
        if one_key:
            list_keys.append(one_key)
        return list_keys

    def _convert_special_keys(self, keys):
        KeysRecord = namedtuple("KeysRecord", "converted, original")
        converted_keys = []
        for key in keys:
            key = self._parse_aliases(key)
            if self._selenium_keys_has_attr(key):
                converted_keys.append(KeysRecord(getattr(Keys, key), key))
            else:
                converted_keys.append(KeysRecord(key, key))
        return converted_keys

    def _selenium_keys_has_attr(self, key):
        try:
            return hasattr(Keys, key)
        except UnicodeError:  # To support Python 2 and non ascii characters.
            return False
