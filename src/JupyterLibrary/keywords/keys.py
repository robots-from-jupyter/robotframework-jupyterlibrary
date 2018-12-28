import platform

from SeleniumLibrary.base import LibraryComponent, keyword


class KeyKeywords(LibraryComponent):
    @keyword
    def get_accelerator_key(self):
        return "COMMAND" if platform.system() == "Darwin" else "CONTROL"
