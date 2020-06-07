from lxml import etree

from domain.paragraph import Paragraph


class WMLParser(object):
    def __init__(self, xml_filename):
        self.namespaces = {
            'w': 'http://schemas.microsoft.com/office/word/2003/wordml',
            'wx': 'http://schemas.microsoft.com/office/word/2003/auxHint',
        }
        self._xml_filename = xml_filename
        self._document = None

    def __iter__(self):
        self._parse_xml()
        paragraph_nodes = self._xpath('//w:p')
        for paragraph_index, paragraph_node in enumerate(paragraph_nodes):
            yield Paragraph(
                originalIndex=paragraph_index,
                text=self._get_paragraph_text(paragraph_node),
            )

    def _get_paragraph_text(self, paragraph_node) -> str:
        text_parts = []
        index_start = 0
        for text_node in self._xpath('w:r/w:t', element=paragraph_node):
            text_part = text_node.text
            if text_part is None:
                continue
            text_parts.append(text_part)
            index_end = index_start + len(text_part)
            index_start = index_end
        return ''.join(text_parts)

    def _xpath(self, expression, element=None):
        element = element if element is not None else self._document
        if element is self._document:
            expression = '/w:wordDocument' + ('' if expression[0] == '/' else '/') + expression
        return element.xpath(expression, namespaces=self.namespaces)

    def _parse_xml(self):
        self._document = etree.parse(self._xml_filename).getroot()
