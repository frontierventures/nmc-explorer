from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.python import log
from twisted.web.template import XMLString, Element, renderer, renderElement

from twisted.python.filepath import FilePath
from twisted.web.util import redirectTo
from twisted.web.static import File

import elements
import explorer
import inventory
import json
import sys


class Main(Resource):
    def __init__(self):
        Resource.__init__(self)

    def render(self, request):
        output = explorer.summary()
        #request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page(output))


class Page(Element):
    def __init__(self, output):
        self.output = output
        self.loader = XMLString(FilePath('templates/pages/search.xml').getContent())

    @renderer
    def menu(self, request, tag):
        return elements.Menu()

    @renderer
    def summary(self, request, tag):
        print self.output
        slots = {}
        slots['blocks'] = "Current block: %s" % self.output['result']['blocks']
        slots['balance'] = "Balance: %s" % self.output['result']['balance']
        yield tag.clone().fillSlots(**slots) 


class Search(Resource):
    def render(self, request):
        print 'request.args: %s' % request.args

        query = request.args.get('query')[0]
        results = explorer.search(query)['result']
        print results

        sessionResults = []
        for result in results:
            sessionResults.append([result['name'], result['value'], result['expires_in']])
        return json.dumps(sessionResults) 


log.startLogging(sys.stdout)
root = Main()
root.putChild('', root)
root.putChild('search', Search())
root.putChild('scripts', File('./scripts'))
root.putChild('styles', File('./styles'))
root.putChild('inventory', inventory.Main())
root.putChild('loadInventory', inventory.Load())
root.putChild('reserve', inventory.Reserve())
root.putChild('activate', inventory.Activate())
root.putChild('update', inventory.Update())


reactor.listenTCP(8080, Site(root))
reactor.run()
