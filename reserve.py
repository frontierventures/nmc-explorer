from twisted.web.resource import Resource
from twisted.web.template import XMLString, Element, renderer, renderElement

from twisted.python.filepath import FilePath
from twisted.web.util import redirectTo
from twisted.web.static import File
from twisted.web.util import redirectTo

import config
import elements
import explorer
import json
import sys


class Main(Resource):
    def __init__(self):
        Resource.__init__(self)

    def render(self, request):
        #output = explorer.start()
        #request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page())


class Page(Element):
    def __init__(self):
        self.loader = XMLString(FilePath('templates/pages/reserve.xml').getContent())

    @renderer
    def menu(self, request, tag):
        return elements.Menu()


class Reserve(Resource):
    def render(self, request):
        print 'request.args: %s' % request.args
    
        domain = request.args.get('domain')[0]
   
        print domain
        timestamp = config.createTimestamp()
        print timestamp 

        summary = explorer.summary()['result']
        lastBlock = summary['blocks']
        print lastBlock
        #print results

        #sessionResults = []
        #for result in results:
        #    sessionResults.append([result['name'], result['value'], result['expires_in']])
        #return json.dumps(sessionResults) 
        return redirectTo('../inventory', request)
