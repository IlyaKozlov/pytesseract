from typing import List

from pytesseract.ocr_page.bbox import BBox
from pytesseract.ocr_page.ocr_tuple import OcrElement
from pytesseract.ocr_page.ocr_word import OcrWord


class OcrLine:

    level = 4

    def __init__(self, order: int, bbox: BBox, words: List[OcrWord]) -> None:
        super().__init__()
        self.order = order
        self.bbox = bbox
        self.words = sorted(words, key=lambda word: word.order)

    def text(self, confidence_threshold) -> str:
        return " ".join(word.text for word in self.words
                        if word.text != ""
                        if word.confidence >= confidence_threshold
                        ) + "\n"

    @staticmethod
    def from_list(line: List[OcrElement]) -> "OcrLine":

        words = []
        head = None
        for element in line:
            assert element.level >= OcrLine.level, "get {} in line".format(element)
            if element.level == OcrLine.level:
                head = element
            else:
                words.append(element)
        line = sorted(line, key=lambda word: word.line_num)
        ocr_words = [OcrWord(bbox=word.bbox, text=word.text, order=word.word_num, confidence=word.conf)
                     for word in line]
        return OcrLine(order=head.line_num, words=ocr_words, bbox=head.bbox)
