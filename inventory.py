from twisted.web.resource import Resource
from twisted.web.template import XMLString, Element, renderer, renderElement

from twisted.python.filepath import FilePath
from twisted.web.util import redirectTo
from twisted.web.static import File

import config
import elements
import explorer
import json
import popups
import sys

from data import Domain
from data import db


class Main(Resource):
    def __init__(self):
        Resource.__init__(self)

    def render(self, request):
        #output = explorer.start()
        #request.write('<!DOCTYPE html>\n')
        return renderElement(request, Page())


class Page(Element):
    def __init__(self): 
        self.loader = XMLString(FilePath('templates/pages/inventory.xml').getContent())
        self.domains = db.query(Domain).order_by(Domain.name.asc())

    @renderer
    def menu(self, request, tag):
        return elements.Menu()

    @renderer
    def domain(self, request, tag):
        for domain in self.domains:
            self.domain = domain
            slots = {}
            slots['status'] = domain.status 
            slots['name'] = domain.name 
            slots['blocks'] = domain.blocks 
            slots['record'] = domain.record
            slots['rand1'] = domain.rand1[0:5] 
            slots['rand2'] = domain.rand2[0:5]

            conf = 'NA'
            if domain.confirmation:
                conf = domain.confirmation[0:5]

            slots['confirmation'] = conf
            yield tag.clone().fillSlots(**slots) 

    @renderer
    def count(self, request, tag):
        slots = {}
        slots['count'] = str(self.domains.count())
        yield tag.clone().fillSlots(**slots) 

    @renderer
    def action(self, request, tag):
        actions = {}
        actions[config.createTimestamp()] = ['activate', '../activate?name=%s' % self.domain.name]
        actions[config.createTimestamp()] = ['update', '../update?name=%s' % self.domain.name]

        for key in sorted(actions.keys()):
            slots = {}
            slots['action'] = actions[key][0]
            slots['url'] = actions[key][1]
            slots['name'] = self.domain.name 
            yield tag.clone().fillSlots(**slots)

    @renderer
    def updateDomainPopup(self, request, tag):
        return popups.UpdateDomain(self.domain)
        

class Load(Resource):
    def render(self, request):

        results = explorer.inventory()['result']
        print results

        sessionResults = []
        for result in results:
            sessionResults.append([result['name'], result['value'], result['expires_in']])
        return json.dumps(sessionResults) 


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
        
        rand = explorer.reserve(domain)['result']
        print
        print rand
        print rand[0]
        print rand[1]

        domain = Domain('reserved', timestamp, timestamp, domain, 'RESERVED', lastBlock, rand[0], rand[1], 'xxx')
        db.add(domain)
        db.commit()
        return redirectTo('../inventory', request)


class Activate(Resource):
    def render(self, request):
        print 'request.args: %s' % request.args
    
        name = request.args.get('name')[0]
   
        domain = db.query(Domain).filter(Domain.name == name).first()
        print domain.name

        timestamp = config.createTimestamp()
        print timestamp 

        #lastBlock = summary['blocks']
        #print lastBlock

        summary = explorer.summary()['result']
        blocks = summary['blocks']
        print blocks
        
        confirmation = explorer.activate(domain.name, domain.rand1, domain.rand2, 'RESERVED')['result']
        print confirmation 

        domain.status = 'active'
        domain.blocks = blocks 
        domain.updateTimestamp = timestamp
        domain.value = 'RESERVED'
        domain.confirmation = confirmation
        db.commit()
        return redirectTo('../inventory', request)


class Update(Resource):
    def render(self, request):
        print 'request.args: %s' % request.args
    
        name = request.args.get('name')[0]
        record = request.args.get('record')[0]
        
        strings = name.split('/')

        domain = db.query(Domain).filter(Domain.name == strings[1]).first()
        print domain.name

        timestamp = config.createTimestamp()
        #timestamp = config.convertTimestamp(timestamp)
        print timestamp 

        summary = explorer.summary()['result']
        blocks = summary['blocks']
        print blocks

        #lastBlock = summary['blocks']
        #print lastBlock
        
        confirmation = explorer.update(domain.name, '%s' % record)['result']
        print confirmation 

        domain.blocks = blocks
        domain.updateTimestamp = timestamp
        domain.record = record
        domain.confirmation = confirmation
        db.commit()
        return redirectTo('../inventory', request)
