import xml.etree.ElementTree as ET
import xml.dom.minidom


class XML2Dict(object):
    def make_dict(self, node):
        d = {}
        for child in node.getchildren():
            if child.tag == "item":
                return self.make_list(node.getchildren())
            elif has_digit_or_letter(child.text):
                d.update(self.make_item(child.tag, child.text))
            else:
                d[child.tag] = self.make_dict(child)
        return d

    def make_list(self, children):
        lst = []
        for child in children:
            if has_digit_or_letter(child.text):
                lst.append(child.text)
            else:
                lst.append(self.make_dict(child))
        return lst

    def make_item(self, key, value):
        return {key: value}

    def parse(self, xml):
        node = ET.parse(xml).getroot()
        return self.make_dict(node)


def has_digit_or_letter(string):
    return any(s.isalnum() for s in string)
