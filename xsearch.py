import urllib.request
import xml.etree.ElementTree as xmlTree
import string


def xsearch(sökning):
    sökning = sökning.replace(' ', '+')
    str = urllib.request.urlopen("http://libris.kb.se/xsearch?query=" + sökning + "&format=marcxml&format_level=full").read()
    xmlRoot = xmlTree.fromstring(str)
    #n = 1 + int(xmlRoot.attrib['to']) - int(xmlRoot.attrib['from'])
    titel = ''
    upphovspersoner = []
    översättare = []
    for node in xmlRoot[0][1]:
        att = node.attrib
        if 'tag' in att:
            if att['tag'] == '100':
                upphovspersoner.append(node[0].text)
            elif att['tag'] == '245':
                for subfield in node:
                    if   subfield.attrib['code'] == 'a':
                        titel = subfield.text
                    elif subfield.attrib['code'] == 'b':
                        titel += " " + subfield.text
            elif att['tag'] == '700':
                if len(node) == 1:
                    upphovspersoner.append(node[0].text)
                else:
                    for subfield in node:
                        if subfield.attrib['code'] == '4':
                            if subfield.text == 'trl':
                                översättare.append(node[0].text)
    titel = titel.rstrip(' /')
    return (titel, upphovspersoner, översättare)

