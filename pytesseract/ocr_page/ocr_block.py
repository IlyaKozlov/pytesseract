from collections import defaultdict
from typing import List

from pytesseract.ocr_page.bbox import BBox
from pytesseract.ocr_page.ocr_paragraph import OcrParagraph
from pytesseract.ocr_page.ocr_tuple import OcrElement


class OcrBlock:
    level = 2

    def __init__(self, order: int, bbox: BBox, paragraphs: List[OcrParagraph]) -> None:
        super().__init__()
        self.order = order
        self.bbox = bbox
        self.paragraphs = paragraphs

    def text(self, confidence_threshold: float) -> str:
        return "".join(paragraph.text(confidence_threshold) for paragraph in self.paragraphs)

    @staticmethod
    def from_list(elements: List[OcrElement]) -> "OcrBlock":
        paragraph2elements = defaultdict(list)
        head = None
        for element in elements:
            if element.level > OcrBlock.level:
                paragraph2elements[element.paragraph_num].append(element)
            elif element.level == OcrBlock.level:
                head = element
            else:
                raise ValueError("Some element {} has level greater than this {}".format(element, OcrBlock.level))
        paragraphs = [OcrParagraph.from_list(paragraph2elements[key]) for key in sorted(paragraph2elements.keys())]
        return OcrBlock(paragraphs=paragraphs, order=head.block_num, bbox=head.bbox)
