from collections import defaultdict
from typing import List

from pytesseract.ocr_page.bbox import BBox
from pytesseract.ocr_page.ocr_line import OcrLine
from pytesseract.ocr_page.ocr_tuple import OcrElement


class OcrParagraph:

    level = 3

    def __init__(self, order: int, bbox: BBox, lines: List[OcrLine]) -> None:
        super().__init__()
        self.order = order
        self.bbox = bbox
        self.lines = sorted(lines, key=lambda line: line.order)

    def text(self, confidence_threshold: float) -> str:
        return "".join(line.text(confidence_threshold) for line in self.lines)

    @staticmethod
    def from_list(paragraph: List[OcrElement]) -> "OcrParagraph":
        line2element = defaultdict(list)
        head = None
        for element in paragraph:
            if element.level > OcrParagraph.level:
                line2element[element.line_num].append(element)
            else:
                head = element

        lines = [OcrLine.from_list(line=line2element[key]) for key in sorted(line2element.keys())]
        return OcrParagraph(order=head.paragraph_num, lines=lines, bbox=head.bbox)
