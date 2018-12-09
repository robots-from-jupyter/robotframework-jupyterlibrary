from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary.base import LibraryComponent, keyword


try:
    import cv2
except ImportError:
    cv2 = None

try:
    from PIL import Image
except ImportError:
    Image = None


class ScreenshotKeywords(LibraryComponent):
    @keyword
    def capture_element_screenshot(self, locator, filename):
        el = self.find_element(locator)
        bbox = self.normalize_bounding_box({**el.location, **el.size})
        filename = BuiltIn().run_keyword("Capture Page Screenshot", filename)
        self.crop_image(filename, **bbox)

    def normalize_bounding_box(self, bbox):
        """ Normalize a bounding box to reasonable defaults
            TODO: also handle larger-than-screen elements (if that's a thing)
        """
        return {
            k: (
                max(int(round(v)), 1)
                if k in ["width", "height"]
                else max(int(round(v)), 0)
            )
            for k, v in bbox.items()
        }

    @keyword
    def crop_image(self, in_file, x, y, width, height, out_file=None):
        if cv2:
            return self.crop_with_opencv(in_file, x, y, width, height, out_file)
        elif Image:
            return self.crop_with_pillow(in_file, x, y, width, height, out_file)

    def crop_with_opencv(self, in_file, x, y, width, height, out_file=None):
        out_file = out_file or in_file
        im = cv2.imread(in_file)
        im = im[int(y) : int(y + height), int(x) : int(x + width)]
        cv2.imwrite(out_file, im)
        return out_file

    def crop_with_pillow(self, in_file, x, y, width, height, out_file=None):
        out_file = out_file or in_file
        img = Image.open(in_file)
        area = img.crop((int(x), int(y), int(x + width), int(y + height)))

        with open(out_file, "wb") as output:
            area.save(output, "png")

        return out_file
