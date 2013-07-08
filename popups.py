from twisted.web.template import Element, renderer, XMLString
from twisted.python.filepath import FilePath

class UpdateDomain(Element):
    def __init__(self, domain): 
        self.loader = XMLString(FilePath('templates/popups/updateDomain.xml').getContent())
        self.domain = domain 
