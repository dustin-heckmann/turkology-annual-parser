from collections import OrderedDict

from lxml import etree


class WMLParser(object):
    def __init__(self, xml_filename):
        self.namespaces = {
            'w': 'http://schemas.microsoft.com/office/word/2003/wordml',
            'wx': 'http://schemas.microsoft.com/office/word/2003/auxHint',
        }
        self.document = etree.parse(xml_filename).getroot()
        self.paragraphs = self._extract_paragraphs()

    def _extract_paragraphs(self):
        paragraph_nodes = self._xpath('//w:p')
        for paragraph_index, paragraph_node in enumerate(paragraph_nodes):
            paragraph = {
                'originalIndex': paragraph_index,
            }
            paragraph.update(self._get_paragraph_text(paragraph_node))

            yield paragraph

    def _get_paragraph_text(self, paragraph_node):
        text_parts = []
        index_start = 0
        for text_node in self._xpath('w:r/w:t', element=paragraph_node):
            text_part = text_node.text
            if text_part is None:
                continue
            text_parts.append(text_part)
            index_end = index_start + len(text_part)
            index_start = index_end
        return {
            'text': ''.join(text_parts),
        }

    def _xpath(self, expression, element=None):
        element = element if element is not None else self.document
        if element is self.document:
            expression = '/w:wordDocument' + ('' if expression[0] == '/' else '/') + expression
        return element.xpath(expression, namespaces=self.namespaces)
