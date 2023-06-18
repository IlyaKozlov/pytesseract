from pytesseract.ocr_page.bbox import BBox


class OcrWord:
    level = 5

    def __init__(self, text: str, bbox: BBox, order: int, confidence: float) -> None:
        """
        Single word from ocr.
        :param text: extracted text
        :param bbox: word coordinates
        :param order: word order in line
        :param confidence: ocr model confidence
        """
        super().__init__()
        self.text = text
        self.bbox = bbox
        self.order = order
        self.confidence = confidence
