import urllib.request
import xml.etree.ElementTree as xmlTree
import string
import doctest

def xsearch(sökning):
    """Utför en sökning på Libris.kb.se databas och returnerar information on det första resultatet.
    Första elementet i returen är verkets titel, 
    andra elementet är en lista på upphovspersoner,
    tredje elementet är en lista på översättare,
    fjärde elementet är en länk till verkets sida.

    Om inga resultat finns returneras tomma element.
    Klarar tyvärr bara ascii, så ej åäö.

    >>> xsearch('adsger4geab')
    ('', [], [], '')
    >>> xsearch('J.K. Rowling Harry Potter och Fenixorden')
    ('Harry Potter och Fenixorden', ['Rowling, J. K.'], ['Fries-Gedin, Lena,'], 'http://libris.kb.se/bib/9391585')
    """
    sökning = sökning.replace(' ', '+')
    try:
        str = urllib.request.urlopen("http://libris.kb.se/xsearch?query=" + sökning + "&format=marcxml&format_level=full").read()
        xmlRoot = xmlTree.fromstring(str)
    except UnicodeEncodeError as err:
        print('Funktionen klarar tyvärr bara ascii.')
        if 'å' in sökning or 'ä' in sökning or 'ö' in sökning:
            print('Så ej åäö.')
        return ('', [], [], '')
    if xmlRoot.attrib['to'] == 'NaN':
        return ('',[],[],'')
    #n = 1 + int(xmlRoot.attrib['to']) - int(xmlRoot.attrib['from'])
    titel = ''
    upphovspersoner = []
    översättare = []
    id = ''
    for node in xmlRoot[0][1]:
        att = node.attrib
        if 'tag' in att:
            if att['tag'] == '001':
                id = node.text
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
    länk = f'http://libris.kb.se/bib/{id}'
    return (titel, upphovspersoner, översättare, länk)

doctest.testmod()