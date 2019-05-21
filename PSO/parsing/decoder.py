import xml.etree.ElementTree as ET
import xml.dom.minidom

class Dict2XML():

    def parse_dict(self, dictionary, node):
        for tag, value in dictionary.items():
            if isinstance(value, dict):
                node.append(self.parse_dict(value, ET.Element(tag)))
            elif isinstance(value, list):
                node.append(self.parse_list(value, ET.Element(tag)))
            else:
                node.append(self.make_xml(tag, value))
        return node

    def parse_list(self, lst, node):
        for item in lst:
            if isinstance(item, dict):
                node.append(self.parse_dict(item, ET.Element('item')))
            else:
                node.append(self.make_xml('item', item))
        return node

    def make_xml(self, tag, value):
        element = ET.Element(tag)
        element.text = str(value)
        return element

    def parse(self, dictionary):
        node = ET.Element('data')
        xml_string = ET.tostring(self.parse_dict(dictionary, node))
        dom = xml.dom.minidom.parseString(xml_string)
        return dom.toprettyxml()